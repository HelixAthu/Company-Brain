import logging
import re
import json
from typing import Optional, Dict, Any, List, Tuple
from backend.config import settings
from backend.graph_executor import execute_cypher, GraphExecutionResult
from backend.models import Citation, TraversedNode

logger = logging.getLogger("company_brain.ai")

CYPHER_SYSTEM_PROMPT = """
You are DevTrace AI, an expert Cypher query generator for FalkorDB graph database in an enterprise setting.
Your task is to translate natural language questions into single, executable, read-only Cypher queries.

### Graph Database Schema:
Nodes:
- Person: {id, name, role, email, slack}
- Team: {id, name, domain, slack_channel}
- System: {id, name, tier, repo_url, status, description}
- Document: {id, title, type, url, last_updated}
- Decision: {id, title, status, rationale, date}

Relationships:
- (:Person)-[:MEMBER_OF]->(:Team)
- (:Team)-[:OWNS]->(:System)
- (:System)-[:DEPENDS_ON]->(:System)
- (:Person)-[:AUTHORED]->(:Document)
- (:Document)-[:DOCUMENTS]->(:System)
- (:Person)-[:RECORDED]->(:Decision)
- (:Decision)-[:DOCUMENTS]->(:System)

### Critical Rules:
1. Output ONLY the raw executable Cypher query.
2. DO NOT include markdown code blocks, backticks (```), explanations, or comments.
3. Only use read operations (MATCH, OPTIONAL MATCH, WHERE, RETURN, ORDER BY, LIMIT). NEVER use CREATE, DELETE, SET, or MERGE.
4. For case-insensitive search on names, use `toLower(n.name) CONTAINS toLower('...')` or exact matching.
5. Always alias return variables clearly (e.g., `RETURN s.name AS system_name, t.name AS owner_team`).
"""

SELF_CORRECTION_PROMPT = """
You are DevTrace AI, an expert Cypher query debugger for FalkorDB.
The previous Cypher query failed execution with a database error.

Original User Question: {prompt}
Failed Cypher Query:
{failed_cypher}

Database Error Message:
{error_message}

Please fix the query. Output ONLY the corrected executable Cypher query with no explanations, no markdown, and no backticks.
"""

SYNTHESIS_SYSTEM_PROMPT = """
You are DevTrace, an enterprise AI knowledge graph assistant for engineering teams.
Given a developer's question and graph traversal rows returned from FalkorDB, synthesize a clear, authoritative, and concise Markdown answer.

Structure your answer with:
1. Direct Executive Summary answering the user's question.
2. Key Graph Entities & Relationships (Owner team, on-call contact, dependencies).
3. Relevant Runbooks, Specs, or ADR Decisions.
"""

class GeminiAgent:
    """Core Google Gemini AI Agent client wrapper with Cypher generation, self-correction, and synthesis."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = "gemini-2.5-flash"
        self._client = None

    def get_client(self):
        """Lazy initialization of the official Google GenAI SDK client."""
        if self._client is not None:
            return self._client
        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            logger.info("Initialized Google GenAI client successfully.")
            return self._client
        except Exception as e:
            logger.warning(f"Could not initialize Google GenAI SDK: {e}. Will rely on fallback/mock mode if needed.")
            return None

    def is_configured(self) -> bool:
        """Check if a non-placeholder Gemini API key is configured."""
        return (
            bool(self.api_key) and 
            self.api_key != "your_gemini_api_key_here" and
            not self.api_key.startswith("your_")
        )

    def clean_cypher_output(self, raw_text: str) -> str:
        """Clean markdown formatting or extra whitespace from model output."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
        return cleaned.strip()

    def generate_cypher(self, prompt: str) -> str:
        """Translate a natural language question into an executable Cypher query."""
        if not self.is_configured():
            logger.info("Gemini API key is placeholder or unconfigured. Returning default template query.")
            return "MATCH (s:System)<-[:OWNS]-(t:Team) RETURN s.name AS system, t.name AS team, t.slack_channel AS slack"

        client = self.get_client()
        if not client:
            return "MATCH (s:System) RETURN s.name, s.tier, s.status LIMIT 10"

        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=[
                    {"role": "user", "parts": [{"text": f"{CYPHER_SYSTEM_PROMPT}\n\nUser Question: {prompt}\nCypher Query:"}]}
                ]
            )
            raw_cypher = response.text or ""
            return self.clean_cypher_output(raw_cypher)
        except Exception as e:
            logger.error(f"Error calling Gemini for Cypher translation: {e}")
            raise

    def correct_cypher(self, prompt: str, failed_cypher: str, error_message: str) -> str:
        """Self-correction prompt: send error feedback to Gemini to generate fixed Cypher."""
        logger.warning(f"Attempting Cypher self-correction. Error was: {error_message}")
        if not self.is_configured():
            return failed_cypher

        client = self.get_client()
        if not client:
            return failed_cypher

        formatted_prompt = SELF_CORRECTION_PROMPT.format(
            prompt=prompt,
            failed_cypher=failed_cypher,
            error_message=error_message
        )
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=[{"role": "user", "parts": [{"text": formatted_prompt}]}]
            )
            corrected = self.clean_cypher_output(response.text or "")
            logger.info(f"Self-corrected Cypher query: {corrected}")
            return corrected
        except Exception as e:
            logger.error(f"Error during self-correction request: {e}")
            return failed_cypher

    def execute_with_self_correction(self, prompt: str, max_retries: int = 1) -> GraphExecutionResult:
        """Pipeline that generates, executes, and self-corrects Cypher queries against FalkorDB."""
        initial_cypher = self.generate_cypher(prompt)
        result = execute_cypher(initial_cypher)

        if result.success or max_retries <= 0:
            return result

        logger.info("Initial Cypher execution failed. Triggering self-correction loop...")
        corrected_cypher = self.correct_cypher(prompt, initial_cypher, result.error or "Unknown syntax error")
        corrected_result = execute_cypher(corrected_cypher)
        return corrected_result

    def extract_citations_from_data(self, data: List[Dict[str, Any]]) -> List[Citation]:
        """Extract citations (documents, ADRs, runbooks) from graph result rows."""
        citations = []
        seen = set()
        for row in data:
            for k, v in row.items():
                if isinstance(v, dict):
                    title = v.get("title") or v.get("name")
                    url = v.get("url")
                    c_type = v.get("type", "Documentation")
                    if title and title not in seen:
                        seen.add(title)
                        citations.append(Citation(title=title, url=url, type=c_type))
                elif isinstance(v, str) and ("http" in v or "wiki" in v):
                    if v not in seen:
                        seen.add(v)
                        citations.append(Citation(title=k.replace("_", " ").title(), url=v, type="Reference"))
        return citations

    def synthesize_answer(
        self,
        prompt: str,
        cypher: str,
        graph_rows: List[Dict[str, Any]],
        traversed_nodes: List[Dict[str, Any]]
    ) -> Tuple[str, List[Citation]]:
        """Synthesize natural language response and extract citations from graph traversal results."""
        citations = self.extract_citations_from_data(graph_rows)

        # Fallback local synthesis if Gemini is unconfigured
        if not self.is_configured():
            if not graph_rows:
                return (
                    f"### Graph Traversal Result\nNo matching entities found in FalkorDB for: *\"{prompt}\"*.\n\nExecuted Cypher:\n```cypher\n{cypher}\n```",
                    citations
                )
            formatted_rows = "\n".join([f"- **Record {idx+1}:** " + ", ".join([f"`{k}`: {v}" for k, v in r.items()]) for idx, r in enumerate(graph_rows[:5])])
            answer = (
                f"### Graph Intelligence Summary\n"
                f"Based on real-time graph traversal in **FalkorDB**, here are the findings for: *\"{prompt}\"*\n\n"
                f"{formatted_rows}\n\n"
                f"> **Provenance Path:** Identified **{len(traversed_nodes)}** connected entities in the enterprise graph."
            )
            return answer, citations

        client = self.get_client()
        if not client:
            return f"Answer generated from graph data ({len(graph_rows)} records returned).", citations

        try:
            synthesis_input = f"""
{SYNTHESIS_SYSTEM_PROMPT}

Developer Prompt: {prompt}
Executed Cypher Query: {cypher}
Raw Graph Results (FalkorDB JSON):
{json.dumps(graph_rows[:10], indent=2)}

Please synthesize the final answer:
"""
            response = client.models.generate_content(
                model=self.model_name,
                contents=[{"role": "user", "parts": [{"text": synthesis_input}]}]
            )
            answer = response.text or "Graph query executed successfully."
            return answer, citations
        except Exception as e:
            logger.error(f"Error synthesizing answer via Gemini: {e}")
            return f"Query executed successfully against FalkorDB with {len(graph_rows)} results returned.", citations

# Global singleton
gemini_agent = GeminiAgent()

import logging
import re
from typing import Optional
from backend.config import settings

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

class GeminiAgent:
    """Core Google Gemini AI Agent client wrapper."""

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
            logger.info("Gemini API key is placeholder or unconfigured. Returning template Cypher.")
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

# Global singleton
gemini_agent = GeminiAgent()

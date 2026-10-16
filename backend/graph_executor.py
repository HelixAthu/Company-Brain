import time
import logging
from typing import Dict, Any, List, Optional
from backend.database import get_graph

logger = logging.getLogger("company_brain.graph_executor")

class GraphExecutionResult:
    def __init__(
        self,
        success: bool,
        cypher: str,
        data: List[Dict[str, Any]],
        traversed_nodes: List[Dict[str, Any]],
        error: Optional[str] = None,
        execution_time_ms: float = 0.0
    ):
        self.success = success
        self.cypher = cypher
        self.data = data
        self.traversed_nodes = traversed_nodes
        self.error = error
        self.execution_time_ms = execution_time_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "cypher": self.cypher,
            "data": self.data,
            "traversed_nodes": self.traversed_nodes,
            "error": self.error,
            "execution_time_ms": self.execution_time_ms
        }

def extract_nodes_from_row(row_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Inspect row fields to extract graph entities for frontend visualization."""
    nodes = []
    for key, value in row_dict.items():
        if isinstance(value, dict) and ("name" in value or "id" in value):
            node_type = value.get("label", key.capitalize())
            nodes.append({
                "id": str(value.get("id", value.get("name"))),
                "name": str(value.get("name", value.get("id"))),
                "type": node_type,
                "details": value
            })
        elif isinstance(value, str) and key.endswith(("_name", "_service", "_team", "system", "team", "person")):
            nodes.append({
                "id": value.lower().replace(" ", "_"),
                "name": value,
                "type": key.split("_")[0].capitalize(),
                "details": {key: value}
            })
    return nodes

def execute_cypher(cypher_query: str) -> GraphExecutionResult:
    """Execute dynamic Cypher query against FalkorDB and return structured results."""
    start_time = time.time()
    graph = get_graph()

    if graph is None:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.warning("FalkorDB graph instance unavailable for Cypher execution.")
        return GraphExecutionResult(
            success=False,
            cypher=cypher_query,
            data=[],
            traversed_nodes=[],
            error="FalkorDB connection unavailable. Ensure container is active on port 6379.",
            execution_time_ms=duration_ms
        )

    try:
        logger.info(f"Executing Cypher against FalkorDB: {cypher_query}")
        result_set = graph.query(cypher_query)
        duration_ms = round((time.time() - start_time) * 1000, 2)

        data = []
        traversed_nodes = []
        seen_node_ids = set()

        # FalkorDB result parsing
        header = [col[1].decode() if isinstance(col[1], bytes) else str(col[1]) for col in getattr(result_set, "header", [])]
        
        for row in getattr(result_set, "result_set", []):
            row_dict = {}
            for idx, val in enumerate(row):
                col_name = header[idx] if idx < len(header) else f"col_{idx}"
                # Handle FalkorDB node objects or primitives
                if hasattr(val, "properties"):
                    row_dict[col_name] = val.properties
                else:
                    row_dict[col_name] = val.decode() if isinstance(val, bytes) else val
            data.append(row_dict)

            # Extract visited entities for graph trace inspector
            for node in extract_nodes_from_row(row_dict):
                if node["id"] not in seen_node_ids:
                    seen_node_ids.add(node["id"])
                    traversed_nodes.append(node)

        return GraphExecutionResult(
            success=True,
            cypher=cypher_query,
            data=data,
            traversed_nodes=traversed_nodes,
            execution_time_ms=duration_ms
        )

    except Exception as e:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        error_msg = str(e)
        logger.error(f"Cypher execution failed: {error_msg}")
        return GraphExecutionResult(
            success=False,
            cypher=cypher_query,
            data=[],
            traversed_nodes=[],
            error=error_msg,
            execution_time_ms=duration_ms
        )

import logging
from typing import Optional
from backend.config import settings

logger = logging.getLogger("company_brain.database")

class FalkorDBManager:
    _instance: Optional["FalkorDBManager"] = None

    def __init__(self):
        self.host = settings.FALKORDB_HOST
        self.port = settings.FALKORDB_PORT
        self.graph_name = settings.FALKORDB_GRAPH
        self._driver = None
        self._graph = None

    @classmethod
    def get_instance(cls) -> "FalkorDBManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def connect(self):
        try:
            from falkordb import FalkorDB
            self._driver = FalkorDB(host=self.host, port=self.port)
            self._graph = self._driver.select_graph(self.graph_name)
            logger.info(f"Connected to FalkorDB at {self.host}:{self.port}, graph: '{self.graph_name}'")
            return self._graph
        except Exception as e:
            logger.warning(f"Could not connect to FalkorDB at {self.host}:{self.port}: {e}")
            self._driver = None
            self._graph = None
            return None

    def get_graph(self):
        if self._graph is None:
            return self.connect()
        return self._graph

    def is_connected(self) -> bool:
        try:
            graph = self.get_graph()
            if graph is not None:
                # Simple ping query
                res = graph.query("RETURN 1 AS ping")
                return len(res.result_set) > 0
            return False
        except Exception:
            return False

# Global singleton helper
db_manager = FalkorDBManager.get_instance()

def get_graph():
    """Retrieve the active FalkorDB graph instance."""
    return db_manager.get_graph()

import logging
import sys
import os

# Ensure backend package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import get_graph

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("company_brain.seeder")

def clear_graph(graph):
    """Safely detach and delete all existing nodes and edges."""
    logger.info("Clearing existing nodes and relationships from graph...")
    try:
        graph.query("MATCH (n) DETACH DELETE n")
        logger.info("Graph reset complete.")
    except Exception as e:
        logger.error(f"Error resetting graph: {e}")
        raise

def seed_database():
    """Main database seeding pipeline."""
    logger.info("Starting FalkorDB Company Brain seeding pipeline...")
    graph = get_graph()
    if graph is None:
        logger.error("Could not obtain FalkorDB graph handle. Ensure FalkorDB container is running on port 6379.")
        return False

    clear_graph(graph)
    logger.info("Base graph initialization complete.")
    return True

if __name__ == "__main__":
    success = seed_database()
    if not success:
        sys.exit(1)

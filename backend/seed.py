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

def seed_teams_and_people(graph):
    """Seed engineering squads and personnel with MEMBER_OF relationships."""
    logger.info("Seeding engineering teams and personnel...")
    queries = [
        # Create Teams
        """
        CREATE (t1:Team {id: 'payments_team', name: 'Payments Team', domain: 'Payments & FinTech', slack_channel: '#team-payments'})
        CREATE (t2:Team {id: 'core_infra', name: 'Core Infra', domain: 'Cloud & Database Infrastructure', slack_channel: '#core-infra'})
        CREATE (t3:Team {id: 'identity_team', name: 'Identity Team', domain: 'Authentication & Security', slack_channel: '#identity-sec'})
        """,
        # Create People and link to Teams
        """
        MATCH (t_pay:Team {id: 'payments_team'}), (t_infra:Team {id: 'core_infra'}), (t_id:Team {id: 'identity_team'})
        CREATE (p1:Person {id: 'alice_johnson', name: 'Alice Johnson', role: 'Staff Infrastructure Engineer', email: 'alice.j@company.internal', slack: '@alice'})
        CREATE (p2:Person {id: 'bob_smith', name: 'Bob Smith', role: 'Senior Payments Engineer', email: 'bob.s@company.internal', slack: '@bob'})
        CREATE (p3:Person {id: 'charlie_davis', name: 'Charlie Davis', role: 'Principal Security Engineer', email: 'charlie.d@company.internal', slack: '@charlie'})
        CREATE (p4:Person {id: 'elena_rostova', name: 'Elena Rostova', role: 'Staff Backend Architect', email: 'elena.r@company.internal', slack: '@elena'})
        CREATE (p1)-[:MEMBER_OF {role: 'Lead Infra'}]->(t_infra)
        CREATE (p2)-[:MEMBER_OF {role: 'Payments Contributor'}]->(t_pay)
        CREATE (p3)-[:MEMBER_OF {role: 'Security Lead'}]->(t_id)
        CREATE (p4)-[:MEMBER_OF {role: 'Tech Lead'}]->(t_pay)
        """
    ]
    for q in queries:
        graph.query(q)
    logger.info("Teams and personnel seeded successfully.")

def seed_database():
    """Main database seeding pipeline."""
    logger.info("Starting FalkorDB Company Brain seeding pipeline...")
    graph = get_graph()
    if graph is None:
        logger.error("Could not obtain FalkorDB graph handle. Ensure FalkorDB container is running on port 6379.")
        return False

    clear_graph(graph)
    seed_teams_and_people(graph)
    logger.info("Teams and personnel initialization complete.")
    return True

if __name__ == "__main__":
    success = seed_database()
    if not success:
        sys.exit(1)

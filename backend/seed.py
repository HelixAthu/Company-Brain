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

def seed_systems_and_dependencies(graph):
    """Seed microservices, databases, and architectural DEPENDS_ON / OWNS edges."""
    logger.info("Seeding microservices systems and dependency tree...")
    queries = [
        # Create Systems
        """
        CREATE (s1:System {id: 'payment_gateway', name: 'Payment Gateway', tier: 'Tier-1', repo_url: 'github.com/company/payment-gateway', status: 'production', description: 'Core transaction orchestrator and payment processor'})
        CREATE (s2:System {id: 'auth_microservice', name: 'Auth Microservice', tier: 'Tier-1', repo_url: 'github.com/company/auth-service', status: 'production', description: 'Authentication and JWT authorization authority'})
        CREATE (s3:System {id: 'billing_db', name: 'Billing DB', tier: 'Tier-1', repo_url: 'github.com/company/billing-cluster', status: 'production', description: 'Primary PostgreSQL cluster for transactions and billing accounts'})
        CREATE (s4:System {id: 'notification_svc', name: 'Notification Service', tier: 'Tier-2', repo_url: 'github.com/company/notification-svc', status: 'production', description: 'Dispatches real-time webhooks, emails, and transaction receipts'})
        CREATE (s5:System {id: 'redis_cache', name: 'Redis Cache Cluster', tier: 'Tier-2', repo_url: 'github.com/company/cache-cluster', status: 'deprecated', description: 'Legacy in-memory cache, superseded by FalkorDB graph layer'})
        CREATE (s6:System {id: 'falkordb_graph', name: 'FalkorDB Graph Engine', tier: 'Tier-1', repo_url: 'github.com/company/falkordb-cluster', status: 'production', description: 'High-performance Low-Latency Cypher Graph Engine for Company Brain'})
        """,
        # Link Teams to Systems (OWNS)
        """
        MATCH (t_pay:Team {id: 'payments_team'}), (t_infra:Team {id: 'core_infra'}), (t_id:Team {id: 'identity_team'})
        MATCH (s1:System {id: 'payment_gateway'}), (s2:System {id: 'auth_microservice'}), (s3:System {id: 'billing_db'}), (s4:System {id: 'notification_svc'}), (s5:System {id: 'redis_cache'}), (s6:System {id: 'falkordb_graph'})
        CREATE (t_pay)-[:OWNS {sla: '99.99%', on_call_rotation: 'weekly'}]->(s1)
        CREATE (t_id)-[:OWNS {sla: '99.99%', on_call_rotation: 'weekly'}]->(s2)
        CREATE (t_infra)-[:OWNS {sla: '99.999%', on_call_rotation: 'primary'}]->(s3)
        CREATE (t_pay)-[:OWNS {sla: '99.9%', on_call_rotation: 'bi-weekly'}]->(s4)
        CREATE (t_infra)-[:OWNS {sla: 'deprecated', on_call_rotation: 'none'}]->(s5)
        CREATE (t_infra)-[:OWNS {sla: '99.99%', on_call_rotation: 'primary'}]->(s6)
        """,
        # Link System Dependencies (DEPENDS_ON)
        """
        MATCH (s1:System {id: 'payment_gateway'}), (s2:System {id: 'auth_microservice'}), (s3:System {id: 'billing_db'}), (s4:System {id: 'notification_svc'}), (s6:System {id: 'falkordb_graph'})
        CREATE (s1)-[:DEPENDS_ON {protocol: 'gRPC', critical: true}]->(s2)
        CREATE (s1)-[:DEPENDS_ON {protocol: 'TCP / SSL', critical: true}]->(s3)
        CREATE (s1)-[:DEPENDS_ON {protocol: 'Async Webhook', critical: false}]->(s4)
        CREATE (s2)-[:DEPENDS_ON {protocol: 'SQL', critical: true}]->(s3)
        CREATE (s4)-[:DEPENDS_ON {protocol: 'SQL', critical: true}]->(s3)
        CREATE (s1)-[:DEPENDS_ON {protocol: 'Cypher / Bolt', critical: false}]->(s6)
        """
    ]
    for q in queries:
        graph.query(q)
    logger.info("Systems and dependency graph seeded successfully.")

def seed_documents_and_decisions(graph):
    """Seed technical runbooks, architecture specs, and Architecture Decision Records (ADRs)."""
    logger.info("Seeding documentation and architectural decisions...")
    queries = [
        # Create Documents
        """
        CREATE (d1:Document {id: 'doc_payment_runbook', title: 'Payment Gateway Incident Runbook & Disaster Recovery', type: 'Runbook', url: 'https://wiki.company.internal/runbooks/payment-gateway', last_updated: '2026-03-15'})
        CREATE (d2:Document {id: 'doc_auth_spec', title: 'Zero Trust Authentication & OAuth2 Architecture Specification', type: 'Architecture Spec', url: 'https://wiki.company.internal/specs/zero-trust-auth', last_updated: '2026-01-10'})
        CREATE (d3:Document {id: 'doc_billing_disaster', title: 'Billing DB Failover Procedure & Hot Standby Runbook', type: 'Runbook', url: 'https://wiki.company.internal/runbooks/billing-db-failover', last_updated: '2026-02-28'})
        """,
        # Create Decisions (ADRs)
        """
        CREATE (dec1:Decision {id: 'adr_012_falkordb_migration', title: 'ADR-012: Migration from Legacy Redis Cache to FalkorDB Graph Engine', status: 'Accepted', rationale: 'FalkorDB provides sub-millisecond graph traversals and Cypher queries for deep service dependency mapping, replacing inflexible Redis key-value lookups.', date: '2026-02-01'})
        CREATE (dec2:Decision {id: 'adr_008_jwt_sso', title: 'ADR-008: Adoption of Ed25519 JWT Tokens for Auth Microservice', status: 'Accepted', rationale: 'Reduces token signing latency by 45% and improves multi-datacenter verification resilience.', date: '2025-11-20'})
        """,
        # Link Authorship and Documentation
        """
        MATCH (p_alice:Person {id: 'alice_johnson'}), (p_bob:Person {id: 'bob_smith'}), (p_charlie:Person {id: 'charlie_davis'})
        MATCH (s_pay:System {id: 'payment_gateway'}), (s_auth:System {id: 'auth_microservice'}), (s_bill:System {id: 'billing_db'}), (s_cache:System {id: 'redis_cache'}), (s_graph:System {id: 'falkordb_graph'})
        MATCH (d1:Document {id: 'doc_payment_runbook'}), (d2:Document {id: 'doc_auth_spec'}), (d3:Document {id: 'doc_billing_disaster'})
        MATCH (dec1:Decision {id: 'adr_012_falkordb_migration'}), (dec2:Decision {id: 'adr_008_jwt_sso'})

        CREATE (p_bob)-[:AUTHORED]->(d1)
        CREATE (d1)-[:DOCUMENTS]->(s_pay)

        CREATE (p_charlie)-[:AUTHORED]->(d2)
        CREATE (d2)-[:DOCUMENTS]->(s_auth)

        CREATE (p_alice)-[:AUTHORED]->(d3)
        CREATE (d3)-[:DOCUMENTS]->(s_bill)

        CREATE (p_alice)-[:RECORDED]->(dec1)
        CREATE (dec1)-[:DOCUMENTS]->(s_cache)
        CREATE (dec1)-[:DOCUMENTS]->(s_graph)

        CREATE (p_charlie)-[:RECORDED]->(dec2)
        CREATE (dec2)-[:DOCUMENTS]->(s_auth)
        """
    ]
    for q in queries:
        graph.query(q)
    logger.info("Documents, ADRs, and provenance links seeded successfully.")

def seed_database():
    """Main database seeding pipeline."""
    logger.info("Starting FalkorDB Company Brain seeding pipeline...")
    graph = get_graph()
    if graph is None:
        logger.error("Could not obtain FalkorDB graph handle. Ensure FalkorDB container is running on port 6379.")
        return False

    clear_graph(graph)
    seed_teams_and_people(graph)
    seed_systems_and_dependencies(graph)
    seed_documents_and_decisions(graph)
    logger.info("Complete graph knowledge base initialization complete.")
    return True

if __name__ == "__main__":
    success = seed_database()
    if not success:
        sys.exit(1)

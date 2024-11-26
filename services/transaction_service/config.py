from neo4j import GraphDatabase
import redis

# Database connections
neo4j_driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "password")
)

redis_client = redis.Redis(
    host='redis',
    port=6379,
    decode_responses=True
)

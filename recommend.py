 
# from neo4j import GraphDatabase

# def recommend_movies(driver, watched_movie):
#     query = """
#     MATCH (m:Movie {title: $watched_movie})-[:SIMILAR_TO]-(recommendations)
#     RETURN recommendations.title AS title
#     LIMIT 3
#     """
#     with driver.session() as session:
#         results = session.run(query, watched_movie=watched_movie)
#         return [record["title"] for record in results]
# from neo4j import GraphDatabase

# # Connect to the Neo4j database
# uri = "bolt://localhost:7687"  # Update with your database URI
# driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# def create_relationships(tx):
#     query = """
#     MATCH (m1:Movie), (m2:Movie)
#     WHERE m1.genre = m2.genre AND m1.title <> m2.title
#     CREATE (m1)-[:SIMILAR_TO]->(m2)
#     LIMIT 3
#     """
#     tx.run(query)

# with driver.session() as session:
#     session.write_transaction(create_relationships)

# driver.close()
# recommend.py
# from neo4j import GraphDatabase

# # Initialize Neo4j Driver
# uri = "bolt://localhost:7687"  # Default URI
# username = "neo4j"
# password = "password"  # Replace with your Neo4j password

# driver = GraphDatabase.driver(uri, auth=(username, password))

# def get_recommendations(watched_movie):
#     query = """
#     MATCH (m:Movie {title: $watched_movie})-[:SIMILAR_TO]-(recommendations:Movie)
#     RETURN recommendations.title AS title
#     LIMIT 3
#     """
#     recommendations = []

#     with driver.session() as session:
#         results = session.run(query, watched_movie=watched_movie)
#         for record in results:
#             recommendations.append(record["title"])

#     return recommendations
# recommend.py
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Default URI
username = "neo4j"
password = "password"  # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

def get_recommendations(watched_movie):
    query = """
    MATCH (m:Movie {title: $watched_movie})-[:SIMILAR_TO]-(recommendations:Movie)
    RETURN recommendations.title AS title
    LIMIT 3
    """


    recommendations = []

    with driver.session() as session:
        results = session.run(query, watched_movie=watched_movie)
        # Debugging the results
        print(f"Results for '{watched_movie}': {results}")
        for record in results:
            recommendations.append(record["title"])

    if not recommendations:
        print(f"No recommendations found for '{watched_movie}'.")

    return recommendations

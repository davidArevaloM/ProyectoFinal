from neo4j import GraphDatabase
import json

# Conectar a la Base de Datos
URI = "neo4j+s://ce19c87f.databases.neo4j.io"
AUTH = ("neo4j", "GuPlCLhONEe3XnvgkzK6muCSK8WTRU8zZGt8kCzkb8A")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

with open('Similitud.json', 'r') as file:
    data = json.load(file)

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    try:
        for dat in data:
            records, summary, keys = driver.execute_query(
                "MERGE (p1:Providencia {nombre: $dat.providencia1})"
                "MERGE (p2:Providencia {nombre: $dat.providencia2})"
                "MERGE (p1)-[r:Similar {similitud: $dat.index_simm}]->(p2)",
                dat = dat,
                database="neo4j",
            )
    except Exception as e:
        print(e)
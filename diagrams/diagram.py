from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python

with Diagram("System Architecture", show=True):
    with Cluster("Frontend"):
        frontend = Server("Streamlit")
    with Cluster("Backend"):
        backend = Server("FastAPI")
        nlp = Python("GPT API")
        pinecone = Server("Pinecone")
    database = PostgreSQL("Database")

    frontend >> backend
    backend >> nlp
    backend >> pinecone
    backend >> database

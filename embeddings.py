import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("repository_docs")
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store(docs):
    for doc in docs:
        embedding = model.encode(doc["message"]).tolist()
        collection.add(doc_id=doc["hash"], embedding=embedding, metadata=doc)


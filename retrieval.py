from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("repository_docs")
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_docs(query, repo_data):
    if not repo_data:
        return ["Nenhuma informação encontrada sobre este repositório."]

    query_embedding = model.encode(query).tolist()

    # Criar listas para adicionar ao ChromaDB no formato correto
    ids = []
    embeddings = []
    metadatas = []

    for doc in repo_data:
        ids.append(str(doc["hash"])) 
        embeddings.append(model.encode(doc["message"]).tolist()) 

        modified_files_str = ", ".join(doc["modified_files"]) if doc["modified_files"] else "Nenhum arquivo modificado"

        metadata = {
            "hash": doc["hash"],
            "author": doc["author"],
            "date": doc["date"],
            "message": doc["message"],
            "modified_files": modified_files_str  
        }

        metadatas.append(metadata)

    # Adiciona os dados ao banco vetorial ChromaDB
    if ids: 
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

    results = collection.query(query_embeddings=[query_embedding], n_results=4)

    if not results or "documents" not in results or not results["documents"]:
        return ["Nenhuma informação relevante foi encontrada para essa pergunta."]

    return results["documents"]


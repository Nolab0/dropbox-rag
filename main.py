import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from dropboxDriver import connect_to_dropbox, list_files
from rag import create_vector_store, query_rag
from utils import process_files

load_dotenv()

app = FastAPI()

# Load Dropbox files and create vector store at startup
dbx = connect_to_dropbox()
data_to_embed = process_files(dbx)
vector_store = create_vector_store(data_to_embed)

@app.get("/query")
def query_rag_endpoint(question: str = Query(..., title="User question")):
    docs, response = query_rag(vector_store, question)
    return {"response": response, "relevant_snippets": docs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

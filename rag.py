from os import getenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain import hub


def get_llm():
    return ChatOpenAI(
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base=getenv("OPENROUTER_BASE_URL"),
        model_name=getenv("MODEL_NAME"),
    )

def create_vector_store(text_data):
    """Chunk and embed text, then store it in FAISS."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    documents = []
    
    for doc in text_data:
        chunks = text_splitter.split_text(doc["text"])
        for chunk in chunks:
            documents.append(Document(page_content=chunk, metadata={"source": doc["filename"]}))

    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents, embedding_model)
    return vector_store

def query_rag(vector_store, query):
    """Retrieve relevant chunks and generate answers using an LLM."""
    context = vector_store.similarity_search(query, k=5)
    
    prompt = hub.pull("rlm/rag-prompt")

    llm = get_llm()

    docs_content = "\n\n".join(doc.page_content for doc in context)
    messages = prompt.invoke({"question": query, "context": docs_content})
    response = llm.invoke(messages)
    return docs_content, response.content

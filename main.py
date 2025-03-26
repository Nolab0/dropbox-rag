from dotenv import load_dotenv

from dropboxDriver import connect_to_dropbox, list_files
from rag import create_vector_store, query_rag
from utils import process_files

load_dotenv()

def main():
    dbx = connect_to_dropbox()
    files = list_files(dbx, "")
    for file in files:
        print(file.path_display)

    data_to_embed = process_files(dbx)
    vector_store = create_vector_store(data_to_embed)

    response, docs = query_rag(vector_store, "How many tourist in Paris region in 2019 ?")
    print(response)

if __name__ == "__main__":
    main()
    
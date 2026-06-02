
import os
import shutil#used to delete old index
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings #used to convert text into vector form
from langchain_community.vectorstores import FAISS

FAISS_INDEX_PATH = "faiss_index"            
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")#model obj 384 vector size.

def create_index(file_path: str):
    if os.path.exists(FAISS_INDEX_PATH):
        shutil.rmtree(FAISS_INDEX_PATH)#remove tree (folder + everything inside it)
    
    
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    
    documents = loader.load()#access path|extract text|returns a list of Document objects
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)#chunk is list as well

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f" Indexed {len(chunks)} chunks successfully.")

def get_retriever():    
    if not os.path.exists(FAISS_INDEX_PATH):
        return None
    try:
        vector_store = FAISS.load_local(
            FAISS_INDEX_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True#used to load the index from disk
        )
        return vector_store.as_retriever(search_kwargs={"k": 4})
    except Exception as e:
        print("FAISS Load Error:", e)
        return None


#1.text-->embedding model(HuggingFaceEmbeddings)->vector store(FAISS)[INDEXING]
#2.user querry-->embedding model(HuggingFaceEmbeddings)->vector store(FAISS)
#3.compare the vector form of user querry with vector form of text in vector store
#4.return the most similar chunk[During query:user_input → embedding → similarity search → top chunks]

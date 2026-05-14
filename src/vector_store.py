import os
from langchain_community.vectorstores import Chroma
from src.document_loader import load_pdf
from src.chunker import split_documents
from src.embedder import get_embedding_model

def create_vector_store(file_paths):
    """
    Loads, chunks, embeds, and stores multiple PDFs in ChromaDB.
    file_paths: Can be a single string path or a list of string paths.
    """
    # Ensure it's a list
    if isinstance(file_paths, str):
        file_paths = [file_paths]
        
    all_chunks = []
    
    # Process each PDF
    for file_path in file_paths:
        # 1. Load the PDF
        docs = load_pdf(file_path)
        # 2. Chunk the text
        chunks = split_documents(docs)
        all_chunks.extend(chunks)
        
    # If no chunks were extracted, exit early
    if not all_chunks:
        raise ValueError("No text could be extracted from the provided PDFs.")
        
    # 3. Get the embedding model
    embedder = get_embedding_model()
    
    # 4. Store in ChromaDB
    print("\nSaving to ChromaDB... (This may take a minute as it embeds all chunks)")
    
    persist_dir = os.path.join("/tmp", "vectorstore", "chroma_db")
    
    # This creates the database and saves it to disk
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embedder,
        persist_directory=persist_dir
    )
    
    print(f"Successfully saved {len(all_chunks)} chunks to {persist_dir}!")
    return vectorstore

def get_vector_store():
    """
    Loads an existing vector store from disk.
    """
    persist_dir = os.path.join("/tmp", "vectorstore", "chroma_db")
    if not os.path.exists(persist_dir):
        raise FileNotFoundError("Vector store not found. Create it first!")
        
    embedder = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=persist_dir, 
        embedding_function=embedder
    )
    return vectorstore

if __name__ == "__main__":
    # Test it! We will ingest the PDF into the database.
    test_file = os.path.join("data", "2023_IJBIS_Gabriel_vikas.pdf")
    create_vector_store(test_file)

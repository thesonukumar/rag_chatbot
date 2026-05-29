import os
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.document_loader import load_pdf
from src.chunker import split_documents
from src.embedder import get_embedding_model

def get_pinecone_index_name():
    # Changed index name so Pinecone creates a fresh one with the correct 3072 dimensions
    return "rag-chatbot-index-v2"

def create_vector_store(file_paths, session_id):
    """
    Loads, chunks, embeds, and stores multiple PDFs in Pinecone.
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]
        
    all_chunks = []
    for file_path in file_paths:
        docs = load_pdf(file_path)
        chunks = split_documents(docs)
        all_chunks.extend(chunks)
        
    if not all_chunks:
        raise ValueError("No text could be extracted from the provided PDFs.")
        
    embedder = get_embedding_model()
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index_name = get_pinecone_index_name()
    
    # Create index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        print(f"Creating Pinecone index '{index_name}' with dimension 3072...")
        pc.create_index(
            name=index_name,
            dimension=3072, # Dimension for gemini-embedding-2
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Wait for index to be ready
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
            
    print(f"\nSaving to Pinecone... (Session ID: {session_id})")
    
    # Initialize the vector store object first
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embedder,
        namespace=session_id
    )
    
    # Upload in batches to avoid overwhelming the Google 100 RPM limit
    batch_size = 25
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        print(f"Uploading chunk batch {i//batch_size + 1}...")
        
        for attempt in range(4): # Try up to 4 times
            try:
                vectorstore.add_documents(batch)
                break # Success! Break out of the retry loop
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "Quota exceeded" in error_msg:
                    print(f"⚠️ Google API Rate Limit hit! Sleeping for 60 seconds to reset quota... (Attempt {attempt+1})")
                    time.sleep(60)
                else:
                    # If it's a different error, crash immediately
                    raise e
        
        # Small delay between successful batches just to be safe
        time.sleep(2)
    
    print(f"Successfully saved {len(all_chunks)} chunks to Pinecone!")
    return vectorstore

def get_vector_store(session_id):
    """
    Loads an existing vector store from Pinecone for a specific session.
    """
    embedder = get_embedding_model()
    index_name = get_pinecone_index_name()
    
    vectorstore = PineconeVectorStore(
        index_name=index_name, 
        embedding=embedder,
        namespace=session_id
    )
    return vectorstore

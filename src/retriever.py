from src.vector_store import get_vector_store

def retrieve_relevant_chunks(question, session_id, k=15):
    """
    Searches the vector database for chunks related to the question.
    k: Number of chunks to return.
    """
    print(f"\nSearching for answers to: '{question}' in session {session_id}")
    
    # Load our database from Pinecone
    try:
        vectorstore = get_vector_store(session_id)
        results = vectorstore.similarity_search(question, k=k)
        print(f"Found top {len(results)} matching chunks.")
        return results
    except Exception as e:
        print(f"Error retrieving from vector store: {e}")
        return []

if __name__ == "__main__":
    pass

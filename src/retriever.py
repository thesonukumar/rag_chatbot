from src.vector_store import get_vector_store

def retrieve_relevant_chunks(question, k=3):
    """
    Searches the vector database for chunks related to the question.
    k: Number of chunks to return.
    """
    print(f"\nSearching for answers to: '{question}'")
    
    # Load our database from disk
    vectorstore = get_vector_store()
    
    # Perform similarity search
    # This converts the question to a vector, compares it to all 92 chunks,
    # and returns the top 'k' closest matches.
    results = vectorstore.similarity_search(question, k=k)
    
    print(f"Found top {k} matching chunks.")
    return results

if __name__ == "__main__":
    # Test it out! Let's ask a question relevant to the PDF.
    user_question = "What are the success factors for e-commerce according to the models?"
    
    chunks = retrieve_relevant_chunks(user_question)
    
    print("\n" + "="*50)
    print("RESULTS FOUND IN PDF:")
    print("="*50)
    
    for i, chunk in enumerate(chunks):
        print(f"\n--- MATCH {i+1} (From Page {chunk.metadata.get('page')}) ---")
        # Print the first 300 characters of each chunk so we can read it
        print(chunk.page_content[:300] + "...")

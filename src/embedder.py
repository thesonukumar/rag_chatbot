import os
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load API key from .env file
load_dotenv()

def get_embedding_model():
    """
    Initializes and returns the Google Gemini embedding model.
    """
    # Verify API key is present
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found. Please add it to your .env file!")

    # Initialize the Google Embedding model
    # "gemini-embedding-2" has the best rate limit (100 RPM) on your account
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    return embeddings

if __name__ == "__main__":
    print("Initializing Google Embeddings...")
    embedder = get_embedding_model()
    
    # Let's test it with two sentences!
    sentence1 = "I love shopping online for electronics."
    sentence2 = "E-commerce is my favorite way to buy gadgets."
    sentence3 = "The weather today is raining and cold."
    
    print("\nGenerating embeddings (this sends the text to Google)...")
    
    # Embed sentence 1 to see what a vector looks like
    vector1 = embedder.embed_query(sentence1)
    
    print(f"\nSuccessfully Created vector for Sentence 1.")
    print(f"Dimensions (Length of the list): {len(vector1)}")
    print(f"First 5 numbers in the vector: {vector1[:5]}")
    print("...")

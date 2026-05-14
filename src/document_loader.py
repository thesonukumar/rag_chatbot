import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    """
    Loads a PDF file and extracts text page by page.
    Returns a list of Document objects.
    """
    print(f"Loading PDF: {file_path}")
    
    # 1. Initialize the loader with the file path
    loader = PyPDFLoader(file_path)
    
    # 2. Extract the text! 
    # Returns a list where each item represents ONE page.
    pages = loader.load()
    
    print(f"Successfully loaded {len(pages)} pages.")
    return pages

if __name__ == "__main__":
    # Let's test it with one of your PDFs!
    # I'll pick the first one from your data folder:
    test_file = os.path.join("data", "2023_IJBIS_Gabriel_vikas.pdf")
    
    # Run the loader
    documents = load_pdf(test_file)
    
    # Print out a sample to verify
    if documents:
        print("\n--- SAMPLE PAGE 1 (First 500 characters) ---")
        # Every Document object has 'page_content' (the text) and 'metadata'
        print(documents[0].page_content[:500])
        print("...")
        print("\n--- METADATA FOR PAGE 1 ---")
        print(documents[0].metadata)

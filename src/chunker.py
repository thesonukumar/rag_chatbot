from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.document_loader import load_pdf
import os

def split_documents(documents):
    """
    Splits a list of Documents into smaller chunks.
    chunk_size: max characters per chunk
    chunk_overlap: characters shared between adjacent chunks
    """
    print(f"Splitting {len(documents)} pages into chunks...")
    
    # Initialize the splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    
    # Perform the split!
    chunks = text_splitter.split_documents(documents)
    
    print(f"Successfully split into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    # Test it out!
    test_file = os.path.join("data", "2023_IJBIS_Gabriel_vikas.pdf")
    docs = load_pdf(test_file)
    chunks = split_documents(docs)
    
    # Print the first chunk and its metadata
    print("\n--- CHUNK 1 ---")
    print(chunks[0].page_content)
    print("\n--- CHUNK 1 METADATA ---")
    print(chunks[0].metadata)
    
    # Print the second chunk to see the overlap
    print("\n--- CHUNK 2 ---")
    print(chunks[1].page_content)

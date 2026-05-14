from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from src.retriever import retrieve_relevant_chunks

def get_llm():
    """
    Initializes the Gemini generation model (Gemini 3.1 Flash Lite)
    """
    # Notice we use ChatGoogleGenerativeAI (for chatting) 
    # instead of GoogleGenerativeAIEmbeddings (for vectors)
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite", # Using exactly the model requested
        temperature=0.0  # 0.0 means "be factual, no creative guessing"
    )

def build_prompt():
    """
    Creates the instructions for the LLM.
    """
    prompt_template = """
    You are a helpful assistant analyzing a research paper.
    Answer the question based ONLY on the provided context below.
    If the context does not contain the answer, say "I cannot find the answer in the provided document."
    Do NOT use your outside knowledge.

    Context:
    {context}

    Question: 
    {question}

    Answer:
    """
    
    return PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

def generate_answer(question):
    """
    Retrieves chunks, builds the prompt, and generates an answer.
    """
    # 1. Get relevant chunks
    chunks = retrieve_relevant_chunks(question)
    
    # 2. Combine the text from all 3 chunks into one big string
    context_text = "\n\n".join([chunk.page_content for chunk in chunks])
    
    # 3. Build the final prompt
    prompt = build_prompt().format(context=context_text, question=question)
    
    # 4. Send to Gemini to get the answer!
    llm = get_llm()
    print("\nAsking Gemini to generate an answer...\n")
    response = llm.invoke(prompt)
    
    return response.content

if __name__ == "__main__":
    user_question = "What are the success factors for e-commerce according to the models?"
    answer = generate_answer(user_question)
    
    print("="*50)
    print("FINAL GENERATED ANSWER:")
    print("="*50)
    print(answer)

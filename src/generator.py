from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from src.retriever import retrieve_relevant_chunks

def get_llm():
    """
    Initializes the Gemini generation model.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite", # Best model based on API quota (15 RPM, 500 RPD)
        temperature=0.0
    )

def build_prompt():
    """
    Creates the instructions for the LLM, including history placeholder.
    """
    system_prompt = """
    You are a helpful assistant analyzing a document.
    Answer the user's question based ONLY on the provided context below.
    If the exact answer is not in the context, synthesize the most relevant information you can find, and explicitly state what part of the answer is missing from the document.
    Do NOT use your outside knowledge.

    Context:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    
    return prompt

def generate_answer(question, session_id, chat_history=None):
    """
    Retrieves chunks, builds the prompt, and generates an answer.
    """
    if chat_history is None:
        chat_history = []
        
    # Convert dict history to Langchain message objects
    formatted_history = []
    for msg in chat_history:
        if msg.get('role') == 'user':
            formatted_history.append(HumanMessage(content=msg.get('content', '')))
        elif msg.get('role') == 'assistant':
            formatted_history.append(AIMessage(content=msg.get('content', '')))

    # 1. Get relevant chunks
    chunks = retrieve_relevant_chunks(question, session_id=session_id)
    
    if not chunks:
        return "Please upload a PDF first."
        
    # 2. Combine the text
    context_text = "\n\n".join([chunk.page_content for chunk in chunks])
    
    # 3. Build the final prompt
    prompt = build_prompt()
    chain = prompt | get_llm()
    
    print("\nAsking Gemini to generate an answer...\n")
    response = chain.invoke({
        "context": context_text, 
        "chat_history": formatted_history,
        "question": question
    })
    
    return response.content

if __name__ == "__main__":
    pass

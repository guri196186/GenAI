import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

_ = load_dotenv(find_dotenv()) 

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.environ['OPENAI_API_KEY']
)


def get_session_history(chat_history, session_id: str):
    if session_id not in chat_history:
        chat_history[session_id] = InMemoryChatMessageHistory()
    return chat_history[session_id]

def set_up_conversation_chain(chat_history, session_id: str):

    session_id = input("Enter session id (or any name): ")
    history = get_session_history(chat_history, session_id) 
    memory = ConversationBufferMemory(chat_memory=history, return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise and helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history")
    ])
    chain = prompt | llm
    
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chat ended.")
            break
        # Add user message to memory
        memory.chat_memory.add_user_message(user_input)
        # Get AI response
        response = chain.invoke({"chat_history": memory.chat_memory.messages})
        print("AI:", response.content if hasattr(response, 'content') else response)
        # Add AI message to memory
        memory.chat_memory.add_ai_message(response.content if hasattr(response, 'content') else str(response))
    session_history = get_session_history(chat_history, session_id="Akriti")
    print("Session History:", session_history.messages) 
    # prompt = ChatPromptTemplate.from_messages([("system", "You are a concise and helpful assistant."),
    #     MessagesPlaceholder(variable_name="chat_history"),("human", "{question}"),("ai", "{response}")])
    
    # chain = prompt | llm

    # memory = ConversationBufferMemory(chat_memory=history, return_messages=True)
    
if __name__ == "__main__":
    
    chat_history = {}
    set_up_conversation_chain(chat_history, session_id="Akriti")
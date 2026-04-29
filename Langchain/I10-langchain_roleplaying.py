import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI 
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

_ = load_dotenv(find_dotenv()) 

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.environ['OPENAI_API_KEY']
)

#llm = OllamaLLM(model="llama3")


def chess_game_master():
    role = """Chess game master """
    tone = "engaging and immersive"
    template = """You are an expert {role}. I have this question {question}.I would like our conversation to be {tone}.
    Answer :"""
    
    prompt = ChatPromptTemplate.from_template(template)
    parser = StrOutputParser()
    chain = prompt | llm | parser
    
    while True:
        question = input("Ask a chess question (or 'exit' to quit): ")
        if question.lower() in ["quit", "exit", "bye"]:
            print("Answering chess questions is my pleasure! Goodbye!")
            break
        response = chain.invoke({"role": role, "question": question, "tone": tone})
        print("Answer :", response)
        
#MessagesPlaceholder - A placeholder that allows you to add a list of messages to a specific spot in a ChatPromptTemplate. 
def chatbot():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise and helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history")
    ])

    chat_history = [
        HumanMessage(content="Hello, my name is Akriti."),
        AIMessage(content="Hello Akriti! It's nice to meet you. How can I help you today?")
    ]

    chain = prompt | llm

    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chat ended.")
            break
        chat_history.append(HumanMessage(content=user_input))
        response = chain.invoke({"chat_history": chat_history})
        print("AI:", response.content if hasattr(response, 'content') else response)
        chat_history.append(AIMessage(content=response.content if hasattr(response, 'content') else str(response)))
    

if __name__ == "__main__":
    #chess_game_master()
    chatbot()
    
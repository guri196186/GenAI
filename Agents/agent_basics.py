import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain.agents import initialize_agent,Tool
from tool_basics import *

_ = load_dotenv(find_dotenv()) 

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.environ['OPENAI_API_KEY']
)


agent = initialize_agent([add_tool], llm, agent="zero-shot-react-description", 
                        verbose=True, handle_parsing_errors=True)

#Use the agent
response =agent.run("In 2023, the US GDP was approximately $27.72 trillion, while Canada's was \
                around $2.14 trillion and Mexico's was about $1.79 trillion what is the total.")
print(response)

agent.invoke({"input": "Add 10, 20, two and 30"})


agent_2 = initialize_agent([sum_numbers_from_text], llm, agent="structured-chat-zero-shot-react-description", verbose=True, handle_parsing_errors=True)
response = agent_2.invoke({"input": "Add 10, 20 and 30"})
print(response)

agent_3 = initialize_agent([sum_numbers_with_complex_output], llm, agent="openai-functions", verbose=True, handle_parsing_errors=True)
response = agent_3.invoke({"input": "Add 10, 20 and 30"})
print(response)

agent_openai = initialize_agent(
    [add_numbers_with_options],
    llm,
    agent="openai-functions",
    verbose=True
)

response = agent_openai.invoke({
    "input": "Add -10, -20, and -30 using absolute values."
})
print(response)
## build advanced AI agents that can dynamically interact with users ##
import os
from langchain.agents import initialize_agent, Tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_core.tools import tool

_ = load_dotenv(find_dotenv()) 

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=os.environ['OPENAI_API_KEY']
) 

@tool
def add(a: int, b: int) -> int:
    """
    Add a and b.
    
    Args:
        a (int): first integer to be added
        b (int): second integer to be added

    Return:
        int: sum of a and b
    """
    return a + b

@tool
def subtract(a: int, b:int) -> int:
    """Subtract b from a."""
    return a - b

@tool
def multiply(a: int, b:int) -> int:
    """Multiply a and b."""
    return a * b

tool_map = {
    "add": add, 
    "subtract": subtract,
    "multiply": multiply
}

input_ = {
    "a": 1,
    "b": 2
}
tools = [add, subtract, multiply]
result = tool_map["add"].invoke(input_)
print(result)

llm_with_tools = llm.bind_tools(tools)

print(f'######## Testing ###############')
query = "What is 3 + 2?"
chat_history = [HumanMessage(content=query)]
response_1 = llm_with_tools.invoke(chat_history)
chat_history.append(response_1)
print(type(response_1))

tool_calls_1 = response_1.tool_calls

tool_1_name = tool_calls_1[0]["name"]
tool_1_args = tool_calls_1[0]["args"]
tool_call_1_id = tool_calls_1[0]["id"]

print(f'tool name:\n{tool_1_name}')
print(f'tool args:\n{tool_1_args}')
print(f'tool call ID:\n{tool_call_1_id}')

# Given the tool call details from the LLM, invoke the correct tool with the correct arguments.
tool_response = tool_map[tool_1_name].invoke(tool_1_args)
tool_message = ToolMessage(content=tool_response, tool_call_id=tool_call_1_id)

print(tool_message)
chat_history.append(tool_message)

#As a final step, pass the entire chat_history into the LLM one more time to get a final response.
answer = llm_with_tools.invoke(chat_history)
print(type(answer))
print(answer.content)

print(f'######## Testing ###############')
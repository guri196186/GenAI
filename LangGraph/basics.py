import os
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.environ['OPENAI_API_KEY']
)

from typing import TypedDict, Optional

#States represent the current condition or context within a workflow
class AuthState(TypedDict):
    username: Optional[str] 
    password: Optional[str]
    is_authenticated: Optional[bool]
    output: Optional[str]
    

def input_node(state):
    print(state)
    if state.get('username', "") =="":
        username = input("What is your username?")

    password = input("Enter your password: ")
    
    if state.get('username', "") =="":
        return {"username":username, "password":password}
    else:
        return {"password": password}
    
def validate_credentials_node(state):
    # Extract username and password from the state
    username = state.get("username", "")
    password = state.get("password", "")

    print("Username :", username, "Password :", password)
    # Simulated credential validation
    if username == "test_user" and password == "secure_password":
        is_authenticated = True
    else:
        is_authenticated = False

    # Return the updated state with authentication result
    return {"is_authenticated": is_authenticated}
    
# Define the success node
def success_node(state):
    return {"output": "Authentication successful! Welcome."}

# Define the failure node
def failure_node(state):
    return {"output": "Not Successfull, please try again!"}

#The router node acts as a decision-making point in the workflow. It takes the current state 
# as input and determines the next node to execute based on the is_authenticated value in the state
def router(state):
    if state['is_authenticated']:
        return "success_node"
    else:
        return "failure_node"
    
from langgraph.graph import StateGraph
from langgraph.graph import END

# Create an instance of StateGraph with the GraphState structure
workflow = StateGraph(AuthState)

#add nodes to the graph
workflow.add_node("InputNode", input_node)
workflow.add_node("ValidateCredential", validate_credentials_node)
workflow.add_node("Success", success_node)
workflow.add_node("Failure", failure_node)

#Adding the Edge Between InputNode and ValidateCredential Node
workflow.add_edge("InputNode", "ValidateCredential")
#Adding the Edge Between Success Node and END
workflow.add_edge("Success", END)
#Adding the Edge Between Failure Node and InputNode
workflow.add_edge("Failure", "InputNode")

#Adding Conditional Edges from ValidateCredential Node to Success and Failure Nodes based on the is_authenticated value in the state
workflow.add_conditional_edges("ValidateCredential", router, {"success_node": "Success", "failure_node": "Failure"})

workflow.set_entry_point("InputNode")

app = workflow.compile()

inputs = {"username": "test_user"}
result = app.invoke(inputs)
print(result)
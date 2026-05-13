import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

_ = load_dotenv(find_dotenv()) 

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.environ['OPENAI_API_KEY']
) 

  
@tool 
def add_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and calculates their sum.

    Parameters:
    - inputs (str): A string containing numbers separated by spaces, commas, or other delimiters.

    Returns:
    - dict: A dictionary with the key "result" containing the sum of the numbers.

    Example Input:
    "1, 2, 3"

    Example Output:
    {"result": 6}

    Notes:
    - If no numbers are found, the result defaults to 0.
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]

    # If no numbers are found, return 0
    if not numbers:
        return {"result": 0}

    # Calculate the sum of the numbers
    result = sum(numbers)

    return {"result": result}
@tool
def subtract_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and performs subtraction sequentially, starting with the first number.

    This function is designed to handle input in string format, where numbers may be separated by spaces, 
    commas, or other delimiters. It parses the input string, extracts numeric values, and calculates 
    the result by subtracting each subsequent number from the first. inputs[0]-inputs[1]-inputs[2]

    Parameters:
    - inputs (str): 
      A string containing numbers to subtract. The string can include spaces, commas, or other 
      delimiters between the numbers.

    Returns:
    - dict: 
      A dictionary containing the key "result" with the calculated difference as its value. 
      If no valid numbers are found in the input string, the result defaults to 0.

    Example Usage:
    - Input: "100, 20, 10"
    - Output: {"result": 70}

    Limitations:
    - The function does not handle cases where numbers are formatted with decimals or other non-integer representations.
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]

    # If no numbers are found, return 0
    if not numbers:
        return {"result": 0}

    # Start with the first number
    result = numbers[0]

    # Subtract all subsequent numbers
    for num in numbers[1:]:
        result -= num

    return {"result": result}


# Multiplication Tool
@tool
def multiply_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and calculates their product.

    Parameters:
    - inputs (str): A string containing numbers separated by spaces, commas, or other delimiters.

    Returns:
    - dict: A dictionary with the key "result" containing the product of the numbers.

    Example Input:
    "2, 3, 4"

    Example Output:
    {"result": 24}

    Notes:
    - If no numbers are found, the result defaults to 1 (neutral element for multiplication).
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]
    #print(numbers)

    # If no numbers are found, return 1
    if not numbers:
        return {"result": 1}

    # Calculate the product of the numbers
    result = 1
    for num in numbers:
        result *= num
        ##print(num)

    return {"result": result}

# Division Tool
@tool
def divide_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and calculates the result of dividing the first number 
    by the subsequent numbers in sequence.

    Parameters:
    - inputs (str): A string containing numbers separated by spaces, commas, or other delimiters.

    Returns:
    - dict: A dictionary with the key "result" containing the quotient.

    Example Input:
    "100, 5, 2"

    Example Output:
    {"result": 10.0}

    Notes:
    - If no numbers are found, the result defaults to 0.
    - Division by zero will raise an error.
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]


    # If no numbers are found, return 0
    if not numbers:
        return {"result": 0}

    # Calculate the result of dividing the first number by subsequent numbers
    result = numbers[0]
    for num in numbers[1:]:
        result /= num

    return {"result": result}





# Test Cases
test_cases = [
    {
        "query": "Subtract 100, 20, and 10.",
        "expected": {"result": 70},
        "description": "Testing subtraction tool with sequential subtraction."
    },
    {
        "query": "Multiply 2, 3, and 4.",
        "expected": {"result": 24},
        "description": "Testing multiplication tool for a list of numbers."
    },
    {
        "query": "Divide 100 by 5 and then by 2.",
        "expected": {"result": 10.0},
        "description": "Testing division tool with sequential division."
    },
    {
        "query": "Subtract 50 from 20.",
        "expected": {"result": -30},
        "description": "Testing subtraction tool with negative results."
    }

]

def test_agent_with_cases(math_agent, test_cases):
    correct_tasks = []
    # Corrected test execution
    for index, test in enumerate(test_cases, start=1):
        query = test["query"]
        expected_result = test["expected"]["result"]  # Extract just the value
        
        print(f"\n--- Test Case {index}: {test['description']} ---")
        print(f"Query: {query}")
        
        # Properly format the input
        response = math_agent.invoke({"messages": [("human", query)]})
        
        # Find the tool message in the response
        tool_message = None
        for msg in response["messages"]:
            if hasattr(msg, 'name') and msg.name in ['add_numbers', 'subtract_numbers', 'multiply_numbers', 'divide_numbers']:
                tool_message = msg
                break
        
        if tool_message:
            # Parse the tool result from its content
            import json
            tool_result = json.loads(tool_message.content)["result"]
            print(f"Tool Result: {tool_result}")
            print(f"Expected Result: {expected_result}")
            
            if tool_result == expected_result:
                print(f"✅ Test Passed: {test['description']}")
                correct_tasks.append(test["description"])
            else:
                print(f"❌ Test Failed: {test['description']}")
        else:
            print("❌ No tool was called by the agent")

    print("\nCorrectly passed tests:", correct_tasks)



from langchain_community.utilities import WikipediaAPIWrapper


@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for factual information about a topic.
    
    Parameters:
    - query (str): The topic or question to search for on Wikipedia
    
    Returns:
    - str: A summary of relevant information from Wikipedia
    """
    wiki = WikipediaAPIWrapper()
    return wiki.run(query)
#search_wikipedia.invoke("What is the male vs female population of Bihar")


if __name__ == "__main__":
    
    tools = [add_numbers,subtract_numbers, multiply_numbers, divide_numbers, search_wikipedia]

    # Create the agent with all tools
    math_agent = create_react_agent(
        model=llm,
        tools=tools,
        # Optional: Add a system message to guide the agent's behavior
        prompt="You are a helpful mathematical assistant that can perform various mathematical operations and look up information. Use the tools precisely and explain your reasoning clearly."
    )
    
    print("\n--- Testing DivideTool ---")
    response = math_agent.invoke({
        "messages": [("human", "What is 25 divided by 4?")]
    })

    # Get the final answer
    final_answer = response["messages"][-1].content
    print(final_answer)

    print("\n--- Testing MultiplyTool ---")
    response = math_agent.invoke({
        "messages": [("human", "Multiply 2, 3, and four.")]
    })
    print("Agent Response:", response["messages"][-1].content)

    print("\n--- Testing DivideTool ---")
    response = math_agent.invoke({
        "messages": [("human", "Divide 100 by 5 and then by 2.")]
    })
    print("Agent Response:", response["messages"][-1].content)

    print("\n--- Testing SubtractTool ---")
    response_2 = math_agent.invoke({
        "messages": [("human", "Subtract 100, 20, and 10.")]
    })

    # Get the final answer
    final_answer_2 = response_2["messages"][-2].content
    print(final_answer_2)
    
    test_agent_with_cases(math_agent, test_cases)
    
    query = "What is the population of Canada? Multiply it by 0.75"

    response = math_agent.invoke({"messages": [("human", query)]})

    print("\nMessage sequence:")
    for i, msg in enumerate(response["messages"]):
        print(f"\n--- Message {i+1} ---")
        print(f"Type: {type(msg).__name__}")
        if hasattr(msg, 'content'):
            print(f"Content: {msg.content}")
        if hasattr(msg, 'name'):
            print(f"Name: {msg.name}")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"Tool calls: {msg.tool_calls}")
    
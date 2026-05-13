import os
from langchain.agents import Tool
from langchain_core.tools import tool
import re


def add_numbers(inputs:str) ->dict:
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    result = sum(numbers)
    return {"result": result}

# print(add_numbers("1 2") )

#converting regular Python functions into agent-compatible tools
add_tool=Tool(
        name="AddTool",
        func=add_numbers,
        description="Adds a list of numbers and returns the result.")

# print("tool object",add_tool)

# # Tool name
# print("Tool Name:")
# print(add_tool.name)

# # Tool description
# print("Tool Description:")
# print(add_tool.description)

# # Tool function
# print("Tool Function:")
# print(add_tool.invoke)

# print("Calling Tool Function:")
# test_input = "10 20 30 a b" 
# print(add_tool.invoke(test_input))



@tool 
def add_numbers_v2(inputs:str) ->dict:
    """
    Adds a list of numbers provided in the input string.
    Parameters:
    - inputs (str): 
    string, it should contain numbers that can be extracted and summed.
    Returns:
    - dict: A dictionary with a single key "result" containing the sum of the numbers.
    Example Input:
    "Add the numbers 10, 20, and 30."
    Example Output:
    {"result": 60}
    """
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    result = sum(numbers)
    return {"result": result}

# print("Name: \n", add_numbers.name)
# print("Description: \n", add_numbers.description) 
# print("Args: \n", add_numbers.args) 

# test_input = "what is the sum between 10, 20 and 30 " 
# print(add_numbers_v2.invoke(test_input))

from typing import List
@tool
def add_numbers_with_options(inputs:List[float], absolute:bool=False) -> float:
    """
    Adds a list of numbers provided as input.

    Parameters:
    - numbers (List[float]): A list of numbers to be summed.
    - absolute (bool): If True, use the absolute values of the numbers before summing.

    Returns:
    - float: The total sum of the numbers.
    """
    if absolute:
        inputs = [abs(x) for x in inputs]
    return sum(inputs)
    

# print(f"Args Schema Info: {add_numbers_with_options.args}")
# print(f"Args Schema Info: {add_numbers.args}")


# print(add_numbers_with_options.invoke({"inputs": [10, -20, 30], "absolute": True}))
# print(add_numbers_with_options.invoke({"inputs":[-1.1,-2.1,-3.0],"absolute":False}))
# print(add_numbers_with_options.invoke({"inputs":[-1.1,-2.1,-3.0],"absolute":True}))


from typing import Dict, Union

@tool
def sum_numbers_with_complex_output(inputs: str) -> Dict[str, Union[float, str]]:
    """
    Extracts and sums all integers and decimal numbers from the input string.

    Parameters:
    - inputs (str): A string that may contain numeric values.

    Returns:
    - dict: A dictionary with the key "result". If numbers are found, the value is their sum (float). 
            If no numbers are found or an error occurs, the value is a corresponding message (str).

    Example Input:
    "Add 10, 20.5, and -3."

    Example Output:
    {"result": 27.5}
    """
    matches = re.findall(r'-?\d+(?:\.\d+)?', inputs)
    if not matches:
        return {"result": "No numbers found in input."}
    try:
        numbers = [float(num) for num in matches]
        total = sum(numbers)
        return {"result": total}
    except Exception as e:
        return {"result": f"Error during summation: {str(e)}"}
    
# print(sum_numbers_with_complex_output.invoke("Add 10, 20.5, and -3."))
# print(sum_numbers_with_complex_output.invoke("No numbers here!"))
# print(sum_numbers_with_complex_output.invoke("Add 10, 20.5, and -3, and also 5.5."))

@tool
def sum_numbers_from_text(inputs: str) -> float:
    """
    Adds a list of numbers provided in the input string.
    
    Args:
        text: A string containing numbers that should be extracted and summed.
        
    Returns:
        The sum of all numbers found in the input.
    """
    # Use regular expressions to extract all numbers from the input
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    result = sum(numbers)
    return result
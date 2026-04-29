Summary
1. Principles:- 
    a. Write clear and specific instructions
    b. Give the model time to think
2. Iterative Prompt development 
3. Capabilities 
    a. Summarizing 
    b. Inferring
    c. Tranforming
    g. Expanding 
4. Built a chatbot
##############################
I9: Using LangChain Expression Language (LCEL) pattern using the pipe operator | for flexible composition
I10: In this role, the LLM answers questions about games while maintaining an engaging and immersive tone, enhancing the user experience.


In addition to prompt formatting, we need to understand the concept of roles (to be enclosed within the <|start_header_id|> and <|end_header_id|> tags). In Llama, there are 4 roles.

System: Specifies the behavior, context, or personality of the assistant. It sets guidelines or instructions that shape how the assistant interacts, responds, and helps users. This can include the tone, formality, and any background knowledge needed to better assist.

User: Represents the person interacting with the assistant. This role contains the queries, requests, or commands made by the user. For example, if the user asks, “What is the capital of France?”, the assistant will generate a relevant response based on this input.

Assistant: This is where the AI-generated response is provided. Based on the user’s input and the system’s instructions, the assistant crafts a reply here that meets the user’s needs.

iPython: A new role introduced in Llama 3.1. This role is used to mark messages with the output of a tool call when sent back to the model from the executor. We won't be using this role here.

####################################################

Gradio - Gradio simplifies the process of building interactive web demos for machine learning models. By integrating Gradio with models like BLIP for image captioning, you can create practical, user-friendly applications that leverage the power of AI to solve real-world problems. This tool not only aids in demonstrating the capabilities of your models but also in collecting valuable feedback for further improvement.

######################################################
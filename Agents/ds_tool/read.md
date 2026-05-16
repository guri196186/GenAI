Dataset caching tool
As you build more complex tools, you need to efficiently manage datasets in memory. Since language models communicate via text, sending entire datasets in each response would waste tokens and context window space. To solve this, you'll create a global cache that stores DataFrames after they're first loaded. This approach has several benefits:

Reduces token usage by referencing datasets by name rather than content
Improves performance by loading data only once
Maintains dataset availability between different tool calls
The following tool allows the agent to preload datasets into this cache system


You may think that the global keyword would work effectively instead of DATAFRAME CACHE, but when using functions in Python with LangChain agents, simply writing the keyword global isn't enough to maintain data between different tool calls. This is because each time the agent runs a tool, it might do so in a separate execution environment, causing any global variables to reset. Instead, using a module-level dictionary (DATAFRAME_CACHE) that lives outside any function creates a persistent storage space that all tools can access without explicitly passing it around. This approach works reliably across multiple function calls, even when they happen in different contexts, and keeps the function interfaces clean by avoiding the need to pass the cache as an additional parameter to every tool.

Well-structured docstrings are essential for your LLM-based tools because they serve as instructions for the AI agent. The agent relies on these descriptions to understand when and how to use each tool. Similarly, formatted outputs help the agent parse and interpret results properly. Always ensure your tool functions have clear docstrings and return well-structured outputs that are easy for both humans and AI to understand.

Agent executor ReAct
Managing this ReAct loop manually can be cumbersome, which is why you'll use the AgentExecutor. The AgentExecutor wraps the agent and the toolset, and handles the full tool-use loop behind the scenes. It automatically runs the agent, executes the selected tool, takes the result (observation), and feeds it back into the agent until a final answer is reached. Without the executor, you'd have to manually manage every step, including checking whether the agent returned a tool call or a final answer, running the tool, and tracking the intermediate steps—all of which the executor handles for you.
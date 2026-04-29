import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama
#from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
from pydantic import BaseModel, Field

_ = load_dotenv(find_dotenv()) # read local .env file

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.environ['OPENAI_API_KEY']
)

#llm = OllamaLLM(model="deepseek-r1:1.5b", base_url="http://localhost:11434")


def summarize_text(text):
    prompt = ChatPromptTemplate.from_template(
        "Summarize the following text in 3 bullet points:\n\n{text}"
    )
    parser = StrOutputParser()
    chain = prompt | llm | parser
    result = chain.invoke({"text": text})
    return result


def joke_json(text):
    class Joke(BaseModel):
        setup: str = Field(description="question to set up a joke")
        punchline: str = Field(description="answer to resolve the joke")
    
    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Joke)

    # Get the formatting instructions for the output parser
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_template(
        "Answer the user query.\n{format_instructions}\n{text}\n"
    ).partial(format_instructions=format_instructions)
    
    chain = prompt | llm | parser
    result = chain.invoke({"text": text})
    return result

def icecream_flavors_csv(text):
    parser = CommaSeparatedListOutputParser()
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_template(
        "List 5 popular ice cream flavors.\n{format_instructions}\n{text}\n"
    ).partial(format_instructions=format_instructions)

    chain = prompt | llm | parser
    result = chain.invoke({"text": text})
    return result


if __name__ == "__main__":
    input_text = """Large pre-trained language models have been shown to store factual knowledge
    in their parameters, and achieve state-of-the-art results when fine-tuned on downstream
    NLP tasks. However, their ability to access and precisely manipulate knowledge
    is still limited, and hence on knowledge-intensive tasks, their performance
    lags behind task-specific architectures. Additionally, providing provenance for their
    decisions and updating their world knowledge remain open research problems. Pretrained
    models with a differentiable access mechanism to explicit non-parametric
    memory have so far been only investigated for extractive downstream tasks. We
    explore a general-purpose fine-tuning recipe for retrieval-augmented generation
    (RAG) — models which combine pre-trained parametric and non-parametric memory
    for language generation. We introduce RAG models where the parametric
    memory is a pre-trained seq2seq model and the non-parametric memory is a dense
    vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare
    two RAG formulations, one which conditions on the same retrieved passages
    across the whole generated sequence, and another which can use different passages
    per token. We fine-tune and evaluate our models on a wide range of knowledgeintensive
    NLP tasks and set the state of the art on three open domain QA tasks,
    outperforming parametric seq2seq models and task-specific retrieve-and-extract
    architectures. For language generation tasks, we find that RAG models generate
    more specific, diverse and factual language than a state-of-the-art parametric-only
    seq2seq baseline."""
    
    # result = summarize_text(input_text)
    # print(result)
    
    # result = joke_json("Tell me a joke about Dogs.")
    # print(result)
    
    result = icecream_flavors_csv("What are some popular ice cream flavors?")
    print(result)
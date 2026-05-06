import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

_ = load_dotenv(find_dotenv()) # read local .env file

def get_llm():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.environ['OPENAI_API_KEY']
    )
    return llm

def pdf_loader(file):
    loader = PyPDFLoader(file.name)
    pages = loader.load_and_split()
    return pages

def text_splitter(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len)
    chunks = text_splitter.split_documents(text)
    return chunks

def vector_store(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    vector_db = Chroma.from_documents(chunks, embeddings)
    return vector_db

# def retrieve_relevant_docs(vector_store, query):
#     relevant_docs = vector_store.similarity_search(query)
#     return relevant_docs


def retriever(file):
    pages = pdf_loader(file)
    chunks = text_splitter(pages)
    vector_db = vector_store(chunks)
    return vector_db.as_retriever()
    
# The retriever object internally uses vector similarity search (via Chroma) to find the most relevant document chunks based on the query embedding.
def retriever_qa(file, query):
    llm = get_llm()
    retriever_obj = retriever(file)
    qa = RetrievalQA.from_chain_type(llm=llm, 
                                    chain_type="stuff", 
                                    retriever=retriever_obj, 
                                    return_source_documents=False)
    response = qa.invoke(query)
    return response['result']
    


# Gradio interface
rag_application = gr.Interface(
    fn=retriever_qa,
    allow_flagging="never",
    inputs=[
        gr.File(label="Upload PDF File", file_count="single", file_types=['.pdf'], type="filepath"),
        gr.Textbox(label="Input Query", lines=2, placeholder="Type your question here...")
    ],
    outputs=gr.Textbox(label="Output"),
    title="RAG Chatbot",
    description="Upload a PDF document and ask any question. The chatbot will try to answer using the provided document."
)

rag_application.launch(server_name="127.0.0.1", server_port=7860)
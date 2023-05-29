import langchain
import os
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from fastapi import UploadFile
from decouple import config

os.environ["OPEN_API_KEY"] = config("OPEN_API_KEY")

def chat_on_file(message: str, file: UploadFile):
    print(f'chat_on_file => Message: {message}')
    loader = UnstructuredFileLoader(file)
    print(f'After loader')
    documents= loader.load()

    print(f'After loading')

    # if you want to load file as a list of elements then only do this
    loader = UnstructuredFileLoader('SamplePDF.pdf', mode='elements')

    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key = os.environ["OPEN_API_KEY"])
    doc_search = Chroma.from_documents(texts,embeddings)
    chain = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=doc_search)

    query = "What are the effects of homelessness?"
    print(chain.run(query))

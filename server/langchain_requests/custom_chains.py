import os
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from decouple import config
from dotenv import load_dotenv
import openai


os.environ["OPENAI_API_KEY"] = config("OPEN_API_KEY")
# os.environ["OPEN_API_KEY"] = config("OPEN_API_KEY")
# load_dotenv()
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_creative = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")


def get_summary_chain(input_message: str):
    messages = [
        SystemMessage(content="You are a useful agent and answer to the human messages"),
        HumanMessage(content=input_message)
    ]

    response = llm_creative(messages)

    return response.content

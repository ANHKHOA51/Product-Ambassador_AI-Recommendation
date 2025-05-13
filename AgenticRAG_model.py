from langchain_community.chat_models import ChatLiteLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.chains import create_retrieval_chain
import os

class KOL(BaseModel):
    id: str = Field(description="id of influencers")
    name: str = Field(description="Name of influencers")
    location: str = Field(description="Location of influencers, copy from source")
    description: str = Field(description="Description of influencers, copy from source")
    characteristic: str = Field(description="Characteristic of influencers, copy from source")
    field: str = Field(description="Field of influencers, copy from source")
    platform: str = Field(description="Platform of influencers, which platform and how many count, copy exactly all from source")
    reason: str = Field(description="Reason why chose this influencers")

parser = JsonOutputParser(pydantic_object=KOL)

prompt = PromptTemplate(
            template="Base on context, find at least three people satisfy user query. If there is no one, just return null, avoid make up.\n{format_instructions}\n{context}\n{input}\n",
            input_variables=["input", "context"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

def find_ambassador(retriever, query):
    model = ChatLiteLLM(
                model="openrouter/deepseek/deepseek-r1-distill-llama-70b",
                api_base="https://openrouter.ai/api/v1",
                api_key=os.getenv('AGENT'),
                temperature=0
            )
    parser = JsonOutputParser(pydantic_object=KOL)

    chain = prompt | model | parser
    chain_2 = create_retrieval_chain(retriever, chain)

    return chain_2.invoke({"input": query})['answer']
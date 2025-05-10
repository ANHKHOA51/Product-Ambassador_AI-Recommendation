from langchain_community.chat_models import ChatLiteLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from data import fetch_data
import os
import json

class Info(BaseModel):
    name: str = Field(description="Name of product")
    description: str = Field(description="At least 5 adjectives or messages to describe the type of customer that would buy this products. These adjectives and messages are implied from the description of product")
    target_customer: str = Field(description="Predict suitable customers for this product")
    price: str = Field(description="Price of product. The currency is VND")
    slogan_1: str = Field(description="Make slogan for product marketing")
    slogan_2: str = Field(description="Another slogan for product marketing")
    slogan_3: str = Field(description="Another slogan for product marketing")


def retrieve_product(id):
    product_DB = os.getenv("product_DB")
    url = product_DB + id + "?fields=id,name,brand,description,price,fabric,features,category"
    data = fetch_data(url)

    if data is None:
        raise Exception("Fetch data failed")
    else:
        model = ChatLiteLLM(
            model="openrouter/deepseek/deepseek-r1-distill-llama-70b",
            api_base="https://openrouter.ai/api/v1",
            api_key=os.getenv('AGENT'),
            temperature=0
        )

        user_query = "Extract info from this data: " + json.dumps(data, ensure_ascii=True)

        parser = JsonOutputParser(pydantic_object=Info)

        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        return chain.invoke({"query": user_query})

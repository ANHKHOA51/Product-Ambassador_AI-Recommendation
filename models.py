from smolagents import Tool, LiteLLMModel, DuckDuckGoSearchTool, CodeAgent
from langchain_community.retrievers import BM25Retriever
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from data import fetch_data
import os
from dotenv import load_dotenv
import json

load_dotenv()

# class SuitableAmbassadorRetrieverTool(Tool):
#     name = "suitable_ambassador_retriever"
#     description = "Retrieves information about KOLs who is most suitable for given details of a product (compare KOLs characteristics with the messages of the product, the related field of KOLs with product, compatibiity between Media, Target customer and Price wỉth the one of the prompt if required)"
#     inputs = {
#         "query": {
#             "type": "string",
#             "description": "The detailed description about the product to compare with all the KOLs to find the most suitable ambassador"
#         }
#     }
#     output_type = "string"

#     def __init__(self, docs):
#         self.is_initialized = False
#         self.retriever = BM25Retriever.from_documents(docs)

#     def forward(self, query: str):
#           results = self.retriever.get_relevant_documents(query)
#           if results:
#             answer = "\n\n".join([doc.page_content["name"] for doc in results[:3]])
#             return f"{answer}"
#           else:
#             return "No suitable KOLs found"
          
model = LiteLLMModel(
    model_id='openrouter/qwen/qwen2.5-vl-32b-instruct:free',
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv('AGENT'),
    flatten_messages_as_text=True,
    temperature=0,
)

def get_agent() -> CodeAgent:
    agent = CodeAgent(
        model = model,
        tools= [find],
        planning_interval=3,
    )
    agent.prompt_templates["final_answer"]["post_messages"] = "Based on the above, please provide directly answer, no extra sentences to the following user task:\n{{task}}"

    return agent

class Info(BaseModel):
    name: str = Field(description="Name of product")
    description: str = Field(description="At least 5 adjectives or messages to describe the products implied from the description of product")
    target_customer: str = Field(description="Predict suitable customers for this product")
    price: str = Field(description="Price of product")
    slogan_1: str = Field(description="Make slogan for product marketing")
    slogan_2: str = Field(description="Another slogan for product marketing")
    slogan_3: str = Field(description="Another slogan for product marketing")


def retrieve_product(id):
    data = fetch_data(id)

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
        
# find = SuitableAmbassadorRetrieverTool(docs)
search = DuckDuckGoSearchTool()

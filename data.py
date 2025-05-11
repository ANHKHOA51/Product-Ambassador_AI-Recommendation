from langchain.docstore.document import Document
import requests
import os

def fetch_data(url: str):
    data = requests.get(url)

    if data.status_code == 200:
        return data.json()
    else:
        return None

def create_doc():
    url = os.getenv("influencer_DB") + "influencer"
    kols = fetch_data(url)

    if kols == None:
        raise Exception("Fetch data failed")
    else:
        docs = [
            Document (
                page_content="\n".join([
                    f"id: {kol['id']}",
                    f"name: {kol['name']}",
                    f"location: {kol['location']}",
                    f"description: {kol['description']}",
                    f"characteristic: {kol['characteristic']}",
                    f"field: {kol['field']}",
                    f"platform: {kol['platform']}",
                ]),
                metadata={
                    "description": kol["description"],
                    "field": kol["field"],
                    "characteristic": kol["characteristic"]}
            )
            for kol in kols
            ]
        
        return docs
    

# def create_doc():
#     url = os.getenv("influencer_DB") + "influencer"
#     kols = fetch_data(url)

#     if kols == None:
#         raise Exception("Fetch data failed")
#     else:
#         docs = []
#         embedding = []
#         for kol in kols:

#             docs.append(
#                 Document (
#                     page_content="\n".join([
#                         f"id: {kol['id']}",
#                         f"name: {kol['name']}",
#                         f"location: {kol['location']}",
#                         f"description: {kol['description']}",
#                         f"characteristic: {kol['characteristic']}",
#                         f"field: {kol['field']}",
#                         f"platform: {kol['platform']}",
#                     ]),
#                     metadata={
#                         "description": kol["description"],
#                         "field": kol["field"],
#                         "characteristic": kol["characteristic"]}
#                 )
#             )
            
#             embedding.append(kol["description_vector"])

#         return docs, embedding
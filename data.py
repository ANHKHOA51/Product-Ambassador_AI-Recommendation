# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from langchain.docstore.document import Document
import requests
from dotenv import load_dotenv
import os
# # Thiết lập quyền truy cập
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
# client = gspread.authorize(creds)

# # Mở sheet bằng URL hoặc tên
# sheet = client.open("KOLs_Dataset").sheet1

# # Lấy toàn bộ dữ liệu
# data = sheet.get_all_records()

# docs = [
#     Document (
#         page_content="\n".join([
#             f"Name: {kol['KOLs']}",
#             f"Medias: {kol['Medias']}",
#             f"Fields: {kol['Fields']}",
#             f"Characteristic: {kol['Characteristic']}",
#             f"Target: {kol['Target']}",
#             f"Price: {kol['Price']}",
#         ]),
#         metadata={"name": kol["KOLs"]}
#     )
#     for kol in data
#     ]

load_dotenv()

product_DB = os.getenv("product_DB")

def fetch_data(id):
    url = product_DB + id + "?fields=id,name,brand,description,price,fabric,features,category"
    data = requests.get(url)

    if data.status_code == 200:
        return data.json()
    else:
        return None
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from langchain.docstore.document import Document
import requests

# Thiết lập quyền truy cập
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Mở sheet bằng URL hoặc tên
sheet = client.open("KOLs_Dataset").sheet1

# Lấy toàn bộ dữ liệu
data = sheet.get_all_records()
# for row in data:
#         print(row)


docs = [
    Document (
        page_content="\n".join([
            f"Name: {kol['KOLs']}",
            f"Medias: {kol['Medias']}",
            f"Fields: {kol['Fields']}",
            f"Characteristic: {kol['Characteristic']}",
            f"Target: {kol['Target']}",
            f"Price: {kol['Price']}",
        ]),
        metadata={"name": kol["KOLs"]}
    )
    for kol in data
    ]

product_DB = "https://backend-vitonweb.onrender.com/api/v4/product/"

def fetch_data(id):
    url = product_DB + id + "?fields=id,name,brand,description,price,fabric,features,category"
    data = requests.get(url)

    if data.status_code == 200:
        return data.json()
    else:
        return None
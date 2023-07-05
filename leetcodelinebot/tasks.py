import requests
import time
from pymongo import MongoClient
import requests

# https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=Z1oeGU1ZW8BmBsCoWbOCBt&redirect_uri=https://tasktrackbot-amisleo000.b4a.run/notify&scope=notify&state=abcd

# 設定請求端點 URL
url = "https://notify-bot.line.me/oauth/token"

# 設定請求參數
params = {
    "grant_type": "authorization_code",
    "code": "3NJT81LkkDVjOzb57A8Upk",
    "redirect_uri": "https://tasktrackbot-amisleo000.b4a.run/notify",
    "client_id": "Z1oeGU1ZW8BmBsCoWbOCBt",
    "client_secret": "I12XId2drh03mRHo1sGsStyvNAuqZwH3sPU9lQax88c"
}

# 發送 POST 請求
response = requests.post(url, data=params)

# 檢查回應狀態碼
if response.status_code == 200:
    # 解析回應 JSON
    data = response.json()
    access_token = data.get("access_token")
    print("Access Token:", access_token)
else:
    print("Request failed with status code:", response.status_code)

# def send_line_message(message):
#     url = "https://notify-api.line.me/api/notify"
#     headers = {
#         "Authorization": "Bearer " + '3t3o0JGWlcQfcv21kc4IBdM6uyyPlVhBSgxQOZTFNUM',
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     params = {
#         'message': message
#     }
#     response = requests.post(url, headers=headers, params=params)
#     if response.status_code == 200:
#         print("Line message sent successfully.")
#     else:
#         print("Failed to send Line message.")

# # 连接到MongoDB数据库
# client = MongoClient("mongodb+srv://amisleo000:AMISleo123@cluster0.3dwwur1.mongodb.net")

# # 选择数据库和集合
# db = client["linebot"]
# collection = db["ReportLog"]

# while True:
#     # 从MongoDB读取数据
#     data = collection.find()
#     for document in data:
#         # 获取需要发送的消息内容
#         message = document['name']
#         # 发送Line消息
#         send_line_message(message)
#     time.sleep(20)
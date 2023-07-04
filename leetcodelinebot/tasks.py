import time
from pymongo import MongoClient
import requests

def send_line_message(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + '3t3o0JGWlcQfcv21kc4IBdM6uyyPlVhBSgxQOZTFNUM',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        'message': message
    }
    response = requests.post(url, headers=headers, params=params)
    if response.status_code == 200:
        print("Line message sent successfully.")
    else:
        print("Failed to send Line message.")

# 连接到MongoDB数据库
client = MongoClient("mongodb+srv://amisleo000:AMISleo123@cluster0.3dwwur1.mongodb.net")

# 选择数据库和集合
db = client["linebot"]
collection = db["ReportLog"]

while True:
    # 从MongoDB读取数据
    data = collection.find()
    for document in data:
        # 获取需要发送的消息内容
        message = document['name']
        # 发送Line消息
        send_line_message(message)
    time.sleep(20)
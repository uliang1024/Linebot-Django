import requests

# LINE Notify 權杖
token = 'q3KwMlbfH3Upxw7FiaYlaopFyJwlHK3tKnOuLnaGhmI'

# 要發送的訊息
message = '喔是喔'

# HTTP 標頭參數與資料
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }

# 远程图片的 URL
image_url = 'https://img.onl/LSQpWr'

# 发送 HTTP GET 请求获取图片内容
response = requests.get(image_url)

# 获取图片的二进制内容
image_content = response.content

# 将图片内容作为文件发送
files = {'imageFile': image_content}

# 以 requests 發送 POST 請求
requests.post("https://notify-api.line.me/api/notify",
    headers = headers, data = data, files = files)
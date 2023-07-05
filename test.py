import requests

# LINE Notify 權杖
token = 'j6CgXLdrQZKfZRmhWG58cqLyBm13rjsR0GaI2Hz7oxU'

# 要發送的訊息
message = '你朋友怪怪的'

# HTTP 標頭參數與資料
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }

# 远程图片的 URL
image_url = 'https://img.onl/OeBvA4'

# 发送 HTTP GET 请求获取图片内容
response = requests.get(image_url)

# 获取图片的二进制内容
image_content = response.content

# 将图片内容作为文件发送
files = {'imageFile': image_content}

# 以 requests 發送 POST 請求
requests.post("https://notify-api.line.me/api/notify",
    headers = headers, data = data)
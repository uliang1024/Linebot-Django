import requests

# LINE Notify 權杖
token = 'MoiWUt97xCLpZTuTVeNvP5kFp3rvVcGS2PFLmfSwMyi'

# 要發送的訊息
message = '嗨'

# HTTP 標頭參數與資料
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }

# 远程图片的 URL
image_url = 'https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcQkrjYxSfSHeCEA7hkPy8e2JphDsfFHZVKqx-3t37E4XKr-AT7DML8IwtwY0TnZsUcQ'

# 发送 HTTP GET 请求获取图片内容
response = requests.get(image_url)

# 获取图片的二进制内容
image_content = response.content

# 将图片内容作为文件发送
files = {'imageFile': image_content}

# 以 requests 發送 POST 請求
requests.post("https://notify-api.line.me/api/notify",
    headers = headers, data = data, files = files)
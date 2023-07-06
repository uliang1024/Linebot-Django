import requests
import requests

# https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=Z1oeGU1ZW8BmBsCoWbOCBt&redirect_uri=https://tasktrackbot-amisleo000.b4a.run/notify&scope=notify&state=abcd

url = "https://notify-bot.line.me/oauth/token"

params = {
    "grant_type": "authorization_code",
    "code": "150t9PYPH7KGpoJLjoFdo2",
    "redirect_uri": "https://tasktrackbot-amisleo000.b4a.run/notify",
    "client_id": "Z1oeGU1ZW8BmBsCoWbOCBt",
    "client_secret": "I12XId2drh03mRHo1sGsStyvNAuqZwH3sPU9lQax88c"
}

response = requests.post(url, data=params)

if response.status_code == 200:
    data = response.json()
    access_token = data.get("access_token")
    print("Access Token:", access_token)
else:
    print("Request failed with status code:", response.status_code)

# def send_line_message(message):
#     url = "https://notify-api.line.me/api/notify"
#     headers = {
#         "Authorization": "Bearer " + 'MoiWUt97xCLpZTuTVeNvP5kFp3rvVcGS2PFLmfSwMyi',
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
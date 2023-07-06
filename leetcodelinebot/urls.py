from django.urls import path
from . import views

import requests

app_name = 'leetcodelinebot'

urlpatterns = [
    path('callback/', views.callback, name='callback'),
]

def send_line_message(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + 'MoiWUt97xCLpZTuTVeNvP5kFp3rvVcGS2PFLmfSwMyi',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        'message': message
    }
    response = requests.post(url, headers=headers, params=params)
    if response.status_code == 200:
        print("Line message sent successfully.")
    else:
        print("Failed to send Line message." + response.status_code)
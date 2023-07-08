import requests

def line_notify_send_message(message):
    requests.post("https://notify-api.line.me/api/notify",
        headers = { "Authorization": "Bearer " + 'q3KwMlbfH3Upxw7FiaYlaopFyJwlHK3tKnOuLnaGhmI' }, 
        data = { 'message': message })
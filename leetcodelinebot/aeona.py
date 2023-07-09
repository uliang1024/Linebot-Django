import requests

url = "https://aeona3.p.rapidapi.com/"

def AI_chatbot(message):

    querystring = {"text":message,"userId":"12312312312"}

    headers = {
    	"X-RapidAPI-Key": "f0ae3b340fmshc395d66132bea31p1e0f64jsn748879f3a85d",
    	"X-RapidAPI-Host": "aeona3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
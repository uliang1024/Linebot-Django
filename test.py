import requests

requests.post("https://notify-api.line.me/api/notify", 
                  headers = {"Authorization": "Bearer " + '3t3o0JGWlcQfcv21kc4IBdM6uyyPlVhBSgxQOZTFNUM', 
                             "Content-Type" : "application/x-www-form-urlencoded"}, 
                  params = {'message': '別再混了 !'})
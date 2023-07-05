import requests

requests.post("https://notify-api.line.me/api/notify", 
                  headers = {"Authorization": "Bearer " + 'BuiLxcTrO3CXKILS5eeuVFouuLRn8fk47V6qJfsEkcw', 
                             "Content-Type" : "application/x-www-form-urlencoded"}, 
                  params = {'message': '小胖子 !'})
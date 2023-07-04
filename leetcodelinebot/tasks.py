from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

import requests

def my_task():
    requests.post("https://notify-api.line.me/api/notify", 
                  headers = {"Authorization": "Bearer " + '3t3o0JGWlcQfcv21kc4IBdM6uyyPlVhBSgxQOZTFNUM', 
                             "Content-Type" : "application/x-www-form-urlencoded"}, 
                  params = {'message': '別再混了 !'})
    
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# 注册定时任务，每分钟执行一次
scheduler.add_job(my_task, "interval", minutes=1)

# 启动任务调度器
scheduler.start()
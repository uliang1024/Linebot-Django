from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, JoinEvent, FollowEvent, MemberJoinedEvent

from leetcodelinebot.models import Users, ReportLog, write_to_report_log, get_report_stats, extract_topic_from_message, settlement_event, reminder_event, report_event

import datetime
from pytz import timezone

import requests

from apscheduler.schedulers.blocking import BlockingScheduler

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


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

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            # if isinstance(event, JoinEvent):  # 如果有加入聊天室的事件
            #     group_id = event.source.group_id  # 群組ID
            #     user_ids = line_bot_api.get_group_member_ids(group_id)  # 取得群組內使用者ID列表
            #     # 將每個使用者ID新增至MongoDB的UsersCollection
            #     for user_id in user_ids:
            #         profile = line_bot_api.get_profile(user_id)
            #         user = Users(
            #             user_id = user_id,
            #             display_name = profile.display_name,
            #             status_message = profile.status_message,
            #             picture_url = profile.picture_url,
            #             # 其他使用者相關的欄位值
            #         )
            #         user.save()  # 將使用者物件保存至MongoDB的UsersCollection

            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         TextSendMessage(text='大家好，我是Line bot！\n請將我加為好友才能為你服務！')  # 聊天室歡迎訊息
            #     )
            # elif isinstance(event, FollowEvent):  # 如果是加好友事件
            #     user_id = event.source.user_id
            #     profile = line_bot_api.get_profile(user_id)

            #     # 更新使用者資訊
            #     user = Users.objects(user_id=user_id).first()
            #     if user:
            #         user.display_name = profile.display_name
            #         user.status_message = profile.status_message
            #         user.picture_url = profile.picture_url
            #         user.save()
                
            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         TextSendMessage(text='有人偷偷加我好友')  # 聊天室歡迎訊息
            #     )
            # elif isinstance(event, MemberJoinedEvent):  # 如果是新的使用者加入群組事件
            #     user_id = event.joined.members[0].user_id  # 取得新加入使用者的 ID
            #     profile = line_bot_api.get_profile(user_id)

            #     # 儲存使用者資訊到資料庫
            #     user = Users(
            #         user_id=user_id,
            #         display_name=profile.display_name,
            #         status_message=profile.status_message,
            #         picture_url=profile.picture_url,
            #         punish=0
            #     )
            #     user.save()
            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         TextSendMessage(text='歡迎歡迎新朋友')  # 聊天室歡迎訊息
            #     )
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == '查詢紀錄':
                    user_id = event.source.user_id
                    reply_text = get_report_stats(user_id)  # 呼叫函式取得 ReportLog 統計數據
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)  # 構建回覆訊息
                    )
                elif event.message.text is not None and event.message.text.startswith('完成'):
                    topic = extract_topic_from_message(event.message.text)
                    if topic is not None:
                        # 建立 ReportLog 物件並保存到資料庫
                        user_id = event.source.user_id
                        profile = line_bot_api.get_profile(user_id)
                        reply_text = write_to_report_log(user_id=event.source.user_id, name=profile.display_name, topic=topic, done=True)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=reply_text)  # 回覆新增成功訊息
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='未提取到數字，舉例:[完成 1]')  # 回覆未提取到數字訊息
                        )
                elif event.message.text == '測試':
                    textHey = settlement_event()
                    send_line_message(textHey)
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# 创建一个调度器对象
scheduler = BlockingScheduler()

# 设置台湾时区
taipei_tz = timezone('Asia/Taipei')

def settlement_event():
    # 早上八點的結算事件
    # 取得台灣時區
    taiwan_tz = timezone('Asia/Taipei')
    # 取得過去24小時的起始時間和結束時間
    start_time = datetime.now(taiwan_tz) - timedelta(hours=24)
    end_time = datetime.now(taiwan_tz)
    
    # 查詢過去24小時內完成題目的使用者和題目數量
    result = ReportLog.objects(created_at__gte=start_time, created_at__lt=end_time).aggregate([
        {"$group": {"_id": "$name", "count": {"$sum": 1}}}
    ])
    
    reply_text = "📢📢📢結算學員完成題數\n"
    reply_text += "⬇️⬇️過去24小時中⬇️⬇️\n"
    reply_text += "-----------------------------\n"
    
    for entry in result:
        user_id = entry["_id"]
        count = entry["count"]
        
        # 構建回覆訊息
        reply_text += f"{user_id}：{count} 題\n"
        
    reply_text += "-----------------------------\n"
    reply_text += '💪💪請繼續完成今日的進度。'
    
    send_line_message(reply_text)

def reminder_event():
    # 下午兩點的提醒事件
    reply_text = "❗❗❗ 請記得完成今日LeetCode 👀"
    
    send_line_message(reply_text)

def report_event():
    # 获取台湾时区
    taiwan_tz = timezone('Asia/Taipei')

    # 获取今天早上8点的时间
    start_time = datetime.now(taiwan_tz).replace(hour=8, minute=0, second=0, microsecond=0)

    # 获取当前时间
    end_time = datetime.now(taiwan_tz)

    # 查询从早上8点到当前时间之间完成题目的用户和题目数量
    result = ReportLog.objects(created_at__gte=start_time, created_at__lt=end_time).aggregate([
        {"$group": {"_id": "$name", "count": {"$sum": 1}}}
    ])

    reply_text = "❗請記得回報今日進度❗"
    # reply_text += "⬇️目前尚未回報的有⬇️\n"
    # reply_text += "-----------------------------\n"

    # anybody = True

    # for entry in result:
    #     user_id = entry["_id"]
    #     count = int(entry["count"])

    #     # 仅在count小于0时显示记录
    #     if count < 1:
    #         # 构建回复消息
    #         reply_text += f"{user_id} 尚未回報\n"
    #         anybody = False

    # reply_text += "-----------------------------\n"
    # reply_text += '我看你們等著請客吧 哈'

    # if anybody:
    #     reply_text = "🎉恭喜各位都已完成今日目標\n"
    #     reply_text += "明天請繼續努力💪💪"
    
    send_line_message(reply_text)

# 添加定时任务，并设置触发时间（台湾时间）
scheduler.add_job(settlement_event, 'cron', hour=11, minute=35, timezone=taipei_tz)
scheduler.add_job(reminder_event, 'cron', hour=11, minute=36, timezone=taipei_tz)
scheduler.add_job(report_event, 'cron', hour=11, minute=37, timezone=taipei_tz)

# 启动调度器
scheduler.start()
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from leetcodelinebot.models import ReportLog, write_to_report_log

import re

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

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
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == '資料':
                    reply_text = get_report_logs()  # 调用函数获取 ReportLog 数据
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)  # 构建回复消息
                    )
                elif event.message.text.startswith('完成'):
                    topic = extract_topic_from_message(event.message.text)
                    if topic is not None:
                        # 建立 ReportLog 物件並保存到資料庫
                        write_to_report_log(user_name=event.source.user_id, topic=topic, done=True)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='已新增 ReportLog 資料')  # 回覆新增成功訊息
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='未提取到數字部分，舉例：[完成 1]')  # 回覆未提取到數字訊息
                        )
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def get_report_logs():
    all_logs = ReportLog.objects.all()
    reply_text = ""
    for log in all_logs:
        reply_text += f"Name: {log.name}, Topic: {log.topic}, Done: {log.done}, Created At: {log.created_at}\n"
    return reply_text

def extract_topic_from_message(message):
    # 使用正則表達式提取數字部分
    match = re.search(r'\b完成\s+(\d+)\b', message)
    
    if match:
        # 提取到數字部分，回傳作為 topic
        topic = match.group(1)
        return topic
    
    # 若未提取到數字部分，回傳 None
    return None
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from leetcodelinebot.models import ReportLog

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
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def get_report_logs():
    all_logs = ReportLog.objects.all()
    reply_text = ""
    for log in all_logs:
        reply_text += f"Name: {log.name}, Topic: {log.topic}, Done: {log.done}, Created At: {log.created_at}\n"
    return reply_text

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .models import MyModel

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if event.message.text.startswith("完成"):
                    # 解析用户输入的数字
                    try:
                        num = int(event.message.text.split(" ")[1])
                    except IndexError:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="请输入正确的格式，例如：完成 1")
                        )
                        continue
                    except ValueError:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="请输入有效的数字")
                        )
                        continue

                    # 将数字保存到数据库
                    my_object = MyModel(field1='Value', field2=num)
                    my_object.save()

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="已将数字保存到数据库")
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
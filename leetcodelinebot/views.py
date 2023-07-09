from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, JoinEvent, FollowEvent, MemberJoinedEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction

from leetcodelinebot.models import ReportLog, Users
from leetcodelinebot.lineNotify import line_notify_send_message
from leetcodelinebot.aeona import AI_chatbot
from leetcodelinebot.myself import myself
from datetime import datetime
from pytz import timezone
import re

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
            if isinstance(event, JoinEvent):  # 如果有加入聊天室的事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='哈囉 哈囉',
                        template=ButtonsTemplate(
                            thumbnail_image_url='https://picx.zhimg.com/v2-e1425095196ac03e4c781a42be0cdc26_r.jpg',  # 替換成你要顯示的圖片網址
                            title='大家好我是Tasktrackbot',
                            text='請先將我加入好友才可以為你服務',
                            actions=[
                                URITemplateAction(
                                    label='加入好友',
                                    uri='https://liff.line.me/1645278921-kWRPP32q/?accountId=615veimk'
                                )
                            ]
                        )
                    )
                )
                        
            elif isinstance(event, FollowEvent):  # 如果是加好友事件
                user_id = event.source.user_id
                profile = line_bot_api.get_profile(user_id)

                user = Users.objects(user_id=user_id).first()
                
                taiwan_tz = timezone('Asia/Taipei')
                taiwan_time = datetime.now(taiwan_tz)
                
                if user:
                    user.display_name = profile.display_name
                    user.status_message = profile.status_message
                    user.picture_url = profile.picture_url
                    user.save()
                else:
                    users = Users(
                        user_id = user_id,
                        name = profile.display_name,
                        status_message = profile.status_message,
                        picture_url = profile.picture_url,
                        punish = 0,
                        created_at=taiwan_time
                    )
                    users.save()

                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='哈囉 哈囉',
                        template=ButtonsTemplate(
                            thumbnail_image_url='https://picx.zhimg.com/v2-e1425095196ac03e4c781a42be0cdc26_r.jpg',  # 替換成你要顯示的圖片網址
                            title='哈囉~我是Tasktrackbot',
                            text='請先將我加入好友才可以為你服務',
                            actions=[
                                URITemplateAction(
                                    label='加入好友',
                                    uri='https://liff.line.me/1645278921-kWRPP32q/?accountId=615veimk'
                                )
                            ]
                        )
                    )
                )

            elif isinstance(event, MemberJoinedEvent):  # 如果是新的使用者加入群組事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='歡迎 歡迎',
                        template=ButtonsTemplate(
                            thumbnail_image_url='https://picx.zhimg.com/v2-e1425095196ac03e4c781a42be0cdc26_r.jpg',  # 替換成你要顯示的圖片網址
                            title='歡迎新朋友~我是Tasktrackbot',
                            text='請先將我加入好友才可以為你服務',
                            actions=[
                                URITemplateAction(
                                    label='加入好友',
                                    uri='https://liff.line.me/1645278921-kWRPP32q/?accountId=615veimk'
                                )
                            ]
                        )
                    )
                )
            elif isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == '查詢紀錄':
                    user_id = event.source.user_id
                    reply_text = get_report_stats(user_id)  # 呼叫函式取得 ReportLog 統計數據
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)  # 構建回覆訊息
                    )
                elif event.message.text == '回報進度':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="輸入格式：「完成 1」")  # 構建回覆訊息
                    )
                elif event.message.text is not None and event.message.text.startswith('完成'):
                    topic = extract_topic_from_message(event.message.text)
                    if topic is not None:
                        # 建立 ReportLog 物件並保存到資料庫
                        user_id = event.source.user_id
                        try:
                            profile = line_bot_api.get_profile(user_id)
                            reply_text = write_to_report_log(user_id=user_id, name=profile.display_name, topic=topic, done=True)
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=reply_text)  # 回覆新增成功訊息
                            )
                        except LineBotApiError:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='請先將我加為好友後再進行操作')  # 回覆未加入好友訊息
                            )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='未提取到數字，舉例:[完成 1]')  # 回覆未提取到數字訊息
                        )
                elif event.message.text == '查詢紀錄':
                    user_id = event.source.user_id
                    reply_text = get_report_stats(user_id)  # 呼叫函式取得 ReportLog 統計數據
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)  # 構建回覆訊息
                    )
                    print(event.source.group_id)
                elif event.message.text is not None and event.message.text.startswith('：'):
                    message = event.message.text
                    user_id = event.source.user_id
                    isMe = myself(user_id)
                    if isMe:
                        message = message.replace('：', '')
                        line_notify_send_message(message)
                else:
                    message = event.message.text
                    reply_text = AI_chatbot(message)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)  # 構建回覆訊息
                    )
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def write_to_report_log(user_id, name, topic, done):
    # 检查是否已存在相同用户和相同topic的记录
    existing_log = ReportLog.objects(user_id=user_id, topic=topic).first()

    if existing_log:
        reply_text = f"第{topic}題您已經完成了，請更換題目"
        return reply_text

    taiwan_tz = timezone('Asia/Taipei')
    taiwan_time = datetime.now(taiwan_tz)
    formatted_time = taiwan_time.strftime('%Y/%m/%d %H:%M')

    report_log = ReportLog(
        user_id=user_id,
        name=name,
        topic=topic,
        done=done,
        created_at=taiwan_time
    )

    report_log.save()
    reply_text = f"已新增ReportLog數據 {formatted_time}"
    return reply_text

def get_report_stats(user_id):
    taiwan_tz = timezone('Asia/Taipei')
    now = datetime.now(taiwan_tz)
    today = now.date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    all_topics = ReportLog.objects(user_id=user_id).distinct("topic")
    total_count = len(all_topics)
    
    today_topics = ReportLog.objects(user_id=user_id, created_at__gte=start_of_day, created_at__lte=end_of_day).distinct("topic")
    today_count = len(today_topics)

    reply_text = f"過去總共完成了{total_count}題測驗，今日已完成{today_count}題"

    return reply_text

def extract_topic_from_message(message):
    # 刪除所有空格
    message = message.replace(" ", "")
    # 使用正則表達式提取數字部分
    match = re.search(r'完成(\d+)|(\d+)完成', message)
    if match:
        # 提取到數字部分，回傳作為 topic
        topic = match.group(1) or match.group(2)
        return topic
    # 若未提取到數字部分，回傳 None
    return None
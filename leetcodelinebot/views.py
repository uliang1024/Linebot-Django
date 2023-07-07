from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, JoinEvent, FollowEvent, MemberJoinedEvent

from leetcodelinebot.models import ReportLog, Users

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
                group_id = event.source.group_id  # 群組ID
                user_ids = line_bot_api.get_group_member_ids(group_id)  # 取得群組內使用者ID列表

                for user_id in user_ids:
                    profile = line_bot_api.get_profile(user_id)
                    user = Users(
                        user_id = user_id,
                        # 其他使用者相關的欄位值
                    )
                    user.save()  # 將使用者物件保存至MongoDB的UsersCollection

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='大家好，我是Line bot！\n請將我加為好友才能為你服務！')  # 聊天室歡迎訊息
                )
            elif isinstance(event, FollowEvent):  # 如果是加好友事件
                user_id = event.source.user_id
                profile = line_bot_api.get_profile(user_id)

                user = Users.objects(user_id=user_id).first()
                if user:
                    user.display_name = profile.display_name
                    user.status_message = profile.status_message
                    user.picture_url = profile.picture_url
                    user.save()
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='有人偷偷加我好友')  # 聊天室歡迎訊息
                )
            elif isinstance(event, MemberJoinedEvent):  # 如果是新的使用者加入群組事件
                user_id = event.joined.members[0].user_id  # 取得新加入使用者的 ID
                profile = line_bot_api.get_profile(user_id)

                user = Users(
                    user_id=user_id,
                )
                user.save()
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='歡迎歡迎新朋友')  # 聊天室歡迎訊息
                )
            elif isinstance(event, MessageEvent):  # 如果有訊息事件
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
import os
import requests

CHATGPT_API_KEY = os.environ.get('CHATGPT_API_KEY')  # 從環境變量中獲取 ChatGPT 金鑰

def chatGPT_send_message(message):

    # 呼叫 ChatGPT API
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {CHATGPT_API_KEY}'},
        json={'messages': [{'role': 'system', 'content': 'user: ' + message}]},
    )
    print(response.json())
    
    # 從 ChatGPT API 的回應中取得回覆的訊息文字
    reply_text = response.json()['choices'][0]['message']['content']

    return reply_text

from flask import Flask, request, abort, url_for
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import requests
import random

# 環境變數檢查和錯誤處理
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    print("警告：LINE Bot 環境變數未設定")
    # 在開發環境中可以設定預設值，生產環境中會使用實際的環境變數
    LINE_CHANNEL_ACCESS_TOKEN = LINE_CHANNEL_ACCESS_TOKEN or "default_token"
    LINE_CHANNEL_SECRET = LINE_CHANNEL_SECRET or "default_secret"

try:
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    line_handler = WebhookHandler(LINE_CHANNEL_SECRET)
except Exception as e:
    print(f"LINE Bot 初始化錯誤: {str(e)}")
    # 創建假的處理器以避免系統崩潰
    line_bot_api = None
    line_handler = None

mant0u_bot_model = os.getenv("MANT0U_BOT_MODEL", "default")

app = Flask(__name__)

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

# 忽略對 favicon.ico 的請求（避免 favicon.ico 的 404 錯誤 ）
@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')

@app.route("/webhook", methods=['POST'])
def callback():
    if not line_handler or not line_bot_api:
        return 'SERVICE_UNAVAILABLE', 503
        
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature', '')
    # get request body as text
    body = request.get_data(as_text=True)
    
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature error")
        abort(400)
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        # 記錄錯誤但不中斷服務
        return 'ERROR', 500
    return 'OK'

# 安全的訊息發送函數
def safe_reply_message(reply_token, message):
    if line_bot_api:
        try:
            line_bot_api.reply_message(reply_token, message)
        except Exception as e:
            print(f"Failed to send message: {str(e)}")

# 文字訊息處理（簡化版本）
if line_handler:
    @line_handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        try:
            # 取得「使用者」訊息
            userMessage = event.message.text
            print(f"Received message: {userMessage}")
            
            # 基本回應
            if userMessage == "ping":
                text_message = TextSendMessage(text="pong")
                safe_reply_message(event.reply_token, text_message)
            elif userMessage == "hello" or userMessage == "你好":
                text_message = TextSendMessage(text="Hello! 機器人運作正常。")
                safe_reply_message(event.reply_token, text_message)
            else:
                # 預設回應
                text_message = TextSendMessage(text="收到訊息，但功能暫時簡化中。")
                safe_reply_message(event.reply_token, text_message)
                
        except Exception as e:
            print(f"Message handling error: {str(e)}")
            # 發送簡單的錯誤回覆
            try:
                error_message = TextSendMessage(text="系統處理中發生錯誤，請稍後再試。")
                safe_reply_message(event.reply_token, error_message)
            except:
                pass  # 如果連錯誤回覆都失敗，就忽略

if __name__ == "__main__":
    app.run()

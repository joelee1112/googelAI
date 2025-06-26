from flask import Flask, request, abort, url_for
import os
import sys

# 環境變數檢查
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)

# 初始化 LINE Bot 相關變數
line_bot_api = None
line_handler = None

# 嘗試匯入 LINE Bot SDK
try:
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *
    
    if LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET:
        line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        line_handler = WebhookHandler(LINE_CHANNEL_SECRET)
        print("LINE Bot SDK 初始化成功")
    else:
        print("警告：LINE Bot 環境變數未設定")
        
except ImportError as e:
    print(f"LINE Bot SDK 匯入失敗: {str(e)}")
except Exception as e:
    print(f"LINE Bot 初始化錯誤: {str(e)}")

# 嘗試匯入其他必要模組
try:
    import requests
    import random
    print("基本模組匯入成功")
except ImportError as e:
    print(f"基本模組匯入失敗: {str(e)}")

# 嘗試匯入自定義模組（如果失敗則繼續運行）
modules_to_import = [
    'apps.example.sendMessage',
    'apps.menu.main',
    'apps.common.common',
]

for module_name in modules_to_import:
    try:
        __import__(module_name)
        print(f"成功匯入: {module_name}")
    except Exception as e:
        print(f"匯入失敗: {module_name} - {str(e)}")

@app.route('/')
def home():
    return 'Hello, World! 機器人服務運行中。'

@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')

@app.route("/webhook", methods=['POST'])
def callback():
    if not line_handler or not line_bot_api:
        return 'LINE Bot 服務未正確初始化', 503
        
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature', '')
    # get request body as text
    body = request.get_data(as_text=True)
    
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature error")
        abort(400)
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return 'Webhook 處理錯誤', 500
    
    return 'OK'

# 安全的訊息發送函數
def safe_reply_message(reply_token, message):
    if line_bot_api:
        try:
            line_bot_api.reply_message(reply_token, message)
            return True
        except Exception as e:
            print(f"發送訊息失敗: {str(e)}")
            return False
    return False

# 註冊事件處理器（只有在 LINE Bot 正確初始化時）
if line_handler and 'TextMessage' in globals():
    @line_handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        try:
            userMessage = event.message.text
            print(f"收到訊息: {userMessage}")
            
            # 基本測試訊息
            if userMessage.lower() == "ping":
                text_message = TextSendMessage(text="pong")
                safe_reply_message(event.reply_token, text_message)
            elif userMessage in ["hello", "你好", "測試"]:
                text_message = TextSendMessage(text="Hello! 機器人運作正常。")
                safe_reply_message(event.reply_token, text_message)
            elif userMessage == "狀態":
                status_text = f"系統狀態：正常\\n版本：簡化版本\\nPython: {sys.version}"
                text_message = TextSendMessage(text=status_text)
                safe_reply_message(event.reply_token, text_message)
            else:
                # 嘗試呼叫原始功能（如果可用）
                try:
                    # 這裡可以添加原始功能的呼叫
                    # 例如：handle_original_message(event, userMessage)
                    text_message = TextSendMessage(text="功能暫時簡化中，僅支援基本回應。")
                    safe_reply_message(event.reply_token, text_message)
                except:
                    text_message = TextSendMessage(text="收到您的訊息了！")
                    safe_reply_message(event.reply_token, text_message)
                    
        except Exception as e:
            print(f"訊息處理錯誤: {str(e)}")
            try:
                error_message = TextSendMessage(text="系統處理中發生錯誤，請稍後再試。")
                safe_reply_message(event.reply_token, error_message)
            except:
                pass

    # 處理其他類型的訊息
    if 'AudioMessage' in globals():
        @line_handler.add(MessageEvent, message=AudioMessage)
        def handle_audio_message(event):
            try:
                text_message = TextSendMessage(text="收到語音訊息，但語音處理功能暫時停用。")
                safe_reply_message(event.reply_token, text_message)
            except Exception as e:
                print(f"語音訊息處理錯誤: {str(e)}")

    if 'ImageMessage' in globals():
        @line_handler.add(MessageEvent, message=ImageMessage)
        def handle_image_message(event):
            try:
                text_message = TextSendMessage(text="收到圖片訊息，但圖片處理功能暫時停用。")
                safe_reply_message(event.reply_token, text_message)
            except Exception as e:
                print(f"圖片訊息處理錯誤: {str(e)}")

else:
    print("LINE Bot 處理器未正確初始化，將以最小模式運行")

if __name__ == "__main__":
    app.run()

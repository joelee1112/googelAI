import os
import sys
import traceback
from flask import Flask, request, jsonify

app = Flask(__name__)

# 全域變數
line_bot_api = None
line_handler = None

def init_linebot():
    """初始化 LINE Bot"""
    global line_bot_api, line_handler
    
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    secret = os.getenv('LINE_CHANNEL_SECRET')
    
    if not token or not secret:
        print("LINE Bot credentials not found")
        return False
    
    try:
        from linebot import LineBotApi, WebhookHandler
        from linebot.exceptions import InvalidSignatureError
        from linebot.models import MessageEvent, TextMessage, TextSendMessage
        
        line_bot_api = LineBotApi(token)
        line_handler = WebhookHandler(secret)
        
        @line_handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            try:
                user_message = event.message.text
                print(f"收到訊息: {user_message}")
                
                # 簡單回應邏輯
                if user_message.lower() in ['ping', 'test', '測試']:
                    reply_text = "pong - 機器人正常運作！"
                elif user_message.lower() in ['hello', '你好', 'hi']:
                    reply_text = "Hello! 很高興為您服務 😊"
                elif user_message == '狀態':
                    reply_text = f"系統狀態：正常運行\\nPython: {sys.version[:6]}\\n時間：運行中"
                else:
                    reply_text = f"收到您的訊息：{user_message}\\n\\n(這是簡化版本的回應)"
                
                text_message = TextSendMessage(text=reply_text)
                line_bot_api.reply_message(event.reply_token, text_message)
                
            except Exception as e:
                print(f"訊息處理錯誤: {str(e)}")
                try:
                    error_message = TextSendMessage(text="系統處理中發生錯誤，請稍後再試。")
                    line_bot_api.reply_message(event.reply_token, error_message)
                except:
                    pass
        
        print("LINE Bot 初始化成功")
        return True
        
    except ImportError as e:
        print(f"LINE Bot SDK 未安裝: {str(e)}")
        return False
    except Exception as e:
        print(f"LINE Bot 初始化失敗: {str(e)}")
        return False

# 嘗試初始化 LINE Bot
linebot_available = init_linebot()

@app.route('/')
def home():
    status = "LINE Bot 已啟用" if linebot_available else "LINE Bot 未啟用（基本模式）"
    return f'Hello World! 機器人服務運行中。\\n狀態: {status}'

@app.route('/status')
def status():
    return jsonify({
        'status': 'running',
        'linebot_available': linebot_available,
        'python_version': sys.version,
        'environment': 'production' if os.getenv('VERCEL') else 'development'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not linebot_available:
            print("LINE Bot 未啟用，返回基本回應")
            return 'LINE Bot 未啟用，但 webhook 接收正常', 200
        
        signature = request.headers.get('X-Line-Signature', '')
        body = request.get_data(as_text=True)
        
        print(f"Webhook 接收: signature={signature[:10] if signature else 'None'}..., body_length={len(body)}")
        
        from linebot.exceptions import InvalidSignatureError
        
        try:
            line_handler.handle(body, signature)
            print("訊息處理成功")
        except InvalidSignatureError:
            print("簽名驗證失敗")
            return 'Invalid signature', 400
        except Exception as e:
            print(f"訊息處理錯誤: {str(e)}")
            return f'Message processing error: {str(e)}', 500
        
        return 'OK'
        
    except Exception as e:
        error_msg = f'Webhook 錯誤: {str(e)}'
        print(error_msg)
        print(traceback.format_exc())
        return error_msg, 500

# 錯誤處理
@app.errorhandler(404)
def not_found(error):
    return 'Page not found', 404

@app.errorhandler(500)
def internal_error(error):
    error_msg = f'Internal server error: {str(error)}'
    print(error_msg)
    print(traceback.format_exc())
    return error_msg, 500

if __name__ == "__main__":
    app.run(debug=True)

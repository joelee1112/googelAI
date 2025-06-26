from flask import Flask, request, abort
import os
import sys
import traceback

app = Flask(__name__)

# 全域錯誤處理
@app.errorhandler(500)
def internal_error(error):
    return f'Internal Server Error: {str(error)}', 500

@app.errorhandler(404)
def not_found(error):
    return 'Not Found', 404

@app.route('/')
def home():
    return 'Hello, World! Bot Service is Running.'

@app.route('/status')
def status():
    return {
        'status': 'running',
        'python_version': sys.version,
        'environment': 'production' if os.getenv('VERCEL') else 'development'
    }

# LINE Bot webhook
@app.route("/webhook", methods=['POST'])
def callback():
    try:
        # 基本的 webhook 處理
        signature = request.headers.get('X-Line-Signature', '')
        body = request.get_data(as_text=True)
        
        # 簡單記錄
        print(f"Received webhook: signature={signature[:10]}..., body_length={len(body)}")
        
        # 環境變數檢查
        token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        secret = os.getenv("LINE_CHANNEL_SECRET")
        
        if not token or not secret:
            print("LINE credentials not configured")
            return 'Configuration Error', 500
        
        # 嘗試處理 LINE Bot 邏輯
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
                    print(f"User message: {user_message}")
                    
                    # 簡單回應
                    if user_message.lower() in ['ping', 'test', '測試']:
                        reply_text = "pong - 機器人正常運作"
                    elif user_message.lower() in ['hello', '你好', 'hi']:
                        reply_text = "Hello! 很高興為您服務"
                    else:
                        reply_text = f"收到您的訊息：{user_message}"
                    
                    text_message = TextSendMessage(text=reply_text)
                    line_bot_api.reply_message(event.reply_token, text_message)
                    
                except Exception as e:
                    print(f"Message handling error: {str(e)}")
                    traceback.print_exc()
            
            # 處理 webhook
            line_handler.handle(body, signature)
            
        except InvalidSignatureError:
            print("Invalid signature")
            abort(400)
        except ImportError as e:
            print(f"LINE Bot SDK not available: {str(e)}")
            return 'LINE Bot SDK Error', 500
        except Exception as e:
            print(f"LINE Bot processing error: {str(e)}")
            traceback.print_exc()
            return 'Processing Error', 500
        
        return 'OK'
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        traceback.print_exc()
        return 'Webhook Error', 500

if __name__ == "__main__":
    app.run(debug=True)

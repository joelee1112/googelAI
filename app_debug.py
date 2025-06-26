import os
import sys
import traceback
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World - Debugging Version'

@app.route('/debug')
def debug():
    try:
        debug_info = {
            'python_version': sys.version,
            'flask_version': Flask.__version__,
            'current_directory': os.getcwd(),
            'environment_variables': {
                'VERCEL': os.getenv('VERCEL', 'Not set'),
                'VERCEL_ENV': os.getenv('VERCEL_ENV', 'Not set'),
                'LINE_CHANNEL_ACCESS_TOKEN': 'Set' if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') else 'Not set',
                'LINE_CHANNEL_SECRET': 'Set' if os.getenv('LINE_CHANNEL_SECRET') else 'Not set'
            },
            'available_files': os.listdir('.'),
        }
        
        # 測試模組匯入
        modules_test = {}
        test_modules = ['flask', 'os', 'sys', 'json']
        for module in test_modules:
            try:
                __import__(module)
                modules_test[module] = 'OK'
            except Exception as e:
                modules_test[module] = f'Error: {str(e)}'
        
        debug_info['modules_test'] = modules_test
        
        return jsonify(debug_info)
    except Exception as e:
        return f'Debug error: {str(e)}\\n{traceback.format_exc()}', 500

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    try:
        if request.method == 'GET':
            return 'Webhook endpoint is working (GET)'
        
        # 基本的 POST 處理
        data = request.get_data()
        return f'Webhook received POST data (length: {len(data)})', 200
        
    except Exception as e:
        error_msg = f'Webhook error: {str(e)}\\n{traceback.format_exc()}'
        print(error_msg)  # 這會出現在 Vercel 日誌中
        return error_msg, 500

# 全域錯誤處理
@app.errorhandler(404)
def not_found(error):
    return 'Page not found', 404

@app.errorhandler(500)
def internal_error(error):
    error_msg = f'Internal server error: {str(error)}\\n{traceback.format_exc()}'
    print(error_msg)  # 記錄到日誌
    return error_msg, 500

# 處理所有未捕獲的異常
@app.errorhandler(Exception)
def handle_exception(e):
    error_msg = f'Unhandled exception: {str(e)}\\n{traceback.format_exc()}'
    print(error_msg)
    return error_msg, 500

if __name__ == "__main__":
    app.run(debug=True)

import sys
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Diagnostic Service Running'

@app.route('/debug')
def debug():
    debug_info = []
    
    # Python 版本
    debug_info.append(f"Python Version: {sys.version}")
    
    # 環境變數檢查
    env_vars = [
        'LINE_CHANNEL_ACCESS_TOKEN',
        'LINE_CHANNEL_SECRET', 
        'MANT0U_BOT_MODEL',
        'IMGBB_KEY'
    ]
    
    debug_info.append("Environment Variables:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            debug_info.append(f"  {var}: ✓ (設定)")
        else:
            debug_info.append(f"  {var}: ✗ (未設定)")
    
    # 模組檢查
    debug_info.append("\\nModule Import Tests:")
    modules = [
        'flask',
        'linebot',
        'requests',
        'bs4',
        'googletrans',
        'imgbbpy',
        'zhdate',
        'zhconv',
        'firebase_admin'
    ]
    
    for module in modules:
        try:
            __import__(module)
            debug_info.append(f"  {module}: ✓")
        except ImportError as e:
            debug_info.append(f"  {module}: ✗ ({str(e)})")
    
    # 自定義模組檢查
    debug_info.append("\\nCustom Modules:")
    custom_modules = [
        'apps.common.common',
        'apps.menu.main',
        'apps.ai.main'
    ]
    
    for module in custom_modules:
        try:
            __import__(module)
            debug_info.append(f"  {module}: ✓")
        except Exception as e:
            debug_info.append(f"  {module}: ✗ ({str(e)})")
    
    # 檔案系統檢查
    debug_info.append("\\nFile System:")
    debug_info.append(f"  Current Directory: {os.getcwd()}")
    debug_info.append(f"  Files in root: {os.listdir('.')}")
    
    if os.path.exists('apps'):
        debug_info.append(f"  Files in apps/: {os.listdir('apps')}")
    
    return '<pre>' + '\\n'.join(debug_info) + '</pre>'

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'diagnostic'}

if __name__ == "__main__":
    app.run()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World - Basic Test'

@app.route('/test')
def test():
    return {'status': 'ok', 'message': 'Server is running'}

@app.route('/webhook', methods=['POST'])
def webhook():
    return 'Webhook received', 200

if __name__ == "__main__":
    app.run()

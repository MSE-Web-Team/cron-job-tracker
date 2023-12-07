from flask import Flask

app = Flask(__name__)

@app.route('/api')
def api_endpoint():
    return 'Hello from the API endpoint!'

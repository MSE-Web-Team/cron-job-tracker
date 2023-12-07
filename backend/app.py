from flask import Flask

app = Flask(__name__)

@app.route('/')
def api_endpoint():
    return 'Hello from the API endpoint!'

@app.route('/api/')
def api_endpoint():
    return '/api/ endpoint'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

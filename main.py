from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from my Python app on Railway!'

if __name__ == '__main__':
    app.run(debug=True)

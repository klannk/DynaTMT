from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/",methods=["GET", "POST"])

def hello():
    return('Hello World from Python:')
if __name__ =='__main__':
    app.run()
    
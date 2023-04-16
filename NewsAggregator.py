from flask import Flask
from webscraper import run
from flask import request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/summarize', methods=['GET'])
def summarize():
    url = request.args.get("url")
    return run(url)


@app.route('/test', methods=['GET'])
def test():
    return {"success": "true"}

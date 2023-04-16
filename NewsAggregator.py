from flask import Flask
from webscraper import run
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/summarize', methods=['GET'])
@cross_origin()
def summarize():
	url = request.args.get("url")
	return run(url)

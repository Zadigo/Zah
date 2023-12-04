from flask import Flask
from flask.json import jsonify
from flask.wrappers import Response

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({'some value': None})

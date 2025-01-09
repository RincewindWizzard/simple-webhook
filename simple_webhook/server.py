import json

from flask import Flask, request
from simple_webhook import pyproject

app = Flask(__name__)


@app.route('/')
def index():
    dict(
        name=pyproject['tool']['poetry']['name'],
        version=pyproject['tool']['poetry']['version'],
        author=
    )
    return json.dumps(pyproject)


@app.route('/webhook', methods=['POST'])
def webhook():
    print(request.get_json())

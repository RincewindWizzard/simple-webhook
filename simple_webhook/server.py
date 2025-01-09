import json
import subprocess

from flask import Flask, request
from simple_webhook import pyproject, logger, config
from simple_webhook.decorators import require_api_token

app = Flask(__name__)

application_json = {'Content-Type': 'application/json'}

@app.route('/')
def index():
    return json.dumps(dict(
        name=pyproject['tool']['poetry']['name'],
        version=pyproject['tool']['poetry']['version'],
        authors=pyproject['tool']['poetry']['authors'],
        repository=pyproject['tool']['poetry']['repository'],
    )), 200, application_json


@app.route('/webhook/firefox', methods=['POST'])
@require_api_token
def webhook():
    doc = request.get_json()
    if 'url' in doc:
        command = [
            'firefox', '--kiosk', '--new-window', doc['url']
        ]
        logger.info(f'Running command: {command}')
        try:
            subprocess.run(command, check=True)
        except FileNotFoundError:
            return {'message': 'Command could not be found'}, 500, application_json
        except subprocess.CalledProcessError as e:
            return {'message': 'Command returned a non zero exit status'}, 500, application_json
    else:
        return {'message': 'Missing url in body'}, 422, application_json

    return {'message': 'ok'}, 200, application_json

from os import environ

from flask import Flask, request
from tutorbot import Bot
import requests

app = Flask(__name__)

bot = Bot()

SLACK_TOKEN = environ['SLACK_TOKEN']

headers = {
    "Authorization": "Bearer " + SLACK_TOKEN
}

WEBHOOK_URL = environ['WEBHOOK_URL']

def send_message(data):
    requests.post(
        WEBHOOK_URL,
        json=data
    )


@app.route('/events', methods=['POST'])
def mention():
    """Called when bot has received a Slack event"""
    req_json = request.get_json()
    if 'challenge' in req_json:
        return req_json['challenge']
    response = bot.handle_event(req_json)
    if response:
        send_message(response)
    return ""


@app.route('/command', methods=['POST'])
def command():
    """Called when the bot is activated via Slash command"""
    ...

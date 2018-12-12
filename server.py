from flask import Flask, request
from tutorbot import Bot
import requests

app = Flask(__name__)

bot = Bot()

TOKEN = "xoxp-501495172338-501495173074-500910471329-2cd1130d6b6c2ec1af15db77371dcf53"

headers = {
    "Authorization": "Bearer " + TOKEN
}

WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_message(data):
    print("Sending message")
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

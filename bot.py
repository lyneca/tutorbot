from flask import Flask, request

app = Flask(__name__)

@app.route('/events', methods=['POST'])
def mention():
    """ Called when bot has received a Slack event """
    req_json = request.get_json()
    if 'challenge' in req_json:
        return req_json['challenge']

@app.route('/command', methods=['POST'])
def command():
    """ Called when the bot is activated via Slash command """
    ...
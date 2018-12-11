from flask import Flask

app = Flask(__name__)

@app.route('/events', methods=['POST'])
def mention():
    """ Called when bot has received a Slack event """
    ...

@app.route('/command', methods=['POST'])
def command():
    """ Called when the bot is activated via Slash command """
    ...
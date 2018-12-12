import random
import re

from flask import jsonify

PING_MESSAGES = [
    "Pong! I'm awake, I swear!",
    "Pong! I wasn't asleep!",
    "Pong... five more minutes please...",
    "Pong... *hits snooze*",
    "zzz... pong... zzz"
]

ERROR_COLOR = "warning"
ERROR_MENTION_AT_START = ("Sorry, try @mentioning me at the start"
                          "of your message - e.g. @tutorbot help")
ERROR_MENTION_UNKNOWN_COMMAND = "Sorry, I didn't understand that command."


class Bot:
    """
    Class to define the bot behaviour

    Most methods should accept a Flask request,
    and return a JSON object representing the response.
    """

    def __init__(self):
        self.mention_commands = {
            'help': self.help,
            'ping': self.ping
        }

    def handle_event(self, event):
        """Handle an incoming Slack event"""
        event_types = {
            'app_mention': self.mentioned,
            'reaction_added': self.reaction_added,
            'reaction_removed': self.reaction_removed,
        }
        return event_types[event['type']](event)

    def handle_command(self, request):
        """Handle an incoming Slack slash command"""
        ...

    def error(self, message):
        """Return a formatted error message"""
        return {
            "attachments": [
                {
                    "text": message,
                    "fallback": message,
                    "color": ERROR_COLOR,
                    "footer": "Type '@tutorbot help' for help.",
                }
            ]
        }

    def get_help(self, command):
        help_text = self.mention_commands[command].__doc__.strip().split('\n')
        help_text = [x.strip() for x in help_text]
        usage = []
        for line in help_text:
            if line.startswith(":usage:"):
                usage.append(line[7:])
        help_text = [x for x in help_text if not x.startswith(":usage:")]
        return help_text, usage

    def get_help_field(self, command):
        text, _ = self.get_help(command)
        return {
            "title": command,
            "value": text[0],
            "short": False
        }

    def help(self, text, event):
        """
        List commands or show help on a specific command

        :usage: `@tutorbot help`
        :usage: `@tutorbot help [command]`
        """
        if text:
            command = text[0]
            if command in self.mention_commands:
                text, usage = self.get_help(command)
                text = "\n".join(text)
                return {
                    "channel": event["channel"],
                    "attachments": [
                        {
                            "fallback": text + "\n\n" + "\n".join(usage),
                            "pretext": f"Showing help for *@tutorbot {command}*",
                            "text": text,
                            "color": "good",
                            "fields": [
                                {"title": "Usage"},
                                *[
                                    {
                                        "value": x,
                                        "short": False
                                    } for x in usage
                                ]
                            ]
                        }
                    ]
                }
            return self.error(ERROR_MENTION_UNKNOWN_COMMAND)
        return {
            "channel": event["channel"],
            "text": "",
            "attachments": [
                {
                    "fallback": '\n'.join(sorted(list(self.mention_commands.keys()))),
                    "pretext": "Available commands:",
                    "color": "good",
                    "fields": [
                        self.get_help_field(command) for command in self.mention_commands
                    ]
                }
            ]
        }

    def ping(self, text, event):
        """
        Ping the bot to wake it up (if it's sleeping)

        Because tutorbot is running on a free-tier Heroku dyno, it goes to sleep
        after a period of inactivity. Pinging the bot with this command will wake
        it up again; although, any other command will do the same.
        """

        return {
            "channel": event["channel"],
            "text": random.choice(PING_MESSAGES),
            "mrkdwn": False
        }

    def mentioned(self, event):
        """Bot was @mentioned"""
        text = event['text']
        if not re.match(r"^\s*<@\w+>", event["text"]):
            return self.error(ERROR_MENTION_AT_START)
        first_word = text.split()[1]
        if first_word not in self.mention_commands:
            return self.error(ERROR_MENTION_UNKNOWN_COMMAND)
        return self.mention_commands[first_word](text.split()[2:], event)

    def reaction_added(self, event):
        """A reaction was added to a message"""
        ...

    def reaction_removed(self, event):
        """A reaction was removed from a message"""
        ...


if __name__ == '__main__':
    bot = Bot()
    print(bot.get_help('help'))

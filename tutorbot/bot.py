from flask import jsonify
import re


ERROR_COLOR = "warning"
ERROR_MENTION_AT_START = ("Sorry, try @mentioning me at the start"
                          "of your message - e.g. @tutorbot help")
ERROR_MENTION_UNKNOWN_COMMAND = ("Sorry, I don't know what you mean."
                                 "Type `@tutorbot help` for help.")


class Bot:
    """
    Class to define the bot behaviour

    Most methods should accept a Flask request,
    and return a JSON object representing the response.
    """

    def __init__(self):
        self.mention_commands = {
            'help': self.help
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
                    "fallback": message,
                    "color": ERROR_COLOR
                }
            ]
        }

    def get_help(self, command):
        help_text = self.mention_commands[command].__doc__.split('\n')
        help_text = [x.strip() for x in help_text]
        usage = []
        for line in help_text:
            if line.startswith(":usage:"):
                usage.append(line[7:])
        return help_text, usage

    def get_help_field(self, command):
        text, _ = self.get_help(command)
        return {
            "title": command,
            "value": text,
            "short": True
        }

    def help(self, text, event):
        """
        Display a help message

        :usage: `@tutorbot help`
        :usage: `@tutorbot help [command]`
        """
        return {
            "channel": event["channel"],
            "text": "",
            "attachments": [
                {
                    "fallback": '\n'.join(sorted(list(self.mention_commands.keys()))),
                    "pretext": "Available commands:",
                    "fields": [
                        self.get_help_field(command) for command in self.mention_commands
                    ]
                }
            ]
        }

    def mentioned(self, event):
        """Bot was @mentioned"""
        text = event['text']
        if not re.match(r'^\s*<@\w+>', event['text']):
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
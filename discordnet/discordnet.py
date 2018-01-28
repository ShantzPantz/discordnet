import discord
import threading
from plugins import coinflip

import config
from importer import list_plugins

HELP_DOC = """help <command>
help syntax:
optional arguments: [arg name]
mandatory arguments: <arg name>
literal arguments: 'this|yesterday|tomorrow'

literal commands can be mandatory or optional"""


class DiscordNetBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugins_interactive = {}
        # Plugins that are passive background tasks and aren't triggered by commands
        self.plugins_passive = []
        self.load_plugins()

    def load_plugins(self):
        print("loading plugins!")
        self.plugins_interactive = {}
        self.plugins_passive = []
        plugins = list_plugins()
        if not plugins:
            print("No plugins")
            return
        for plugin in plugins:
            if plugin.COMMAND:
                self.plugins_interactive[plugin.COMMAND.lower()] = plugin
            else:
                self.plugins_passive.append(plugin)

    @staticmethod
    def parse_command_content(content):
        print("Original Message: " + content)
        if not content:
            return
        print("Prefix: " + content[0])
        if content[0] != config.COMMAND_PREFIX:
            return
        command, _, content = content[1:].partition(' ')
        clean_command = command.lower().strip()
        return clean_command, content

    async def run_plugin(self, message, **kwargs):
        parsed_content = self.parse_command_content(message.content)
        if parsed_content is None:
            return
        command, content = parsed_content
        print(command)
        map(print, self.plugins_interactive)
        if command in self.plugins_interactive:
            plugin = self.plugins_interactive[command]
            await plugin.main(self, message)
        else:
            print("Invalid Command " + command)


if __name__ == '__main__':
    print('Hello World')
    client = DiscordNetBot()

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('-------------')

    @client.event
    async def on_message(message):
        if message.author.name == client.user.name:
            return
        await client.run_plugin(message)


    client.run(config.DISCORD_TOKEN)


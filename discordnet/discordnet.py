import discord

import config
from importer import list_plugins

HELP_DOC = """help <command>"""


class DiscordNetBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugins_interactive = {}
        # Plugins that are passive background tasks and aren't triggered by commands
        self.plugins_passive = []
        self.plugin_helps = {}
        self.load_plugins()

    def load_plugins(self):
        print("loading plugins!")
        self.plugins_interactive = {}
        self.plugins_passive = []
        self.plugin_helps = {
            'help': HELP_DOC
        }
        plugins = list_plugins()
        if not plugins:
            return
        for plugin in plugins:
            if plugin.__doc__ and plugin.COMMAND:
                self.plugin_helps[plugin.COMMAND.lower()] = plugin.__doc__.strip('\n')
            if plugin.COMMAND:
                print("Adding Plugin: " + plugin.COMMAND)
                self.plugins_interactive[plugin.COMMAND.lower()] = plugin
            else:
                self.plugins_passive.append(plugin)

    @staticmethod
    def parse_command_content(content):
        if not content:
            return
        if content[0] != config.COMMAND_PREFIX:
            return
        command, _, content = content[1:].partition(' ')
        clean_command = command.lower().strip()
        return clean_command, content

    async def run_plugins_passive(self, message, **kwargs):
        for plugin in self.plugins_passive:
            await plugin.main(self, message, **kwargs)

    async def run_plugin_interactive(self, message, **kwargs):
        parsed_content = self.parse_command_content(message.content)
        if parsed_content is None:
            return
        command, content = parsed_content
        message.content = content
        if command in self.plugins_interactive:
            plugin = self.plugins_interactive[command]
            await plugin.main(self, message, **kwargs)


if __name__ == '__main__':
    print('Starting DiscordNet')
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
        await client.run_plugins_passive(message)
        await client.run_plugin_interactive(message)


    client.run(config.DISCORD_TOKEN)


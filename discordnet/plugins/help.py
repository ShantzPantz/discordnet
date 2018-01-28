
import config

__author__ = 'Brian Shantz'
COMMAND = 'help'


async def main(bot, message, **kwargs):
    content_parts = message.content.split()
    if not content_parts:
        command_list = []
        for command in bot.plugins_interactive.keys():
            command_list.append(config.COMMAND_PREFIX + command)
        await bot.send_message(message.channel, 'Available Commands: \n' + '\n'.join(command_list))
    else:
        plugin = content_parts[0]
        if plugin.startswith(config.COMMAND_PREFIX):
            plugin = plugin[1:]
        if plugin in bot.plugin_helps:
            await bot.send_message(message.channel, plugin + ": " + bot.plugin_helps[plugin])
        else:
            await bot.send_message(message.channel, 'help not found for command `' + plugin + '`')


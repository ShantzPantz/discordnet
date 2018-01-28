'''
Barebonese Test
'''

__author__ = ('Brian', 'Shantz')
COMMAND = 'test'


async def main(bot, message, **kwargs):
    await bot.send_message(message.channel, "Test Successful! - Content passed was '"+message.content+"'")


'''
Flip a coin, 50/50 shot.
'''

import random

__author__ = ('Brian', 'Shantz')
COMMAND = 'coinflip'


def coinflip():
    PROBABILITY = 0.5
    return "heads" if _chance(PROBABILITY) else "tails"


def _chance(probability):
    return random.random() < probability


async def main(bot, message, **kwargs):
    flip = coinflip()
    await bot.send_message(message.channel, flip)


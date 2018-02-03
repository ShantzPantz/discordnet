'''
    Generate messages based on a markov chain model based on message history.
    Usage:
        !imitate                - returns 5 generated messages for you based on historical data.
        !imitate <@username>     - returns 5 generated messages for a user.
'''

import random

import markovify
import json


COMMAND = 'imitate'


openers = [
    'Hey, you guys wanna here my %username% impression?',
    "Look at me. I'm the %username% now.",
    "Here's my attempt at %username%.",
    "This is my impression of %username%. Could I make it on the comedy circuit?",
    "Oh, so we're doing this for %username% too?",
    "Do you want it done well, or fast? I can do neither. Here's my %username% imitation."
]


def get_random_opener(username):
    global openers
    return random.choice(openers).replace('%username%', username)


def get_sub_command(content):
    if not content:
        return None
    parts = content.split(' ')
    return parts[0]


def generate_sentences_from_messages(messages):
    usertext = ""
    for t in messages:
        usertext += t['clean_content'] + "\n"
    # make model out of chat messages
    model = markovify.NewlineText(usertext)
    # Collect five randomly-generated sentences
    generated = []
    for i in range(5):
        generated.append(model.make_sentence())
    return generated


async def main(bot, message, **kwargs):
    for me in message.mentions:
        print(me.mention)
        print(me.name)
    if message.mentions is None or len(message.mentions) == 0:
        targetusers = [message.author]
    else:
        targetusers = message.mentions

    # eventually handle more than one target user, but for now just use the first in the list.
    user = targetusers[0]
    usermessages = await bot.get_all_messages(message.channel.id, user.id)
    #usermessages = await bot.get_all_messages('356961851679965186', user.id)

    if usermessages is not None and len(usermessages) > 5:
        responses = generate_sentences_from_messages(usermessages)
        filtered = list(filter(lambda x: x is not None, responses))
        if len(filtered) > 0:
            print(responses)
            output = get_random_opener(user.mention) + "\n\n" + " ".join(filtered)
        else:
            output = "Wow... I wasn't able to generate messages for " + user.display_name
    else:
        output = "Sorry, I don't have enough data to generate messages for " + user.display_name

    await bot.send_message(message.channel, output)




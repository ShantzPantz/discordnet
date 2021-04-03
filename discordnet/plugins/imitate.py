'''
    Generate messages based on a markov chain model based on message history.
    Usage:
        !imitate <@username> <#channel>  - returns 5 generated messages for a user from data on an existing channel.
'''

import random

import markovify


COMMAND = 'imitate'


openers = [
    'Hey, you guys wanna hear my %username% impression?',
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


def generate_sentences_from_messages(messages, short=True):
    usertext = ""
    for t in messages:
        usertext += t['clean_content'] + "\n"
    # make model out of chat messages
    model = markovify.NewlineText(usertext)
    # Collect five randomly-generated sentences
    generated = []
    for i in range(5):
        gentext = model.make_short_sentence(140, 0) if short else model.make_sentence()
        generated.append(gentext)
    return generated


async def main(bot, message, **kwargs):
    for me in message.mentions:
        print("User Mention: " + me.name)
    for ch in message.channel_mentions:
        print("Channel Mention: " + ch.name)
    if message.mentions is None or len(message.mentions) == 0:
        targetusers = [message.author]
    else:
        targetusers = message.mentions

    if message.channel_mentions is None or len(message.channel_mentions) == 0:
        targetchannels = bot.get_all_channels()
    else:
        targetchannels = message.channel_mentions

    # eventually handle more than one target user, but for now just use the first in the list.
    user_names = [user.name for user in targetusers]
    channel_names = [channel.name for channel in targetchannels]
    usermessages = await bot.get_all_messages(channel_names, user_names)

    if usermessages is not None and len(usermessages) > 5:
        short = get_sub_command(message.content) == 'short'
        responses = generate_sentences_from_messages(usermessages, short)
        filtered = list(filter(lambda x: x is not None, responses))
        if len(filtered) > 0:
            output = get_random_opener(", ".join([u.mention for u in targetusers])) + "\n\n" + "\n\n".join(filtered)
        else:
            output = "Wow... I wasn't able to generate messages for " + ", ".join([u.display_name for u in targetusers])
    else:
        output = "Sorry, I don't have enough data to generate messages for " + ", ".join([u.display_name for u in targetusers])

    await message.channel.send(output)




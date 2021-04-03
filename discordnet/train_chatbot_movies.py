from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot, comparisons, response_selection
import json
import pandas as pd

__author__ = ('Brian', 'Shantz')

# movies_whitelist = ['trainspotting', 'fear and loathing in las vegas']
movies_whitelist = ['the big lebowski', 'pretty woman']

movie_id_whitelist = []
conversations = []
lines_lookup = {}

# First, get a list of movie ids we care about
with open('data/movie-dialogs/movie_titles_metadata.txt') as f:
    # loop through all lines using f.readlines() method
    for line in f.readlines():
        cols = line.split(sep=" +++$+++ ")
        title = cols[1]
        if title in movies_whitelist:
            movie_id_whitelist.append(cols[0])


with open('data/movie-dialogs/movie_conversations.txt') as f:
    # get all the conversations we care about
    for line in f.readlines():
        cols = line.split(sep=" +++$+++ ")
        movie_id = cols[2]
        if movie_id in movie_id_whitelist:
            conversations.append(cols[3])

with open('data/movie-dialogs/movie_lines.txt') as f:
    # get all the conversations we care about
    for line in f.readlines():
        cols = line.split(sep=" +++$+++ ")
        movie_id = cols[2]
        if movie_id in movie_id_whitelist:
            lines_lookup[cols[0]] = cols[4]



#
# Create a new instance of a ChatBot
chatbot = ChatBot(
        'Mort',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'statement_comparison_function': comparisons.SpacySimilarity,
                'response_selection_method': response_selection.get_random_response
            }
        ],
        database_uri='sqlite:///database.db'
    )

trainer = ListTrainer(chatbot)

for conversation in conversations:
    conversation_json = json.loads(conversation.replace("'", '"'))
    dialog_convo = [lines_lookup.get(c).rstrip("\n") for c in conversation_json]
    trainer.train(dialog_convo)




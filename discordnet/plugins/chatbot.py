'''
    Experiments in chatbot
'''

from chatterbot import ChatBot, comparisons, response_selection
# import nltk
import spacy
import os
import numpy as np
import matplotlib.pyplot as plt
import ndjson


__author__ = ('Brian', 'Shantz')

# Create a new instance of a ChatBot
chatbot = ChatBot(
        'Mort',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'statement_comparison_function': comparisons.LevenshteinDistance,
                'response_selection_method': response_selection.get_random_response,
                'default_response': 'k',
                'maximum_similarity_threshold': 0.90
            }
        ],
        database_uri='sqlite:///database.db'
    )

nlp = spacy.load("en_core_web_sm")

categories = {}


async def init():
    files = os.listdir('./data/draw/ndjson')
    for f in files:
        name = f.rstrip(".ndjson")
        categories[name] = f


async def get_keyword(text):
    doc = nlp(text)
    # Analyze syntax
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    for noun in doc.noun_chunks:
        words = noun.text.split(" ")
        for word in words:
            if word.lower() in categories:
                return categories[word.lower()]

    # Find named entities, phrases and concepts
    if len(doc.ents) > 0:
        for entity in doc.ents:
            if entity.text.lower() in categories:
                return categories[entity.text.lower()]
            elif entity.label_.lower() in categories:
                return categories[entity.label_.lower()]


async def main(bot, message, **kwargs):
    if message.channel.name == 'bot-experiments':

        # keyword = await get_keyword(message.clean_content)
        # if(keyword != None):
        #     with open('data.ndjson') as f:
        #         data = ndjson.load(f)
        #         text = ndjson.dumps(data)
        #         data = ndjson.loads(text)
        bot_response = chatbot.get_response(message.clean_content)
        if str(bot_response).replace(" ", "") != "":
            # await get_keyword(str(bot_response))
            await message.channel.send(bot_response)

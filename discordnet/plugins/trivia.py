import time
from aiohttp import ClientSession
import random
from threading import Timer

COMMAND = 'trivia'


async def request_json(url):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


class TriviaQuestion(object):
    """A Triva question with methods for server and checking answers"""

    def __init__(self, category, type, difficulty, question, correct_answer, incorrect_answers):
        self.category = category
        self.type = type
        self.difficulty = difficulty
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers

    def formatted_question(self):
        output = "Category: **" + self.category + "** \n\n"
        output += "Question: " + self.question + " \n\n"
        answers = self.incorrect_answers + [self.correct_answer]
        for index, answer in enumerate(answers):
            output += "**" + str(index) + "**: \t" + answer + "\n"
        return output


class TriviaRound(object):
    def __init__(self, questions):
        self._questions = questions
        self._remaining = questions
        self._completed = []

    def get_remaining_questions(self):
        return self._questions

    def get_completed(self):
        return self._completed

    def next_question(self):
        if len(self._remaining) >= 1:
            return self._remaining.pop()
        else:
            return None

class Player(object):
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.score = 0


class TriviaGame(object):
    def __init__(self):
        self.players = {}
        self.active = False
        self.current_round = 0
        self.rounds = []
        self.start_time = 0

    async def __load_questions(self):
        trivia_questions = []
        results = await request_json("https://opentdb.com/api.php?amount=3")
        if results['response_code'] == 0:
            for q in results['results']:
                trivia_question = TriviaQuestion(q['category'],
                                                 q['type'],
                                                 q['difficulty'],
                                                 q['question'],
                                                 q['correct_answer'],
                                                 q['incorrect_answers'])
                trivia_questions.append(trivia_question)
            return trivia_questions
        else:
            return None

    def get_question(self):
        return self.rounds[self.current_round].next_question()

    def has_questions(self):
        return len(self.rounds[self.current_round].get_remaining_questions()) > 0

    async def start(self):
        self.start_time = time.time()
        self.rounds = []
        self.rounds.append(TriviaRound(await self.__load_questions()))
        self.current_round = 0


async def countdown(bot, message_ref):
    await bot.edit_emssage(message_ref, "New Content")

trivia_game = TriviaGame()


async def main(bot, message, **kwargs):
    if not trivia_game.active:
        await trivia_game.start()
        trivia_game.active = True

    if trivia_game.has_questions():
        question = trivia_game.get_question()
        message_ref = await bot.send_message(message.channel, question.formatted_question())
    else:
        await bot.send_message(message.channel, "No More Questions... Restarting")
        trivia_game.active = False


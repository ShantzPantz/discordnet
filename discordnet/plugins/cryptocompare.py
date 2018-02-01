'''
    CryptoCompare coin data offering the current value of a coin in USD as well as the 24 hour change.
    Sub Commands:
        !coin price <coin>      - returns the price for a coin, or list of coins
        !coin add <coin>        - adds a coin to your favorites
        !coin remove <coin>     - removes a coin from your favorites
        !coin list              - Lists your current coin favorites
        !coin me                - Shows the current price info for your favorites

'''

import time
from aiohttp import ClientSession

COMMAND = 'coin'
SUB_COMMANDS = ['price', 'markets']

cached_coins = {}
usercoins = {}
last_update_time = 0
refresh_time = 60 * 5  # 5 minutes
updating = False


def index(a_list, value):
    try:
        return a_list.index(value)
    except ValueError:
        return None


async def request_json(url):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


def is_valid_coin_response(result):
    return 'Data' in result


async def get_coin_list():
    global last_update_time
    global refresh_time
    global cached_coins
    global updating
    if time.time() - last_update_time > refresh_time:
        updating = True
        last_update_time = time.time()
        result = await request_json('https://min-api.cryptocompare.com/data/all/coinlist')
        if is_valid_coin_response(result):
            cached_coins = result['Data']
        updating = False
    return cached_coins


async def get_multi_price(symbols):
    joinedsymbols = ",".join(symbols)
    return await request_json('https://min-api.cryptocompare.com/data/pricemultifull?fsyms='+joinedsymbols+'&tsyms=USD')


async def find_coin(term):
    data = await get_coin_list()
    result = next((data[coin] for coin in data
                   if data[coin]["CoinName"].lower() == term.lower()
                   or data[coin]["Symbol"].lower() == term.lower()))
    return result


def get_sub_command_content(content):
    if not content:
        return None, None
    parts = content.split(' ')
    if len(parts) > 1:
        return parts[0], parts[1:]
    else:
        return parts[0], None


async def format_price_message(prices):
    output = ''
    for key in prices:
        coin = await find_coin(key)
        fullname = coin['FullName']
        price = prices[key]['USD']['PRICE']
        change24h = prices[key]['USD']['CHANGEPCT24HOUR']
        exchange = prices[key]['USD']['LASTMARKET']
        output += key + " is currently trading at " + price + " USD.  The 24h change is " + change24h + "% (via " + exchange + ")\n"
    return output


def add_user_coins(userid, coins):
    global usercoins
    if userid not in usercoins:
        usercoins[userid] = []
    for coin in coins:
        if coin not in usercoins[userid]:
            usercoins[userid].append(coin)
    return usercoins[userid]


def remove_user_coins(userid, coins):
    global usercoins
    if userid not in usercoins:
        usercoins[userid] = []
    for coin in coins:
        coinindex = index(usercoins[userid], coin)
        if not coinindex:
            continue
        else:
            del usercoins[userid][coinindex]
    return usercoins[userid]


def get_user_coins(userid):
    global usercoins
    if userid not in usercoins or len(usercoins[userid]) == 0:
        return None
    else:
        return usercoins[userid]


async def init():
    await get_coin_list()


async def main(bot, message, **kwargs):
    global COMMAND
    global updating
    if not message:
        return
    else:
        while updating:
            print("Data is updating.. Hold on...")
            time.sleep(1)  # Delay for 1 minute (60 seconds).

        sub_command, sub_command_content = get_sub_command_content(message.content)
        print(sub_command)
        print(sub_command_content)
        symbols = []
        if sub_command is None:
            await bot.send_message(message.channel, "Run **!help "+COMMAND+"** for a list of commands.")
        elif sub_command_content is not None:
            for term in sub_command_content:
                coin = await find_coin(term)
                if not coin:
                    continue
                else:
                    symbols.append(coin['Symbol'])

        if sub_command == 'remove' or sub_command == 'removecoin':
            remove_user_coins(message.author.id, symbols)
        elif sub_command == 'add' or sub_command == 'addcoins':
            add_user_coins(message.author.id, symbols)
        elif sub_command == 'list':
            if message.author.id not in usercoins:
                await bot.send_message(message.channel, message.author.name + ", you do not have any coins set. run !c setcoins <coin> <coin2> <etc..>")
            else:
                symbols = get_user_coins(message.author.id)
                await bot.send_message(message.channel, message.author.name +", your coins are: " + ", ".join(symbols))
        elif sub_command == 'coins' or sub_command == 'me':
            if message.author.id not in usercoins:
                await bot.send_message(message.channel, message.author.name + ", you do not have any coins set. run !c setcoins <coin> <coin2> <etc..>")
            else:
                symbols = get_user_coins(message.author.id)
                prices = await get_multi_price(symbols)
                response = await format_price_message(prices['DISPLAY'])
                await bot.send_message(message.channel, response)
        elif sub_command == 'price':
            prices = await get_multi_price(symbols)
            response = await format_price_message(prices['DISPLAY'])
            await bot.send_message(message.channel, response)



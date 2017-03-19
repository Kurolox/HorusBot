import discord
import logging
from credentials import token

# Enable logging
logging.basicConfig(level=logging.INFO)

bot_client = discord.Client()

@bot_client.event
async def on_ready():
    print('Logged in as')
    print(bot_client.user.name)
    print(bot_client.user.id)
    print('------')


@bot_client.event
async def on_message(msg):
    print('MSG: ' + msg.content)
    if msg.content.startswith('!test'):
        await bot_client.send_message(msg.channel, 'Test received!')
    elif msg.content.startswith('<@291477047962763264>'):
        code = check_code(msg.content)
        if not code:
            await bot_client.send_message(msg.channel, "There's no code to run.")
        else:
            print(code)
            lang = check_lang(msg.content)
            if not lang:
                await bot_client.send_message(msg.channel, "The language wasn't specified.")
            else:
                # TODO: Run code
                return 0
        #TODO: Research how to sandbox a python program


def check_code(message):
    try:
        primitive_code = message.split("```")[1]
    except IndexError:
        return 0
    print(primitive_code)
    return primitive_code.split("\\n")




def check_lang(message):
    return 0
    # TODO: Split message into args and syntax markdown

    # TODO: Check if it's using one of them, or both at the same time

    # TODO: Return the lang

bot_client.run(token)

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
    if msg.content.startswith('!test'):  # Test function
        await bot_client.send_message(msg.channel, 'Test received!')
    elif msg.content.startswith('<@291477047962763264>'):  # Toggled when the bot is mentioned
        code = check_code(msg.content)
        if not code:
            await bot_client.send_message(msg.channel, "There's no code to run.")
        else:
            lang, code = check_lang(msg.content, code)
            if not lang:
                await bot_client.send_message(msg.channel, "The language wasn't specified.")
            else:
                await bot_client.send_message(msg.channel, "Running %s code." % lang)
                # TODO: Run code

            await bot_client.send_message(msg.channel, code)
        # TODO: Research how to sandbox a python program


def check_code(message):
    '''Checks if the message actually does have code to run'''
    try:
        primitive_code = message.split("```")[1]
    except IndexError:
        return 0
    return primitive_code.split("\n")


def check_lang(message, code):
    '''Checks if there's an argument or a language specified in the code.'''
    compatible_languages = {
            "Python": ("python", "py", "pycode")}
    detected_lang = ""
    try:
        argument = message.split("```")[0].split(" ")[1]  # Checks argument
    except IndexError:
        argument = ""
    for language, diff_naming in compatible_languages.items():
        if argument.lower() in diff_naming:
            detected_lang = language

    if code[0] == "":
        if detected_lang != "":
            return detected_lang, code
        else:
            return 0, code
    else:
        for language, diff_naming in compatible_languages.items():
            if code[0] in diff_naming:
                print("Break B")
                detected_lang = language
                code[0] = ""
                return detected_lang, code
    print("Break C")
    return 0, code

    # TODO: Split message into args and syntax markdown

    # TODO: Check if it's using one of them, or both at the same time

    # TODO: Return the lang


bot_client.run(token)

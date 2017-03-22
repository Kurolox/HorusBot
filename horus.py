import discord
from subprocess import Popen, PIPE, TimeoutExpired
import logging
from sys import path
from credentials import token
from datetime import datetime

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
    with open("botlog", "a") as log:
        log.write("%s %s MSG: %s\n" % (datetime.now(), msg.author, msg.content))
        print("%s %s MSG: %s\n" % (datetime.now(), msg.author, msg.content))
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
                filename = build_exec(lang, code)
                print(filename)
                output, error, loop_flag = run_code(lang, filename)
                if error:
                    await bot_client.send_message(msg.channel, "The bot has encountered the following error when running your %s code. \n```\n%s```" % (lang, error))
                elif loop_flag:
                    await bot_client.send_message(msg.channel, "I'm sorry, but your request took too long. Here are the last 5 lines from the output.\n```\n%s```" % output)
                else:
                    await bot_client.send_message(msg.channel, "Here's the output of your %s code. \n```\n%s```" % (lang, output))

                # TODO: Run code
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
                detected_lang = language
                code[0] = ""
                return detected_lang, code
    return 0, code


def build_exec(lang, code):
    """Creates a file with the provided code in it."""
    lang_to_filetype = {
        "Python": ".py"}
    date = str(datetime.now())
    filename = "%s/%s/%s%s" % (path[0], lang, date.replace(" ", "--"), lang_to_filetype[lang])
    with open(filename, "a") as file:
        for line in code:
            file.write("%s\n" % line)
    return filename


def run_code(lang, filename):
    # Still WIP.
    loop_flag = 0
    if lang == "Python":
        process = Popen(["python", filename], stdout=PIPE, stderr=PIPE)
        try:
            stdout, stderr = process.communicate(timeout=6)
        except TimeoutExpired:
            line_number = 5
            stderr = b""
            stdout = b""
            while line_number > 0:
                stdout += process.stdout.readline()
                print(stdout)
                line_number -= 1
            loop_flag = 1
            # TODO: Make it return the last 5 lines of output instead.
        return stdout.decode("utf-8"), stderr.decode("utf-8"), loop_flag


bot_client.run(token)

import discord
import logging

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
        try: 
            syntax_language = str(msg.content.split(' ')[1])
        except IndexError:
            await bot_client.send_message(msg.channel, "You need to specify the syntax language if you want me to run it!")
        print(syntax_language)
        print(msg.content.split('```'))
        
        #TODO: Research how to sandbox a python program

        await bot_client.send_message(msg.channel,'```%s```' % msg.content.split('```')[1])


bot_client.run('')

# A fun meme Discord bot that can store and echo quotes from a
# live database!
#TODO: more description here

import discord
import re


# Store user-quote pairs in a growing database
database = { }


# Initialize Discord client and log-in the bot
client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


# Channel message handler
@client.event
async def on_message(message):
    # Do nothing for the bot's own messages.
    if (message.author == client.user):
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
        

# Get locally-stored bot token and run
# (Assume token stored in directory in bot_token.txt)
with open("bot_token.txt", "r") as reader:
    bot_token = reader.readline()
    
client.run(bot_token)




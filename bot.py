# A fun meme Discord bot that can store and echo quotes from a
# live database!
#TODO: more description here

import discord
import random
#import re


# Store user-quote pairs in a growing database
database = {
    "one": "blahblahblah",
    "two": "eqrewrewqtegasd",
}


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

    # On $hello, print a helpful list of the bot's commands
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    # On $store, store the quoted message to the database
    if ("$store" in message.content):
        # Check that there was a quote

        # Check that there was an attribution (how to get the ID
        # given the mention? Is there a way to query the channel?)
        
        await message.channel.send(
            "Here is where I'd store a quote!"
        )

    # On $random, return a random quote divorced of any context
    if message.content.startswith("$random"):
        await message.channel.send(random.choice(list(database.values())))

    # On $debug, echo the raw text of the message that the bot sees
    if ("$debug" in message.content):
        await message.channel.send(
            "RAW:\n```text\n{}\n```".format(message.content)
        )
        

# Get locally-stored bot token and run
# (Assume token stored in directory in bot_token.txt)
with open("bot_token.txt", "r") as reader:
    bot_token = reader.readline()
    
client.run(bot_token)




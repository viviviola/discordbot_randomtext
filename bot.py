# A fun meme Discord bot that can store and echo quotes from a
# live database!
#TODO: more description here

import discord
import random
import re


# Store user-quote pairs in a growing database
database = { }


# Given a Discord message string containing a quote, parse and
# return the quoted text and the attributed user ID.
#
# @param message A string containing the raw text of the message.
# @return A list containing the user ID and their quote string, in
#     that order.
def parse_quoted_message(message):
    message = message.splitlines()
    
    # All of the lines following a ">" are part of the quote
    quoted_lines = list(filter(lambda line: line.startswith(">"), message))
    quote = "\n".join(map(lambda line: line.replace("> ", ""), quoted_lines)) 
    
    # Assume the attributed user is the first mention directly
    # following the first quoted text.
    other_lines = list(filter(lambda line: not(line.startswith(">")), message))
    rest_of_message = "\n".join(other_lines)
    user = re.findall(r"(?<=\<@!)\d+", rest_of_message)[0]

    return [user, quote]


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

    # On $help, print a helpful list of the bot's commands
    if message.content.startswith("$help"):
        await message.channel.send("TODO")

    # On $hello, say a nice greeting
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
        
    # On $store, store the quoted message to the database
    if ("$store" in message.content):
        user, quote = parse_quoted_message(message.content)
        database[user] = quote
        
        await message.channel.send(
            "I saw <@!{}> say\n{}\n\n Stored!".format(
                user,
                "> " + quote.replace("\n", "\n> ")
            )
        )

    # On $random, return a random quote divorced of any context
    if message.content.startswith("$random"):
        quotes = list(database.values())
        if (not quotes):
            await message.channel.send("I don't have any quotes stored yet!")
        else:
            await message.channel.send(random.choice(quotes))

    # On $debug, echo the raw text of the message that the bot sees
    if ("$debug" in message.content):
        print(message.content)
        await message.channel.send(
            "RAW:\n```text\n{}\n```".format(message.content)
        )
        

# Get locally-stored bot token and run
# (Assume token stored in directory in bot_token.txt)
with open("bot_token.txt", "r") as reader:
    bot_token = reader.readline()
    
client.run(bot_token)




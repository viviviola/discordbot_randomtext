# A fun meme Discord bot that can store and echo quotes from a
# live database!
#TODO: more description here

import discord
import pickle

from collections import defaultdict
from itertools import chain
from os import path
from random import choice
from re import findall


# Store user-quote pairs in a growing database
database = defaultdict(set)


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
    quote = "\n".join(map(lambda line: line[2:], quoted_lines)) 
    
    # Assume the attributed user is the first mention directly
    # following the first quoted text.
    other_lines = list(filter(lambda line: not(line.startswith(">")), message))
    rest_of_message = "\n".join(other_lines)

    # User IDs will have an exclamation mark prefix if they are using a
    # server nickname apparently
    # TODO: Fix this up? It's kind of ugly.
    mentions = findall(r"(?<=\<@)\d+", rest_of_message) \
               + findall(r"(?<=\<@!)\d+", rest_of_message)
    print(str(mentions))  # DEBUG
    user = mentions[0]

    return [user, quote]


# Initialize Discord client and log-in the bot. Reads in a local
# database of quotes if available (assume they are stored in
# database.txt).
client = discord.Client()

@client.event
async def on_ready():
    # Read in the local database of quotes if it exists
    # TODO: Binary for now, but might want human-readable text?
    if (path.exists("database.ser")):
        global database
        with open("database.ser", "rb") as database_file:
            database = pickle.loads(database_file.read())

        # DEBUG: print contents of the database to console
        print("Local database file:\n{}".format(str(database)))

    # DEBUG: Successful login
    print("Logged in as {0.user}".format(client))


# Channel message handler
@client.event
async def on_message(message):
    # Do nothing for the bot's own messages.
    if (message.author == client.user):
        return

    # On $help, print a helpful list of the bot's commands
    if (message.content.startswith("$help")):
        await message.channel.send("TODO")

    # On $hello, say a nice greeting
    if (message.content.startswith("$hello")):
        await message.channel.send("Hello!")
        
    # On $store, store the quoted message to the database
    if ("$store" in message.content):
        user, quote = parse_quoted_message(message.content)
        database[user].add(quote)
        
        await message.channel.send(
            "I saw <@!{}> say\n{}\n\n Stored!".format(
                user,
                "> " + quote.replace("\n", "\n> ")
            )
        )

    # On $random, return a random quote divorced of any context
    if (message.content.startswith("$random")):
        quotes = list(chain(*database.values()))
        if (not quotes):
            await message.channel.send("I don't have any quotes stored yet!")
        else:
            await message.channel.send(choice(quotes))

    # On $debug, echo the raw text of the message that the bot sees
    if ("$debug" in message.content):
        print(message.content)
        await message.channel.send(
            "RAW:\n```text\n{}\n```".format(message.content)
        )

    # On $dumpdatabase, dump the entire database listing as a message
    # (Eventually disable this so we don't trip the message
    # character limit)
    if ("$dumpdatabase" in message.content):
        # Write database?
        with open("database.ser", "wb") as database_file:
            pickle.dump(database, database_file)
        
        print(str(database))
        await(message.channel.send(str(database)))

    # On $exit, gracefully disconnect from the server
    if ("$shutdown" in message.content):
        await client.close()


# When the bot disconnects/log out, store the database locally
@client.event
async def on_disconnect():
    # Store the live database to a local file
    # TODO: Apparently this function can be called many times
    # (simultaneously?). Might need a mutex to make sure the data
    # doesn't get corrupted or something?    
    with open("database.ser", "wb") as database_file:
        pickle.dump(database, database_file)


# Get locally-stored bot token and run
# (Assume token stored in directory in bot_token.txt)
with open("bot_token.txt", "r") as reader:
    bot_token = reader.readline()
    
client.run(bot_token)

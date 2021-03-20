# Import dependencies. The "discord" and "mysql.connector" modules may say they're not in use, but they are.
import discord
import json
import random
import time
import mysql.connector
import validators

# Load the configuration file.
with open('./storage/config.json') as f:
    config = json.load(f)

"""
Define variables possible at the beginning.

Most database and config variables are listed here.
"""



prefix = config.get("prefix")

mydb = mysql.connector.connect(
  host=config.get("db_host"),
  user=config.get("db_user"),
  password=config.get("db_password"),
  database=config.get("db_database")
)

mycursor = mydb.cursor()

#myresult = mycursor.fetchone()

log_channel = None

client = discord.Client()

def check_if_blacklisted(user):
    """Checks if a user is blacklisted based on blacklisted_users.txt
    
    Parameters:
    user - The user to check, their ID.

    Returns:
    blacklisted - a boolean which is True or False if they are blacklisted.
    """
    blacklisted = False
    with open('./storage/blacklisted_users.txt', "r") as f:
        blacklisted_users = f.read().split(";")
        for i in range(len(blacklisted_users)):
            if(blacklisted_users[i] == user):
                blacklisted = True
                return blacklisted
            else:
                continue
    return blacklisted
def filter_message(orig):
    """Filters out an input based on banned_words.txt.
    
    Parameters:
    orig - The original input.

    Returns:
    filtered - A string that has been filtered out.
    """
    with open('./storage/banned_words.txt', "r") as f:
        banned_words = f.read().split(";")
        filtered = orig
        for i in range(len(banned_words)): # Loops through all banned words and replaces in string
            filtered = filtered.replace(banned_words[i], "")
    return filtered

@client.event
async def on_ready():
    print('Currently online!')
    await client.change_presence(activity=discord.Streaming(name= prefix + "help", url="https://twitch.tv/NateTheCarrot"))
    global log_channel
    log_channel = client.get_channel(config.get("logs_id"))

@client.event
async def on_message(message):
    if(message.author.bot or check_if_blacklisted(str(message.author.id))): # Check if the author of the message is a bot or is blacklisted
        return # Return will always be used to make sure to not continue in the code, as it isn't needed.
    msg = message.content.lower()
    if(msg == prefix + "add"):
        mycursor.execute("SELECT * FROM allowed_channels WHERE channel_id = " + str(message.channel.id))
        myresult = mycursor.fetchone()
        if(myresult == None): # Essentially saying "if the channel isn't in the database"
            sql = "INSERT INTO allowed_channels (channel_id, allowed) VALUES (%s, %s)"
            val = (str(message.channel.id), 1)
            mycursor.execute(sql, val)
            mydb.commit() # Push the changes to the database
            # Also, f strings help a lot with not having to use + prefix + all the time.
            await message.channel.send(f"Successfully made this channel a conversating channel. If I react with \"🧠\" (if I have permissions), that means I don't know what that phrase is. If you see it, please run the `{prefix}addphrase` command. \n\nTo use it, type `{prefix}addphrase <original phrase>; <response>`. Make sure there is a space between the semicolon and the new reply.\n**Example:** `{prefix}addphrase How's the weather?; Very sunny!`")
        elif(myresult[2] == 1):
            await message.channel.send(f"Sorry, this is already a conversating channel. If you would like to remove it as a conversating channel, run the `{prefix}!remove` command.")
            return
        else:
            await message.channel.send(f"Successfully made this channel a conversating channel. If I react with \"🧠\" (if I have permissions), that means I don't know what that phrase is. If you see it, please run the `qtaddphrase` command. \n\nTo use it, type `{prefix}addphrase <original phrase>; <response>`. Make sure there is a space between the semicolon and the new reply.\n**Example:** `{prefix}addphrase How's the weather?; Very sunny!`")
            mycursor.execute("UPDATE allowed_channels SET allowed = 1 WHERE channel_id = " + str(message.channel.id))
            mydb.commit()
            return
        return


    if(msg == prefix + "remove"):
        mycursor.execute("UPDATE allowed_channels SET allowed = 0 WHERE channel_id = " + str(message.channel.id)) # Does not return an error if the channel doesn't exist in the database.
        mydb.commit()
        await message.channel.send("Successfully made this a non-conversating channel.")
        return


    if(msg == prefix + "init"):
        if(str(message.author.id) != config.get("owner_id")): # Make sure it is the owner of the bot running the command
            return
        else:
            await message.channel.send("**ONLY USE THIS COMMAND ONCE PER INITIALIZATION!**\n\nIf you deleted the messages table and readded it, then you may run this command again.")
            mycursor.execute("INSERT INTO messages (sentences, replies) VALUES (\"hello\", \"hey, hi, hello, what's up\")")
            mycursor.execute("INSERT INTO messages (sentences, replies) VALUES (\"hi\", \"hey, hi, hello, what's up\")")
            mycursor.execute("INSERT INTO messages (sentences, replies) VALUES (\"hey\", \"hey, hi, hello, what's up\")")
            mycursor.execute("INSERT INTO messages (sentences, replies) VALUES (\"what's up\", \"hey, hi, hello, what's up\")")
            mycursor.execute("INSERT INTO messages (sentences, replies) VALUES (\"what's your name\", \"charles, mary, ymir, henrick\")")
            mydb.commit()


    if(msg.startswith(prefix + "addphrase")):
        if("@" in msg):
            return
        word = msg.split("; ")
        word[0] = word[0].replace(prefix + "addphrase ", "") # Separate it into the original word and the new reply
        mycursor.execute("SELECT * FROM messages WHERE sentences = '" + str(filter_message(word[0])) + "'")
        myresult = mycursor.fetchone()
        if(myresult != None): # If it can find the original word
            if(word[1] not in myresult[2]): # If the reply doesn't already exist
                mycursor.execute("UPDATE messages SET replies = '" + myresult[2] + ", " + filter_message(word[1]) + "' WHERE sentences = '" + filter_message(word[0]) + "'")
                mydb.commit()
                await message.channel.send("Successfully added reply, thanks for contributing!")
                await log_channel.send("<@" + str(message.author.id) + "> added phrase \"*" + filter_message(word[1]) + "*\" to **" + filter_message(word[0]) + "**")
                return;
            else: # If the reply is there
                await message.channel.send("That reply is already added to the list of replies for that word.")
                return;
        else: # If the original word doesn't exist
            sql = "INSERT INTO messages (sentences, replies) VALUES (%s, %s)"
            val = (filter_message(word[0]), filter_message(word[1]))
            mycursor.execute(sql, val)
            mydb.commit()
            await message.channel.send("Successfully added reply, thanks for contributing!")
            await log_channel.send("<@" + str(message.author.id) + "> added phrase \"*" + filter_message(word[1]) + "*\" to **" + filter_message(word[0]) + "**")
            return;
        return;

    if(msg == prefix + "help"):
        await message.channel.send(f"**Commands:**\n__{prefix}add__ - Allows the channel the command is used in to participate in the bot (have the bot conversate)\n__{prefix}remove__ - Disallows the bot to conversate in the channel the command is used in.\n__{prefix}addphrase <original phrase>; <response>__ - Lets you add a new phrase to the bot. (Example: `{prefix}addphrase How's the weather?; Very sunny!`)\n__{prefix}init__ - Initializes the database by adding a few premade sentences and replies. Should only be run once! Can only be run by the bot owner.")
    mycursor.execute("SELECT * FROM allowed_channels WHERE channel_id = " + str(message.channel.id))
    myresult = mycursor.fetchone()
    if(myresult[2] != 0): # If it can go in the channel
        mycursor.execute("SELECT * FROM messages WHERE sentences = '" + filter_message(msg) + "'")
        myresult = mycursor.fetchone()
        if(myresult != None):
            replies_to_use = myresult[2].split(", ")
            true_reply = random.choice(replies_to_use) # random.choice() is very useful for what I'm trying to do, select a random value from an array.
            if(validators.url(true_reply)):
                await message.channel.send(true_reply)
                return
            else:
                async with message.channel.typing(): # Occasionally will duplicate the typing if server connection issues occur - EDIT: Still may happen if connection errors occur, but too a much less degree.
                    time.sleep(len(true_reply) / 10) # / 10 to make it more realistic (and faster). That means a 10 letter word would take 10 seconds to type.
                await message.channel.send(true_reply)
                return

        else:
            await message.add_reaction("🧠")
    else:
        return
client.run(config.get("token"))
import discord
import json
import random
import time
import mysql.connector

with open('./storage/config.json') as f:
    config = json.load(f)

prefix = config.get("prefix")

mydb = mysql.connector.connect(
  host=config.get("db_host"),
  user=config.get("db_user"),
  password=config.get("db_password"),
  database=config.get("db_database")
)

mycursor = mydb.cursor()

myresult = mycursor.fetchone()

client = discord.Client()
def filter_message(orig):
    with open('./storage/banned_words.txt', "r") as f:
        banned_words = f.read().split(";")
        filtered = orig
        for i in range(len(banned_words)):
            filtered = filtered.replace(banned_words[i], "")
    return filtered
@client.event
async def on_ready():
    print('Currently online!')
@client.event
async def on_message(message):
    if(message.author.bot):
        return
    msg = message.content.lower()
    if(msg == prefix + "add"):
        mycursor.execute("SELECT * FROM allowed_channels WHERE channel_id = " + str(message.channel.id))
        myresult = mycursor.fetchone()
        if(myresult == None):
            sql = "INSERT INTO allowed_channels (channel_id, allowed) VALUES (%s, %s)"
            val = (str(message.channel.id), 1)
            mycursor.execute(sql, val)
            mydb.commit()
            await message.channel.send("Successfully made this channel a conversating channel. If I react with \"🧠\" (if I have permissions), that means I don't know what that phrase is. If you see it, please run the `qt!addword` command. \n\nTo use it, type `qt!addword <original phrase>; <response>`. Make sure there is a space between the semicolon and the new reply.\n**Example:** `qt!addword How's the weather?; Very sunny!`")
        else:
            await message.channel.send("Sorry, this is already a conversating channel. If you would like to remove it as a conversating channel, run the `qt!remove` command.")
        return


    if(msg == prefix + "remove"):
        mycursor.execute("UPDATE allowed_channels SET allowed = 0 WHERE channel_id = " + str(message.channel.id))
        mydb.commit()
        await message.channel.send("Successfully made this a non-conversating channel.")
        return


    if(msg == prefix + "init"):
        if(str(message.author.id) != config.get("owner_id")):
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
        word = msg.split("; ")
        word[0] = word[0].replace("qt!addphrase ", "")
        mycursor.execute("SELECT * FROM messages WHERE sentences = '" + str(filter_message(word[0])) + "'")
        myresult = mycursor.fetchone()
        if(myresult != None):
            if(word[1] not in myresult[2]):
                mycursor.execute("UPDATE messages SET replies = '" + myresult[2] + ", " + filter_message(word[1]) + "' WHERE sentences = '" + filter_message(word[0]) + "'")
                mydb.commit()
                return;
            else:
                await message.channel.send("That reply is already added to the list of replies for that word.")
                return;
        else:
            sql = "INSERT INTO messages (sentences, replies) VALUES (%s, %s)"
            val = (filter_message(word[0]), filter_message(word[1]))
            mycursor.execute(sql, val)
            mydb.commit()
            return;
        return;

    mycursor.execute("SELECT * FROM allowed_channels WHERE channel_id = " + str(message.channel.id))
    myresult = mycursor.fetchone()
    if(myresult != None):
        mycursor.execute("SELECT * FROM messages WHERE sentences = '" + filter_message(msg) + "'")
        myresult = mycursor.fetchone()
        if(myresult != None):
            replies_to_use = myresult[2].split(", ")
            true_reply = random.choice(replies_to_use)
            async with message.channel.typing():
                time.sleep(len(true_reply) / 5)
            await message.channel.send(true_reply)
        else:
            await message.add_reaction("🧠")
    else:
        return
client.run(config.get("token"))
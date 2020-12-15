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

@client.event
async def on_ready():
    print('Currently online!')
@client.event
async def on_message(message):
    msg = message.content.lower()
    if(msg == prefix + "add"):
        #with open('./storage/addchannel.sql') as f:
            #cursor.execute(f.read().decode('utf-8'), multi=True) # More efficient to do this with a file rather than a line.
        sql = "INSERT IGNORE INTO allowed_channels SET (channel_id, allowed) VALUES (%s, %s);"
        val = (str(message.channel.id), 1)
        mycursor.execute(sql, val, multi=True)
        mydb.commit()
        await message.channel.send("Successfully made this channel a conversating channel.")
        return
    if(msg == prefix + "remove"):
        mycursor.execute("UPDATE allowed_channels SET allowed = 0 WHERE channel_id = " + str(message.channel.id))
        mydb.commit()
        await message.channel.send("Successfully made this a non-conversating channel.")
        return
client.run(config.get("token"))
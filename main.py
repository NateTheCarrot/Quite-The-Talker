import discord
import json
import random
import time
import mysql.connector

with open('./storage/config.json') as f:
    config = json.load(f)

mydb = mysql.connector.connect(
  host=config.get("db_host"),
  user=config.get("db_user"),
  password=config.get("db_password"),
  database=config.get("db_database")
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS allowed_channels (id TINYTEXT, allowed BOOL);") # TINYTEXT to make sure there are no incompatibilities with types.
mycursor.execute("CREATE TABLE IF NOT EXISTS lines (sentences TEXT, replies LONGTEXT);") # Currently not working. Program thinks "lines" is part of the "CREATE TABLE".

myresult = mycursor.fetchone()

client = discord.Client()

@client.event
async def on_ready():
    print('Currently online!')
async def on_message(message):
    msg = message.content.lower()
client.run(config.get("token"))
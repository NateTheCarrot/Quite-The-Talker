import discord
import json
import random
import time

client = discord.Client()

with open('./config.json') as f:
    config = json.load(f)

client.run(config.get("token"))
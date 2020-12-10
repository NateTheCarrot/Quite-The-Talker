import discord
import json
import random
import time

with open('./config.json') as f:
    config = json.load(f)
print(config.get("name")) # w
# Quite the Talker

A unique chatting bot for discord.

## Description

"Quite the Talker" is a Discord bot that utilizes a database to store replies and sentences. When activated in a channel, it will talk normally based on what the community decides. For example, if the users want a reply to their "What's up?" with "Nothing much.", then the bot will store that in the database. Everything in the database can easily be edited.
**Official Bot Invite**: https://discord.com/oauth2/authorize?client_id=786626995755810897&permissions=67648&scope=bot

## Get Started

### Dependencies

* Python 3.7+
* MySQL
* Optional: DBeaver

* discord.py module
* json module
* random module
* time module
* mysql.connector module
* validators module
### Installing

Press the "Code" button, and either clone it with the provided HTTPS/SSH links or download the ZIP file.
![Code Image](https://i.imgur.com/d1vi6PK.png)

[Make sure to link the .sql files to a database you create.](https://www.youtube.com/watch?v=C9AGrSJ6ZB0)
Make a copy of the config.example.json file named "config.json". Move this to the storage folder, and put in your details in the respective places. Also, if you want to add banned words, go to the banned_words.txt file and add ";yourphrasehere". The values are separated by semicolons. After this, make sure to run the "creation.sql" file. When working (running in the console), run the `prefix!init` command to add samples to your database. `prefix!add` will add the channel to a list of channels that the bot can work on, and `prefix!remove` will remove the channel.

### Executing Program

* Enter the file path to the main.py file (i.e. cd C:\Users\Me\Desktop\Bot\)
* Run "python main.py". This should run without any other steps or errors. If you do get errors, please see the next section.

## Help

Most errors will be caused by database connections. There are a few things you could do.

* Make sure your SQL files are actually connected to the database. In DBeaver, you can see in the top right if you are connected to a database and host. If any of these are N/A, then you will need to select the proper item.
![DBeaver Connections](https://i.imgur.com/ZxT7yoS.png)
* Make sure your "config.json" file is in the correct spot (in /storage/), and has all the correct information.
* Any other errors that you can't resolve? Feel free to contact me at iamnatej@gmail.com, and I'll try my best to help you.

## License

This repository is under BY-NC.

## Authors

Nathan Jimenez - iamnatej@gmail.com

## Credits

Lots of thanks for https://www.w3schools.com/ . They helped a lot in helping me prepare and work through the project.
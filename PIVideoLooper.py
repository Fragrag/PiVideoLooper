import os
import json

with open('config.json') as configfile:
    config = json.load(configfile)


command = "omxplayer"

if config["subtitles"] == True:
    command = command + "--subtitles " + config["subtitlesLocation"]

if config["loop"] == True:
    command = command + "--loop "

if config["noInterface"] == True:
    command = command + "--no-osd "

command = command + " " + config['commandLine'] + " \"" + config['fileLocation'] + "\""


print(command)

# os.system("command")
import subprocess
import json

with open('config.json') as configfile:
    config = json.load(configfile)

command = ["omxplayer"]

if config["subtitles"] == True:
    command.append("--subtitles" + config["subtitlesLocation"])
if config["loop"] == True:
    command.append("--loop")
if config["noInterface"] == True:
    command.append("--no-osd")

command.append(config['fileLocation'])

print(command)

omxprocess = subprocess.Popen(command, stdin=subprocess.PIPE)
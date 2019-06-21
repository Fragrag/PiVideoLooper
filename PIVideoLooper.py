import subprocess
import json
from os.path import dirname, join

abspath = dirname(__file__)

with open(join(abspath, 'config.json')) as configfile:
    print("JSON File loaded at " + join(abspath, 'config.json'))
    config = json.load(configfile)

command = ["omxplayer"]

if config["subtitles"] == True:
    command.append("--subtitles" + join(abspath, config["subtitlesLocation"]))
if config["loop"] == True:
    command.append("--loop")
if config["noInterface"] == True:
    command.append("--no-osd")

command.append(join(abspath, config['fileLocation']))

print("Running command with parameters:")
print(command)

#omxprocess = subprocess.Popen(command, stdin=subprocess.PIPE)
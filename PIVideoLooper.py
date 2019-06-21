import subprocess
import json
from os.path import dirname, join

abspath = dirname(__file__)

# Loads the config
with open(join(abspath, 'config.json')) as configfile:
    print("JSON File loaded at " + join(abspath, 'config.json'))
    config = json.load(configfile)

# Sets the base command, i.e. the video player
command = ["omxplayer"]

# Goes through the booleans in the config and appends the appropriate argument
if config["subtitles"] == True:
    command.append("--subtitles" + join(abspath, config["subtitlesLocation"]))
if config["loop"] == True:
    command.append("--loop")
if config["noInterface"] == True:
    command.append("--no-osd")

# Custom arguments are added
if len(config['commandLine']) != 0:
    command.append(config['commandLine'])

# Finally append the file location of video
command.append(join(abspath, config['fileLocation']))

print("Running command with parameters:")
print(command)
omxprocess = subprocess.Popen(command, stdin=subprocess.PIPE)
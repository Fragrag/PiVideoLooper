import subprocess
import json
import os.path

abspath = os.path.dirname(__file__)
config_file = os.path.join(abspath, 'config.json')

class Config:
    def __init__(self, config_location):
        with open(config_location) as configfile:
            config = json.load(configfile)

        self.file_location = config['fileLocation']        
        self.command_line = config['commandLine']
        self.subtitles = config['subtitles']
        self.subtitles_location = config['subtitlesLocation']
        self.loop = config['loop']
        self.no_interface = config['noInterface']

def restart_pi():
    command = ['reboot now']
    with open(os.path.join(abspath, 'log.txt'),'wb') as out, open(os.path.join(abspath, 'errorlog.txt'),'wb') as err:
        subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err)

def read_config():
    return Config(config_file)
    
def write_config(config_object):
    pass

def launch_video():
    # Loads the config
    with open(config_file) as configfile:
        print('JSON File loaded at ' + config_file)
        config = json.load(configfile)

    # Sets the base command, i.e. the video player
    command = ['omxplayer']

    # Goes through the booleans in the config and appends the appropriate argument
    if config['subtitles'] == True:
        command.append('--subtitles ' + os.path.join(abspath, config['subtitlesLocation']))
    if config['loop'] == True:
        command.append('--loop')
    if config['noInterface'] == True:
        command.append('--no-osd')

    # Custom arguments are added
    if len(config['commandLine']) != 0:
        command.append(config['commandLine'])

    # Finally append the file location of video
    command.append(os.path.join(abspath, config['fileLocation']))

    print('Running command with parameters:')
    print(command)

    with open(os.path.join(abspath, 'log.txt'),'wb') as out, open(os.path.join(abspath, 'errorlog.txt'),'wb') as err:
        subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err)

def kill_video():
    command = "killall omxplayer"
    with open(os.path.join(abspath, 'log.txt'),'wb') as out, open(os.path.join(abspath, 'errorlog.txt'),'wb') as err:
        subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err)

def restart_video():
    kill_video()
    launch_video()

if __name__ == "__main__":
    launch_video()
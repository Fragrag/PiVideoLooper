import subprocess
import json
import os

ABSPATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(ABSPATH, 'config.json')

class Config:
    def __init__(self, _config_location=None):
        self.config_location = _config_location
        if self.config_location != None:
            with open(self.config_location) as configfile:
                config = json.load(configfile)
                print(config)

            self.file_location = config['fileLocation']        
            self.command_line = config['commandLine']
            self.subtitles = config['subtitles']
            self.subtitles_location = config['subtitlesLocation']
            self.loop = config['loop']
            self.no_interface = config['noInterface']

    def refresh_config(self):
        with open(self.config_location) as configfile:
            config = json.load(configfile)

        self.file_location = config['fileLocation']        
        self.command_line = config['commandLine']
        self.subtitles = config['subtitles']
        self.subtitles_location = config['subtitlesLocation']
        self.loop = config['loop']
        self.no_interface = config['noInterface']

    def write_config(self):
        data = []
        data.append({
            'fileLocation': self.file_location,
            'commandLine': self.command_line,
            'subtitles': self.subtitles,
            'subtitlesLocation': self.subtitles_location,
            'loop': self.loop,
            'noInterface': self.no_interface
        })

        with open(self.config_location, 'w') as configfile:
            print(json.dump(data[0], configfile))

def get_file_list():
    """
    Get the list of files in the content folder

    :return: List of files in content folder
    """
    return [f for f in os.listdir(ABSPATH + '/content/') if os.path.isfile(os.path.join(ABSPATH + '/content/', f))]

def launch_video():
    """
    Loads the settings from the config file and launches omxplayer with appropriate settings
    """
    # Loads the config
    config = Config(CONFIG_FILE)

    # Sets the base command, i.e. the video player
    command = ['omxplayer']

    # Goes through the booleans in the config and appends the appropriate argument
    if config.subtitles == True:
        command.append('--subtitles ' + os.path.join(ABSPATH, config.subtitles_location))
    if config.loop == True:
        command.append('--loop')
    if config.no_interface == True:
        command.append('--no-osd')

    # Custom arguments are added
    if len(config.command_line) != 0:
        command.append(config.command_line)

    # Finally append the file location of video
    command.append(os.path.join(ABSPATH, config.file_location))

    print('Running command with parameters:')
    print(command)
    subprocess.run(command)

def kill_video():
    """
    Kills omxplayer
    """
    command = ['killall', 'omxplayer']
    subprocess.run(command)

def restart_video():
    """
    Kills omxplayer followed by launching it again
    """
    kill_video()
    launch_video()

def reboot():
    """
    Reboots the Pi or system running PiVideoLooper
    """
    command = ['reboot', 'now']
    subprocess.run(command)

    # with open(os.path.join(abspath, 'log.txt'),'wb') as out, open(os.path.join(abspath, 'errorlog.txt'),'wb') as err:
    #     subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err)

def echo(msg):
    print(msg)

if __name__ == "__main__":
    print(get_file_list())
    launch_video()
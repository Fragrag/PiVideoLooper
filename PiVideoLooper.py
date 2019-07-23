import subprocess
import json
import os

ABSPATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(ABSPATH, 'config.json')
CONTENT_FOLDER = ABSPATH + '/content/'

class Config:
    def __init__(self, _CONFIG_FILE=None):
        self.CONFIG_FILE = _CONFIG_FILE
        if self.CONFIG_FILE != None:
            with open(self.CONFIG_FILE) as config_file:
                config = json.load(config_file)
                print(config)

            self.file_location = config['fileLocation']        
            self.command_line = config['commandLine']
            self.subtitles = config['subtitles']
            self.subtitles_location = config['subtitlesLocation']
            self.loop = config['loop']
            self.no_interface = config['noInterface']

    def refresh_config(self):
        with open(self.CONFIG_FILE) as config_file:
            config = json.load(config_file)

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

        with open(self.CONFIG_FILE, 'w') as config_file:
            print(json.dump(data[0], config_file))

def get_file_list():
    """
    Get the list of files in the content folder

    :return: List of files in content folder
    """
    return [f for f in os.listdir(CONTENT_FOLDER) if os.path.isfile(os.path.join(CONTENT_FOLDER, f))]

def launch_video(return_string=False):
    """
    Loads the settings from the config file and launches omxplayer with appropriate settings
    """
    # Loads the config
    config = Config(CONFIG_FILE)

    # Sets the base command, i.e. the video player
    command = ['sudo', 'omxplayer']

    # Goes through the booleans in the config and appends the appropriate argument
    if config.subtitles == True:
        command.append('--subtitles ' + "\"" + os.path.join(ABSPATH, config.subtitles_location) + "\"")
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
    if return_string == True:
        return ' '.join(command)
    else:
        subprocess.run(command)

def kill_video():
    """
    Kills omxplayer
    """
    command = ['sudo', 'killall', 'omxplayer.bin']
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
    command = ['sudo', 'reboot', 'now']
    subprocess.run(command)

    # with open(os.path.join(abspath, 'log.txt'),'wb') as out, open(os.path.join(abspath, 'errorlog.txt'),'wb') as err:
    #     subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err)

def echo(msg):
    print(msg)

if __name__ == "__main__":
    print(get_file_list())
    launch_video()
from flask import Flask, render_template, request
import PiVideoLooper
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

server = Flask(__name__)
settings = PiVideoLooper.Config(PiVideoLooper.config_file)
is_video_playing = False

class SettingsForm(FlaskForm):
    video_file = StringField('Video file')
    command_line = StringField('Custom command line arguments')
    subtitles = BooleanField('Enable subtitles')
    subtitles_location = StringField('Subtitles file location')
    loop = BooleanField('Enable loop')
    no_interface = BooleanField('Enable on-screen-display')

    submit = SubmitField()

    def __init__(self, configobject, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.video_file.data = settings.file_location
        self.command_line.data = settings.command_line
        self.subtitles.data = settings.subtitles
        self.subtitles_location.data = settings.subtitles_location
        self.loop.data = settings.loop
        self.no_interface.data = settings.no_interface

@server.route('/', methods=['GET', 'POST'])
def main():
    form = SettingsForm(csrf_enabled=False, configobject = settings)

    if is_video_playing == True:
        playback_status = 'Playing'
    else:
        playback_status = 'Stopped'

    return render_template('index.html', 
                            form=form,
                            settings = settings,
                            playback_status = playback_status
                            )

@server.route('/playback_settings', methods=['GET', 'POST'])
def playback_settings():
    form = SettingsForm(csrf_enabled=False, configobject = settings)

    return render_template('playback_settings.html',
                            form=form,
                            settings = settings)

@server.route('/launch_video', methods=['GET', 'POST'])
def launch_video():
    print("Launch video")
    is_video_playing = True
    # PiVideoLooper.launch_video()
    return ('', 204)

@server.route('/kill_video', methods=['GET', 'POST'])
def kill_video():
    print("Kill video")
    is_video_playing = False
    # PiVideoLooper.kill_video()
    return ('', 204)

@server.route('/restart_video', methods=['GET', 'POST'])
def restart_video():
    print("Restart video")
    # PiVideoLooper.restart_video()
    return ('', 204)

@server.route('/reboot', methods=['GET', 'POST'])
def reboot():
    print("Reboot pi")
    # PiVideoLooper.reboot()
    return ('', 204)

@server.route('/update_settings', methods=['GET', 'POST'])
def update_settings():
    print("Update settings")
    if request.method == 'POST':
        settings.file_location = request.args.get('file_location')
        settings.command_line = request.args.get('command_line')
        settings.subtitles = request.args.get('subtitles')
        settings.subtitles_location = request.args.get('subtitles_location')
        settings.loop = request.args.get('loop')
        settings.no_interface = request.args.get('no_interface')

    print(settings.file_location)
    settings.write_config()
    return ('', 204)

@server.route('/echo')
def echo():
    print("Echo")
    # PiVideoLooper.echo('Echo')
    return ('', 204)

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5001, debug=True)
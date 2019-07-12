from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

import PiVideoLooper


server = Flask(__name__)
settings = PiVideoLooper.Config(PiVideoLooper.CONFIG_FILE)
is_video_playing = False

class SettingsForm(FlaskForm):
    file_location = StringField('Video file')
    command_line = StringField('Custom command line arguments')
    subtitles = BooleanField('Enable subtitles')
    subtitles_location = StringField('Subtitles file location')
    loop = BooleanField('Enable loop')
    no_interface = BooleanField('Enable on-screen-display')

    submit = SubmitField("Save settings")

    def __init__(self, configobject, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.file_location.data = settings.file_location
        self.command_line.data = settings.command_line
        self.subtitles.data = settings.subtitles
        self.subtitles_location.data = settings.subtitles_location
        self.loop.data = settings.loop
        self.no_interface.data = settings.no_interface

def python_list_to_html(list):
    """
    Converts a Python list object to a formatted HTML list string

    :param list: Python list object
    :return: Formatted html list string
    """
    # html_list = "<ul class=\"mt-decrease10\" style=\"list-style-type:none;\">\n"
    html_list = ""

    for item in list:
        html_list += "<tr><td>" + str(item) + "</td></tr>\n"

    # html_list += "</ul>"

    return html_list

def parse_form_bool(request_arg):
    """
    Parses the value of a BooleanField, which comes into the server as 'y' or null, into a Python boolean

    :return: Boolean
    """
    if request_arg == 'y':
        return True
    else:
        return False

@server.route('/', methods=['GET', 'POST'])
def main():
    form = SettingsForm(csrf_enabled=False, configobject = settings)

    if is_video_playing == True:
        playback_status = 'Playing'
    else:
        playback_status = 'Stopped'

    video_list = python_list_to_html(PiVideoLooper.get_file_list())


    return render_template('index.html', 
                            form=form,
                            settings = settings,
                            playback_status = playback_status,
                            video_list = video_list
                            )

@server.route('/launch_video')
def launch_video():
    print("Launch video")
    is_video_playing = True
    # PiVideoLooper.launch_video()
    return ('', 204)

@server.route('/kill_video')
def kill_video():
    print("Kill video")
    is_video_playing = False
    # PiVideoLooper.kill_video()
    return ('', 204)

@server.route('/restart_video')
def restart_video():
    print("Restart video")
    # PiVideoLooper.restart_video()
    return ('', 204)

@server.route('/reboot')
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

    if request.method == 'GET':
        settings.file_location = request.args.get('file_location')
        settings.command_line = request.args.get('command_line')
        settings.subtitles = parse_form_bool(request.args.get('subtitles'))
        settings.subtitles_location = request.args.get('subtitles_location')
        settings.loop = parse_form_bool(request.args.get('loop'))
        settings.no_interface = parse_form_bool(request.args.get('no_interface'))

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
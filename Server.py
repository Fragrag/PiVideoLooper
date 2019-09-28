import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField

import PiVideoLooper
import Adafruit_Video_Looper

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = PiVideoLooper.CONTENT_FOLDER
server.secret_key = 'PIVIDEOLOOPER'

# NEW ARCHITECTURE IMPLEMENTING ADAFRUIT_VIDEO_LOOPER
# Create instance of Adafruit_Video_Looper.VideoLooper
# /launch_video will run the instances self.run()
# /kill_video will run self.quit()

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
    html_list = ""

    for item in list:
        html_list += "<tr><td>" + str(item) + "</td></tr>\n"

    return html_list

def create_html_dropdown_list_options(list):
    options = ''
    value = 0
    for item in list:
        # option = '<option value=\"' + str(value) + '\">' + item + '</option>\n'
        option = '<option value=\"' + item + '\">' + item + '</option>\n'
        options += option
        value += 1

    return options
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_form_bool(request_arg):
    """
    Parses the value of a BooleanField, which comes into the server as 'y' when ticked or null when unticked, into a Python boolean

    :return: Boolean
    """
    if request_arg == 'y':
        return True
    else:
        return False

@server.route('/', methods=['GET', 'POST'])
def main():
    settings_form = SettingsForm(csrf_enabled=False, configobject = settings)

    if is_video_playing == True:
        playback_status = 'Playing'
    else:
        playback_status = 'Stopped'

    available_videos = python_list_to_html(PiVideoLooper.get_file_list())
    video_select_list = create_html_dropdown_list_options(PiVideoLooper.get_file_list())
    command_string = PiVideoLooper.launch_video(return_string=True)

    return render_template('index.html', 
                            settings_form=settings_form,
                            settings = settings,
                            playback_status = playback_status,
                            available_videos = available_videos,
                            command_string = command_string,
                            video_select_list = video_select_list
                            )

@server.route('/launch_video')
def launch_video():
    print("Launch video")
    is_video_playing = True
    PiVideoLooper.launch_video()
    return ('', 204)

@server.route('/kill_video')
def kill_video():
    print("Kill video")
    is_video_playing = False
    PiVideoLooper.kill_video()
    return ('', 204)

@server.route('/restart_video')
def restart_video():
    print("Restart video")
    PiVideoLooper.restart_video()
    return ('', 204)

@server.route('/reboot')
def reboot():
    print("Reboot pi")
    PiVideoLooper.reboot()
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

@server.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return ('', 204)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return ('', 204)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            flash('Uploaded!')
            return ('', 204)

    return ('', 204)

@server.route('/delete', methods=['GET'])
def delete():
    if request.method == 'GET':
        os.remove(os.path.join(server.config['UPLOAD_FOLDER'], request.args.get('filename')))
        return ('', 204)

@server.route('/echo')
def echo():
    print("Echo")
    PiVideoLooper.echo('Echo')
    return ('', 204)

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5001, debug=True)
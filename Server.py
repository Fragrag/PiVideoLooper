from flask import Flask, render_template
import PiVideoLooper
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

server = Flask(__name__)
settings = PiVideoLooper.read_config()

class SettingsForm(FlaskForm):
    video_file = StringField()
    command_line = StringField()
    subtitles = BooleanField()
    subtitles_location = StringField()
    loop = BooleanField()
    no_interface = BooleanField()

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


    return render_template('index.html', 
                            form=form
                            )

@server.route('/update_config', methods=['GET', 'POST'])
def update_config():
    print('hello')
    return 'nothing'

@server.route('/echo')
def echo():
    print('hello')
    return 'nothing'

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5001, debug=True)
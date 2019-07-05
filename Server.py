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

@server.route('/', methods=['GET', 'POST'])
def main():
    form = SettingsForm(csrf_enabled=False)
    return render_template('index.html', 
                            form=form
                            # video_file = settings.video_file,
                            # command_line = settings.command_line,
                            # subtitles = settings.subtitles,
                            # subtitles_location = settings.subtitles_location,
                            # loop = settings.loop,
                            # no_interface = settings.no_interface
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
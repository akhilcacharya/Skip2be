from flask import Flask
from flask import request
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    vid_id = request.args.get('id')
    os.system("youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch?v="+vid_id+" -o "+vid_id)
    os.system("python convert_single_vtt.py"+vid_id+".en.vtt")

    return 'Hello, World!'
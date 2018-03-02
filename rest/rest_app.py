from flask import Flask
from flask import request
from webvtt import WebVTT
from flask_cors import CORS
import os
import json
import svm_predict
from time_stuff import to_seconds
app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    ranges = []
    vid_id = request.args.get('id')
    if vid_id == "" or not isinstance(vid_id,str):
        return "Pass an arg ya garg!"
    os.system("youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch?v="+vid_id+" -o "+vid_id)
    print('outputs are happening')
    captions = WebVTT().read(vid_id+'.en.vtt')
    ad_array = ["" for i in range(len(captions))]

    last_time=''
    for caption in captions:
        last_time = caption.start
    last_time = to_seconds(last_time)

    i = 0
    for caption in captions:
        words = caption.text
        time = to_seconds(caption.start)/last_time
        ad_array[i] = svm_predict.predict(words,time)
        print(words, str(ad_array[i]))
        i += 1
    end = -1
    for i in range(len(ad_array)):
        if ad_array[i] == 1 and i > end:
            max_sum = 0
            curr_sum = 0
            for x in range(i,len(ad_array)):
                if ad_array[x] ==1:
                    curr_sum+=1
                else:
                    curr_sum-=1
                if curr_sum>= max_sum:
                    max_sum = curr_sum
                    end = x
            ranges.append((i,end))
    starts = []
    times = []
    for caption in captions:
        starts.append(caption.start)
    for each in ranges:
        if each[0] != each[1]:
            times.append((to_seconds(starts[each[0]]),to_seconds(starts[each[1]])))
    os.remove(vid_id+'.en.vtt')
    return "\""+json.dumps(times)+"\""


app.run('0.0.0.0', port=80)
#app.run('0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))
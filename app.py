import json
from random import random
from flask import Flask, render_template, make_response, Response

from queue import Queue
import threading
import gevent
import os, sys
from time import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data='test')

q = Queue()

# To do - Class for Logger and Publisher

# Logging temp data - simulation
# To do - Error handling.
temp_c = 0
def log_temp(name):
    print("Starting " + name)
    gevent.sleep(5)
    while True:
        global temp_c
        temp_c = temp_c + 1
        q.put(temp_c)
        # print("temp added in the queue")
        gevent.sleep(0.5)

# streaming logged data
def stream_data():
    print("Starting streaming")
    while True:
        if not q.empty():
            result = [time() * 1000, random() * 100]
            print("sent data: ", result)
            # print(result)
            # yield 'data: %s\n\n' % str(result)
            yield 'data: ' + json.dumps(result) + "\n\n"
            gevent.sleep(1)
        else:
            print ("QUEUE empty!! Unable to stream @",time())
            gevent.sleep(1) # Try again after 1 sec
            # os._exit(1)

@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    # gevent.sleep(1)
    print("stream requested/posted")
    return Response(stream_data(), mimetype="text/event-stream")


if __name__ == '__main__':
    try:
        th1 = threading.Thread(target=log_temp, args=("temp_logger",))
        # th2 = threading.Thread(target=log_humidity, args=("humidity_logger",))
        th1.start()
        # th2.start()
        print ("Thread(s) started..")
    except:
        print ("Error: unable to start thread(s)")
        os._exit(1)
    else:
        # start streaming
        try:
            app.run(debug=True, host='127.0.0.1', port=5000)
        except:
            print ("Streaming stopped")
            os._exit(1)
    
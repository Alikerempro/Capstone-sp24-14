from flask import Flask, render_template, Response, request
import cv2 as cv
import pickle 
from multiprocessing.connection import Client
import atexit
import json

app = Flask(__name__, static_url_path='',
                  static_folder='Webpage/dist',
                  template_folder='Webpage/dist')

try:
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'sp2414')
except:
    print('Cannot IPC connect')


camera1 = cv.VideoCapture('/dev/video0')
camera2 = cv.VideoCapture("/dev/video3")

camera1.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
camera1.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

camera2.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
camera2.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

#Video 0 is Norm
#Video 2 is Carl


videoMap0 = {}
videoMap1 = {}

with open("LogiCarl.remap", "rb") as infile:
    videoMap0 = pickle.load(infile)

with open("LogiNorm.remap", "rb") as infile:
    videoMap1 = pickle.load(infile)


def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera2.read()  # read the camera frame
        if not success:
            break
        success, frame2 = camera1.read()
        if not success:
            break
        ret, buffer = cv.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route("/manual", methods = {"POST"})
def manualControl():
    req = request.json
    print('manual control request received: ')
    print(req)
    
    try:
        if req['move'] == "forward":
            conn.send(json.dumps({
                "source" : "manual",
                "move" : 1
            }))
        elif req['move'] == "backward":
            conn.send(json.dumps({
                "source" : "manual",
                "move" : -1
            }))
        elif req['move'] == "turnCW":
            conn.send(json.dumps({
                "source" : "manual",
                "turn" : 1
            }))
        elif req['move'] == "turnCCW":
            conn.send(json.dumps({
                "source" : "manual",
                "turn" : -1
            }))
        elif req['move'] == "sampler":
            conn.send(json.dumps({
                "source" : "manual",
                "sampler" : 1
            }))
    except Exception as e:
        print(e)
        return ('', 500)
        
    return ('', 204)

@app.route('/video_feed_reg')
def video_feed_reg():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



#@app.route('/video_feed_CV')
#def video_feed_CV():
#    return Response(gen_frames(False), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')

def cleanup():
    try:        
        conn.close()
    except:
        print("Can not close IPC. Does it exist?")
    
    
atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, port=9000, threaded=True, host='0.0.0.0')

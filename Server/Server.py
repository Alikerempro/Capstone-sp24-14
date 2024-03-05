from flask import Flask, render_template, Response
import cv2 as cv

cap = cv.VideoCapture("/dev/video0")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

print("Width is " + str(cap.get(3)) + " height is " + str(cap.get(4)))
    
cap2 = cv.VideoCapture("/dev/video2")
if not cap2.isOpened():
    print("Cannot open camera 2")
    exit()
    
cap2.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

print("Width2 is " + str(cap2.get(3)) + " height2 is " + str(cap2.get(4)))

app = Flask(__name__, static_url_path='',
                  static_folder='Webpage/dist',
                  template_folder='Webpage/dist')

stereo = cv.StereoBM.create(numDisparities=16, blockSize=15)

def gen_frames():  
    while True:
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        
        frame_new=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame2_new=cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
    
        if not ret2:
            print("Can't receive frame2 (stream end?). Exiting ...")
            break
        
        disparity = stereo.compute(frame_new,frame2_new)
        
        ret3, buffer = cv.imencode('.jpg', disparity)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/camStream")
def camStream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True, host='0.0.0.0')

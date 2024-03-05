from flask import Flask, render_template, Response
import cv2 as cv

app = Flask(__name__, static_url_path='',
                  static_folder='Webpage/dist',
                  template_folder='Webpage/dist')

cameras = [cv.VideoCapture('/dev/video0'), cv.VideoCapture("/dev/video2")]

def gen_frames(plain):  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = cameras[0].read()  # read the camera frame
	success2, frame2 = cameras[1].read()
        if not success or not success2:
            break
        else:
	    if plain == True:
		   ret, buffer = cv.imencode('.jpg', frame)
		   frame = buffer.tobytes()
                   yield (b'--frame\r\n'
                         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
	    else:
		   
		   ret, buffer = cv.imencode('.jpg', frame)
                   frame = buffer.tobytes()
                   yield (b'--frame\r\n'
                         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(use_reloader=False, port=5000, threaded=True, host='0.0.0.0')

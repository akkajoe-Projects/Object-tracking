from flask import Flask, render_template, Response, request, session
import cv2
import threading

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# dict containing different Tracker types
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create,
    "goturn": cv2.TrackerGOTURN_create
}

multiTracker = cv2.MultiTracker_create()
bboxes = []
tracker_objects = []
data_list = []
selected = False
only_once = False
tracker_count = 0

@app.route('/')
def index():
    return render_template('video.html')

def gen_frames():
    global frame
    global tracker_count
    video_stream = cv2.VideoCapture(0)
    print("CAP", video_stream.isOpened())
    while True:
        ret, frame = video_stream.read()
        frame = cv2.resize(frame, (720, 640))
        if not selected:
            r, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame_bytes\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            if tracker_count == 1:
                tracker = OPENCV_OBJECT_TRACKERS[tracker_inp]()
                multiTracker.add(tracker, frame, (data_list[0], data_list[1], data_list[2], data_list[3]))
                tracker_count = 0
            else:
                success, boundingBox = multiTracker.update(frame)
                for i, newbox in enumerate(boundingBox):
                    cv2.rectangle(frame, (int(newbox[0]), int(newbox[1])),
                                  (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3])), (127, 255, 0), 2)
                r, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame_bytes\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/initbb', methods=['POST'])
def initbb():
    global selected
    global tracker_count
    selected = True
    tracker_count = 1
    data = request.get_json()
    print('DATA', data)
    global data_list
    data_list = [i for i in data.values()]
    session['data_list'] = data_list
    return data

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
import cv2
import imutils
import sys
from imutils.video import FPS
import psutil
import threading
from flask import Flask,render_template,Response,request,redirect,url_for,jsonify,session
from logging import FileHandler,WARNING

#dict containing different Tracker types
OPENCV_OBJECT_TRACKERS={
	"csrt":cv2.legacy.TrackerCSRT_create,
	"kcf":cv2.legacy.TrackerKCF_create,
	"boosting":cv2.legacy.TrackerBoosting_create,
	"mil":cv2.legacy.TrackerMIL_create,
	"tld":cv2.legacy.TrackerTLD_create,
	"medianflow":cv2.legacy.TrackerMedianFlow_create,
	"mosse":cv2.legacy.TrackerMOSSE_create,
	"goturn":cv2.TrackerGOTURN_create
}

print(OPENCV_OBJECT_TRACKERS.keys())
print("For GOTURN you are required to download GOTURN model files")
tracker_inp=input("Which tracker would you like to use? ")    

multiTracker=cv2.legacy.MultiTracker_create()
bboxes=[]
tracker_objects=[]
data_list=[]
# fps=FPS().start()

app = Flask(__name__,template_folder='templates')
file_handler= FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.secret_key= 'super secret key'
app.config['SESSION_TYPE']= 'filesystem'

@app.route('/')
def index():
	return render_template('video.html')

'''
gen_frames() enters a loop which continuously returns frames as response chunks
'''
def gen_frames():
	video_stream=cv2.VideoCapture(0)
	print("CAP",video_stream.isOpened())
	while True:
		ret,frame=video_stream.read()
		frame= imutils.resize(frame, width=720, height=640)
		if ret==False:
			print("ERROR")
			sys.exit()
		#resize the frame to process it faster
		# frame=imutils.resize(frame,width=450)
		# frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		# Bounding Boxes are created on pressing "s"
		# if cv2.waitKey(1) & 0xFF==ord("s"):
		# 	while True:		
		# 		bbox=cv2.selectROI("MultiTracker",frame,fromCenter=False,
		# 		showCrosshair=False)
		# 		tracker=OPENCV_OBJECT_TRACKERS[tracker_inp]()
		# 		tracker_objects.append(tracker)
		# 		bboxes.append(bbox)
		# 		print("bboxes"+str(bboxes))
		# 		print("Press q to quit selecting boxes and start tracking.")
		# 		#if cv2.waitKey(1) & 0xFF==ord("b")
		# 		if cv2.waitKey(0) & 0xFF==ord("q"):
		# 			print("INSIDE IF CONDITION")
		# 			break

		# for b in range(len(bboxes)):
		# 	multiTracker.add(tracker_objects[b],frame,bboxes[b])
		# 	(success,boundingBox)=multiTracker.update(frame)
		# 	for i,newbox in enumerate(boundingBox):
		# 		cv2.rectangle(frame,(int(newbox[0]),int(newbox[1])),
		# 		(int(newbox[0]+newbox[2]),int(newbox[1]+newbox[3])),(127,255,0),2)

		# if cv2.waitKey(1) & 0xFF==ord("x"):
		# 	break
	
		#cv2.imshow("MultiTracker",frame)
		r,buffer=cv2.imencode('.jpg',frame)
		frame=buffer.tobytes()
		yield (
		b'--frame\r\n'
		b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
		) #concat frame one by one and show the result
		# fps.update()
		
	# video_stream.release()
	# cv2.destroyAllWindows()

'''Define app route for video feed, returns the streaming response (images)
The URL to this route is in the "src" attribute of the image tag'''
@app.route('/video_feed')
def video_feed():
	return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

#endpoint for POST request
@app.route('/initbb',methods=['POST'])
def initbb():
	data= request.get_json()
	print('DATA',data)
	global data_list
	data_list=[i for i in data.values()]
	session['data_list']= data_list
	# return redirect(url_for('initcoords'))
	return data
# @app.route('/initcoords')
# def initcoords():
# 	data_list= session.get('data_list')
# 	initcoords= {"x":data_list[0],"y":data_list[1],"width":data_list[2],"height":data_list[3]}
# 	response= jsonify(initcoords)
# 	#jsonify() converts the data to JSON format and send it as a response
# 	return response

	# fps.stop()
# print(f"ELAPSED TIME {fps.elapsed()}")s
# print(f"APPROX FPS {fps.fps()}")
print(f"The cpu usage is:{psutil.cpu_percent(4)}")
print(f"ACTIVE THREADS: {threading.enumerate()}")

		
		


import cv2
import sys
#import imutils
#from imutils.video import VideoStream
#from argparse import ArgumentParser


#for command line interface
#ap=ArgumentParser()
#ap.add_argument("--t","--tracker",type=str,default="kcf",
#help="OpenCv Object tracker type")
#args=vars(ap.parse_args())

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
tracker_inp=input("Which tracker would you like to use? ")

tracker=OPENCV_OBJECT_TRACKERS[tracker_inp]()
#tracker=OPENCV_OBJECT_TRACKERS[list(args.values())[0]]()
#print(OPENCV_OBJECT_TRACKERS[list(args.values())[0]])

#inititalize
initBB=None

video_stream=cv2.VideoCapture(0)

while True:
	ret,frame=video_stream.read()
	#resize the frame to process it faster
	#frame=imutils.resize(frame,width=500)
	#(h,w)=frame.shape[:2]
	
	if ret==False:
		print("ERROR")
		sys.exit()
	if initBB !=None:
		(success,box)=tracker.update(frame)
		if success:
			(x,y,w,h)=[int(c) for c in box]
			cv2.rectangle(frame,(x,y),(x+w,y+h),(127,255,0),2)
			
	cv2.imshow("Frame",frame)
	if cv2.waitKey(1) & 0xFF==ord("x"):
		break
	if cv2.waitKey(1) & 0xFF==ord("b"):
		initBB=cv2.selectROI("Frame",frame,fromCenter=False
		,showCrosshair=True)
		tracker.init(frame,initBB)
		
video_stream.release()
cv2.destroyAllWindows()
		

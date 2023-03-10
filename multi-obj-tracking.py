import cv2
import sys
#import imutils
#from imutils.video import VideoStream
import keyboard

OPENCV_OBJECT_TRACKERS={
	"csrt":cv2.legacy.TrackerCSRT_create,
	"kcf":cv2.legacy.TrackerKCF_create,
	"boosting":cv2.legacy.TrackerBoosting_create,
	"mil":cv2.legacy.TrackerMIL_create,
	"tld":cv2.legacy.TrackerTLD_create,
	"medianflow":cv2.legacy.TrackerMedianFlow_create,
	"mosse":cv2.legacy.TrackerMOSSE_create,
	#"goturn":cv2.TrackerGOTURN_create
}

print(OPENCV_OBJECT_TRACKERS.keys())
print("For GOTURN you are required to download GOTURN model files")
tracker_inp=input("Which tracker would you like to use? ")

multiTracker=cv2.legacy.MultiTracker_create()

#inititalize
initBB=None
bboxes=[]
k=cv2.waitKey(1) & 0xFF
tracker_objects=[]

video_stream=cv2.VideoCapture(0)

while True:
	ret,frame=video_stream.read()
	#resize the frame to process it faster
	#frame=imutils.resize(frame,width=500)
	#(h,w)=frame.shape[:2]
	
	if ret==False:
		print("ERROR")
		sys.exit()

	if cv2.waitKey(1) & 0xFF==ord("s"):
	#if keyboard.read_key() == "s":
	# if k==ord("s"):
		print("INSIDE S")
		while True:		
			bbox=cv2.selectROI("MultiTracker",frame,fromCenter=False,
			showCrosshair=False)
			tracker=OPENCV_OBJECT_TRACKERS[tracker_inp]()
			tracker_objects.append(tracker)
			bboxes.append(bbox)
			print("bboxes"+str(bboxes))
			print("Press q to quit selecting boxes and start tracking.")
			#if cv2.waitKey(1) & 0xFF==ord("b")
			if cv2.waitKey(0) & 0xFF==ord("q"):
				print("INSIDE IF CONDITION")
				break

	for b in range(len(bboxes)):
		multiTracker.add(tracker_objects[b],frame,bboxes[b])
		(success,boundingBox)=multiTracker.update(frame)
		for i,newbox in enumerate(boundingBox):
			cv2.rectangle(frame,(int(newbox[0]),int(newbox[1])),
			(int(newbox[0]+newbox[2]),int(newbox[1]+newbox[3])),(127,255,0),2)



	# for tracker in tracker_objects:
	# 	print("Tracker",tracker)
	# 	print(type(tracker))
	# for bbox in bboxes and tracker in tracker_objects: #and tracker in tracker_objects:
	# 	multiTracker.add(tracker,frame,bbox)
	# 	print("BOUNDING BOX",bbox)
	# 	(success,b) = multiTracker.update(frame)
	# 	print("b:")
	# 	print(b)
	# 	for i,newbox in enumerate(b):
	# 		cv2.rectangle(frame,(int(newbox[0]),int(newbox[1])),
	# 		(int(newbox[0]+newbox[2]),int(newbox[1]+newbox[3])),(127,255,0),2,1)
	# 		print(int(newbox[0]),"NEWBOX")
	# if len(bboxes)>=1:
	# 	for b in range(len(bboxes)):
	# 		multiTracker.add(tracker,frame,bboxes[b])
	# 		(success,boundingBox)=multiTracker.update(frame)
	# 		for i,newbox in enumerate(boundingBox):
	# 			cv2.rectangle(frame,(int(newbox[0]),int(newbox[1])),(int(newbox[0]+newbox[2]),int(newbox[1]+newbox[3])),(127,255,0),2)
		
	cv2.imshow("MultiTracker",frame)
	if cv2.waitKey(1) & 0xFF==ord("x"):
		break
	#if cv2.waitKey(1) & 0xFF==ord("b"):
		#initBB=cv2.selectROI("Frame",frame,fromCenter=False
		#,showCrosshair=True)
		#tracker.init(frame,initBB)
		
video_stream.release()
cv2.destroyAllWindows()
		
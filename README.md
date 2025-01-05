## Introduction
This repository contains a multi-object tracking application using OpenCV and Flask. The application allows users to track multiple objects in a video stream using various tracking algorithms.
Please view the single-obj branch for single object tracking.
**I would recommend running the [multi-tracking-wthread.py](multi-tracking-wthread.py) using the medianflow tracker.**

### Summary of set up
1. Clone the repository.
2. Install the required dependencies.
3. Run the application.

### Dependencies
Install the required dependencies using the following command:
```bash
pip install -r requirements.txt
``

### Deployment instructions
To run the Flask server, use the following command:
```bash
python flask_server.py
```

To run the multi-object tracking application, use the following command:
```bash
python multi-obj-tracking.py
```

To run the multi-object tracking application with threading, use the following command:
```bash
python multi-tracking-wthread.py
```

## Contribution guidelines
- **Writing tests**: Ensure all new features are covered by unit tests.
- **Code review**: Submit pull requests for code review before merging.
- **Other guidelines**: Follow PEP 8 coding standards.

## Who do I talk to?
- **Repo owner or admin**
- **Other community or team contact**

## Additional Information
- The `static` directory contains static files such as JavaScript and CSS.
- The `templates` directory contains HTML templates for the Flask application.
- The `flask_server.py` file contains the Flask server implementation.
- The `multi-obj-tracking.py` file contains the multi-object tracking implementation.
- The `multi-tracking-wthread.py` file contains the multi-object tracking implementation with threading.

## Code Explanation

### multi-tracking-wthread.py
The `multi-tracking-wthread.py` script performs the following tasks:
- **Imports necessary libraries**: The script imports OpenCV, imutils, and other necessary libraries.
- **Defines available trackers**: A dictionary `OPENCV_OBJECT_TRACKERS` is defined to hold different types of OpenCV object trackers.
- **Initializes variables**: Variables such as `multiTracker`, `bboxes`, `tracker_objects`, and `vs` (video stream) are initialized.
- **Starts video stream**: The video stream is started using `WebcamVideoStream`.
- **Main loop**: The script enters a loop where it reads frames from the video stream, resizes them, and converts them to grayscale.
- **Select ROI**: If the 's' key is pressed, the user can select multiple regions of interest (ROIs) on the frame. These ROIs are added to the `multiTracker`.
- **Update and draw bounding boxes**: The `multiTracker` updates the positions of the tracked objects and draws bounding boxes around them.
- **Display frame**: The frame with the bounding boxes is displayed in a window.
- **Exit condition**: If the 'x' key is pressed, the loop breaks, and the video stream stops.
- **Print FPS**: The elapsed time and approximate FPS are printed.

### multi-obj-tracking.py
The `multi-obj-tracking.py` script performs the following tasks:
- **Imports necessary libraries**: The script imports OpenCV, imutils, Flask, and other necessary libraries.
- **Defines available trackers**: A dictionary `OPENCV_OBJECT_TRACKERS` is defined to hold different types of OpenCV object trackers.
- **Initializes variables**: Variables such as `multiTracker`, `bboxes`, `tracker_objects`, and `data_list` are initialized.
- **Flask server setup**: The Flask server is set up with routes for the index page and video feed.
- **Video stream**: The `gen_frames` function captures video frames and processes them for tracking.
- **Select ROI**: The `/initbb` route allows the user to select regions of interest (ROIs) on the frame. These ROIs are added to the `multiTracker`.
- **Update and draw bounding boxes**: The `multiTracker` updates the positions of the tracked objects and draws bounding boxes around them.
- **Display frame**: The frame with the bounding boxes is displayed in a web page.

This script allows users to track multiple objects in real-time using different tracking algorithms provided by OpenCV.
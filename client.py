import cv2
import numpy as np
import socket
import sys
import pickle
import struct
#Yash added: March 17
import pyrealsense2 as rs
from realsensecv import RealsenseCapture


#cap = cv2.VideoCapture(0)


#cap = RealsenseCapture()
#cap.start()

#### Yash changes: March 17
# Initialize communication with intel realsense
pipeline = rs.pipeline()
realsense_cfg = rs.config()
realsense_cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 6)
pipeline.start(realsense_cfg)
print("Test data source...")
try: 
	np.asanyarray(pipeline.wait_for_frames().get_color_frame().get_data())
except:
	raise Exception("Can't get rgb frame from data source")
print("Press [ESC] to close the application")
####

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '10.150.9.127' # YOUR IP ADDRESS
#10.150.9.127
clientsocket.connect((host_ip, 12345))

while True:
  
#### Yash added: March 17
    # Get frame from realsense and convert to grayscale image
    frames = pipeline.wait_for_frames()
    img_rgb = np.asanyarray(frames.get_color_frame().get_data())
    cv2.imshow("AR-Example", cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
  #  img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
#### 
    
   # ret,frame=cap.read()
# Yash added:
#   ret,frame=frames.get_color_frame()

    # Serialize frame
    data = pickle.dumps(img_rgb)

    # Send message length first
    message_size = struct.pack("L", len(data)) ### CHANGED    
    print(len(data))
    # Then data
    clientsocket.sendall(message_size + data)

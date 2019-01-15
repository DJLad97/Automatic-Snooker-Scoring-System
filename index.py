import cv2
import numpy as np
import argparse
import imutils
import time
import mysql.connector
import pymysql
import paramiko
import pandas as pd
import os
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
from dotenv import load_dotenv

load_dotenv()

home = expanduser('~')
mypkey = paramiko.RSAKey.from_private_key_file(home + '/.ssh/id_rsa', password=os.getenv('priv_key_password'))

# Add these to env file
sql_hostname = os.getenv('sql_hostname')
sql_username = os.getenv('sql_username')
sql_password = os.getenv('sql_password')
sql_main_database = os.getenv('sql_main_database')
sql_port = 3306
ssh_host = os.getenv('ssh_host')
ssh_user = os.getenv('ssh_user')
ssh_port = 22

  # query = '''SELECT * FROM tempTable;'''
  # data = pd.read_sql_query(query, conn)
  # print(data)

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
# cap = cv2.VideoCapture('/Users/dan/Lady-Cannings.mp4')

# cap = cv2.VideoCapture("udp://127.0.0.1:10000")
cap = cv2.VideoCapture('game2.mov')
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('/Users/dan/Downloads/snooker-game2.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
  print("Error opening video stream or file")

tableLower = (47, 100, 100)
tableUpper = (67, 255, 255)
lower = {
#   #'red':    (166,84,141), // Video game colours
  'red':    (0,176,154),
# #   'yellow': (23,59,119), // Video game colours
  'yellow': (11,139,215),
# #   'green':  (66,122,129), // Video game colours
  'green':  (57,70,89),
# #   'brown':  (0,29,0), // Video game colours
  'brown':  (0,41,49),
# #   'blue':   (97,100,117), // Video game colours
  'blue':   (87,122,111),
# #   'pink':   (141,40,200), // Video game colours
  'pink':   (169,76,149),
# #   'black':  (53,26,0), // Video game colours
  'black':  (103,56,16),
}

upper = {
# #   'red':    (186,255,255), // Video game colours
  'red':    (35,237,208),
# #   'yellow': (50,255,255), // Video game colours
  'yellow': (169,227,255),
# #   'green':  (86,255,255), // Video game colours
  'green':  (82,96,138),
# #   'brown':  (48,174,143), // Video game colours
  'brown':  (13,204,145),
# #   'blue':   (117,255,255), // Video game colours
  'blue':   (162,255,255),
# #   'pink':   (169,192,255), // Video game colours
  'pink':   (176,199,255),
# #   'black':  (120,120,75), // Video game colours
  'black':  (133,156,88),
}

colours = {
    'red': (0,0,255),
    'yellow': (0,255,255),
    'green': (0,255,0),
    'brown': (42,255,165),
    'blue': (255,0,0),
    'pink': (180,105,255),
    'black': (0,0,0),
}
balls = [
  ([166,84,141], [186,255,255]), # Red
  # ([175,0,0], [180,255,255]), # Red
  ([23,59,119],   [50,255,255]), # Yellow
  ([66,122,129], [86,255,255]), # Green
  ([0,29,0], [    48,174,143]), # Brown
  ([97,100,117], [117,255,255]), # Blue
  ([141,40,200],  [169,192,255]), # Pink
  ([53,26,0],    [120,120,75]), # Black
  ([22,31,242], [33,76,255]), # White (not working)
  # ([150,84,141], [186,255,255]), # Pink
  # ([22, 0, 0], [60, 255, 255]), # White
  # ([25, 0, 0], [50, 255, 255])
]


finalEdges = 0
finalMask = 0

totalReds = 15
redCount = 0
yellowCount = 0
pinkCount = 0
initialFrame = 0
frameCheck = 5
currentBallCount = 0

cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrame)
# img = cv2.imread('red.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(img, (9,9), 0)

# hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
# kernal = np.ones((8,8), np.uint8)
# mask = cv2.inRange(hsv, lower['red'], upper['red'])
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
# mask = cv2.erode(mask, kernal, iterations=4)

# # Add this and the threshold function to get make the results more circular 
# # They are currently not in as they're not needed at this stage and just slow things down
# mask = cv2.GaussianBlur(mask, (7,7), 0)

# finalMask = mask
# thresh = cv2.threshold(finalMask, 20, 255, 0)[-1]

# contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
# currentColor = colours['red']
# # print(key + ': ' + str(len(contours)))
# for c in contours:

#     # The following code is only needed to show what has been detected
#     # Can be removed in final version to improve fps
#     M = cv2.moments(c)
#     if M["m00"] != 0:
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#     else:
#         cX, cY = 0, 0

#     cv2.circle(img, (cX, cY), 10, (255,255,255), -1)
# cv2.imshow('result', img)
# Read until video is completed
while True:
    # Captures the live stream frame-by-frame
    _, frame = cap.read()

    # Width: 600 - Height: 337
    frame = imutils.resize(frame, width=600)
    # Crop video to only check the table and not the game UI
    # frame = frame[25:315, 25:585]
    finalMask = 0
    finalMaskTable = 0
    finalEdges = 0

    blur = cv2.GaussianBlur(frame, (9,9), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    checkBallCount = False

    # Every 5 frames give the system the ability to check the current ball count on the tabl
    # The first frame to be processed is always 1 + the initial frame and as a result, there will be no inital check of the current red balls
    # And redCount will be set to 0 as a result which also means the if statement to check whether to update the database will also be true
    # So check if current frame is 1 + initalFrame will seed the inital redCount and not update the database prematurely
    if((currentFrame == initialFrame + 1) or currentFrame % frameCheck == 0):
        redCount = 0
        yellowCount = 0
        pinkCount = 0
        checkBallCount = True
    else:
        checkBallCount = False
    
    for key, value in upper.items():
        kernal = np.ones((8,8), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)

        # Add this and the threshold function to get make the results more circular 
        # They are currently not in as they're not needed at this stage and just slow things down
        mask = cv2.GaussianBlur(mask, (7,7), 0)

        finalMask = mask
        # thresh = cv2.threshold(finalMask, 127, 255, 0)[-1]
        
        contours = cv2.findContours(finalMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        currentColor = colours[key]
        # print(key + ': ' + str(len(contours)))
        i = 0
        for c in contours:
            # The following code is only needed to show what has been detected
            # Can be removed in final version to improve fps
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            cv2.circle(frame, (cX, cY), 5, (255,255,255), -1)


            # if(i < 1 and str(key) != 'red'):
            #     cv2.putText(frame, str(key), (cX -25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            
            # if(str(key) == 'red' and i <= 9):
            #     cv2.putText(frame, str(key), (cX -25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

            # i += 1
            # Need to work out something where if a ball ends up being obscured and so won't be counted
            if(checkBallCount):
                # When counting the number of balls make sure to reset the ball count at the beginning of the while loop
                if (key == 'pink'):
                    pinkCount += 1
                elif(key == 'red'):
                    redCount += 1

        # print('redCount' + str(redCount))
        # print('totalReds' + str(totalReds))

        # Check if any red balls have been potted   
        if(redCount < totalReds):
            numberOfRedsPotted = totalReds - redCount
            pointsScored = numberOfRedsPotted
            totalReds =- numberOfRedsPotted
            
            # Connect to database using ssh keys 
            with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                with conn.cursor() as cursor:
                    # Simple query for that just increments the points count
                    query = '''UPDATE tempTable SET points = points + %s WHERE player_name = "dan";'''
                    cursor.execute(query, (pointsScored))
                
                conn.commit()
                conn.close()


    # May not be needed
    # res = cv2.bitwise_and(frame,frame, mask = finalMask)

    # Display test for number of red balls
    cv2.putText(frame, str(redCount), (250, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)


    cv2.imshow('res', frame)
    # cv2.imshow('resTable', resTable)

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()

cap.release()


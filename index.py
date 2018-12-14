import cv2
import numpy as np
import argparse
import imutils
import time
import mysql.connector
import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser

home = expanduser('~')
mypkey = paramiko.RSAKey.from_private_key_file(home + '/.ssh/id_rsa', password='billion2468')

sql_hostname = '127.0.0.1'
sql_username = 'root'
sql_password = 'billion2468'
sql_main_database = 'Snooker_Scoring_System'
sql_port = 3306
ssh_host = '178.62.84.70'
ssh_user = 'dan'
ssh_port = 22

  # query = '''SELECT * FROM tempTable;'''
  # data = pd.read_sql_query(query, conn)
  # print(data)

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
# cap = cv2.VideoCapture('/Users/dan/Lady-Cannings.mp4')

cap = cv2.VideoCapture('snooker-game.mp4')
# pts = deque(maxlen=64)

# cap = cv2.VideoCapture(1)

# Morphology



# Check if camera opened successfully
if (cap.isOpened() == False):
  print("Error opening video stream or file")

time.sleep(2.0)
tableLower = (47, 100, 100)
tableUpper = (67, 255, 255)

lower = {
  'red':    (166,84,141),
  'yellow': (23,59,119),
  'green':  (66,122,129),
  'brown':  (0,29,0),
  'blue':   (97,100,117),
  'pink':   (141,40,200),
  'black':  (53,26,0),
}

upper = {
  'red':    (186,255,255),
  'yellow': (50,255,255),
  'brown':  (48,174,143),
  'green':  (86,255,255),
  'blue':   (117,255,255),
  'pink':   (169,192,255),
  'black':  (120,120,75),
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
img = cv2.imread('test.png', cv2.IMREAD_COLOR)
img = cv2.resize(img, (600, 400))

grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(grayImg, 127, 255, 0)

im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    cv2.circle(img, (cX, cY), 5, (255,255,255), -1)
    cv2.putText(img, "centroid", (cX -25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    # cv2.imshow("Image", img)

# cv2.waitKey(0)

totalReds = 15
redCount = 0
initialFrame = 700
frameCheck = 5
cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrame)

# Read until video is completed
while True:
  # Captures the live stream frame-by-frame
    _, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    frame2 = imutils.resize(frame, width=600)
    finalMask = 0
    finalMaskTable = 0
    finalEdges = 0

    blur = cv2.GaussianBlur(frame, (9,9), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    checkBallCount = False
    if((currentFrame == initialFrame + 1) or currentFrame % frameCheck == 0):
        redCount = 0
        checkBallCount = True
    else:
        checkBallCount = False

    

    # lower_red = np.array([166,84,141])
    # upper_red = np.array([186,255,255])

    # redBallsMask = cv2.inRange(hsv, lower_red, upper_red)

    # lower_green = np.array([66, 122, 129])
    # upper_green = np.array([86, 255, 255])

    # greenBallsMask = cv2.inRange(hsv, lower_green, upper_green)

    # lower_blue = np.array([97, 100, 117])
    # upper_blue = np.array([117, 255, 255])

    # blueBallsMask = cv2.inRange(hsv, lower_blue, upper_blue)

    # lower_yellow = np.array([23, 59, 119])
    # upper_yellow = np.array([54,255,255])

    # yellowBallsMask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # mask = redBallsMask | greenBallsMask | blueBallsMask | yellowBallsMask

    # kernal = np.ones((9,9), np.uint8)
    # maskTable = cv2.inRange(hsv, tableLower, tableUpper)
    # maskTable = cv2.morphologyEx(maskTable, cv2.MORPH_OPEN, kernal)
    # maskTable = cv2.morphologyEx(maskTable, cv2.MORPH_CLOSE, kernal)
    # finalMaskTable += maskTable

    # gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(gray, 5)
    # rows = gray.shape[0]
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
    #                           param1=100,param2=30,minRadius=1, maxRadius=200)

    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for i in circles[0, :]:
    #         center = (i[0], i[1])
    #         # circle center
    #         cv2.circle(frame2, center, 1, (0, 100, 100), 3)
    #         # circle outline
    #         radius = i[2]
    #         cv2.circle(frame2, center, radius, (255, 0, 255), 3)

    # edges = cv2.Canny(frame, 200, 500)
    
    i = 0
    for key, value in upper.items():
        # print(lower[key])
        # lower = np.array(lower[key], dtype="uint8")
        # upper = np.array(upper[key], dtype="uint8")

        kernal = np.ones((6,6), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        # mask = cv2.erode(mask, kernal, iterations=1)
        # mask = cv2.dilate(mask, kernal, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
        mask = cv2.GaussianBlur(mask, (7,7), 0)

        # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
        finalMask += mask
        # edges = cv2.Canny(finalMask, 300, 500)
        # finalEdges += edges
        # i += 1

        # gray = cv2.cvtColor(finalMask, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(finalMask, 127, 255, 0)

        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        currentColor = colours[key]
        for c in contours:
            M = cv2.moments(c)
            # if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # else:
                # cX, cY = 0, 0

            # cv2.circle(frame, (cX, cY), 5, (255,255,255), -1)


            # cv2.putText(frame, key + " ball", (cX -25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            if(checkBallCount):
                if(key == 'red'):
                    redCount += 1
        # print('redCount' + str(redCount))
        # print('totalReds' + str(totalReds))
        # Check if any red balls have been potted   
        if(redCount < totalReds):
            numberOfRedsPotted = totalReds - redCount
            pointsScored = numberOfRedsPotted
            totalReds =- numberOfRedsPotted
            with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                with conn.cursor() as cursor:
                    query = '''UPDATE tempTable SET points = points + %s WHERE player_name = "dan";'''
                    cursor.execute(query, (pointsScored))
                
                conn.commit()
                conn.close()


    # resTable = cv2.bitwise_and(frame,frame, mask = finalMaskTable)
    # edges= cv2.Canny(finalMask, 100, 200)
    res = cv2.bitwise_and(frame,frame, mask = finalMask)
    # cv2.putText(frame,"Count " + str(i), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255,255,255),2)

    cv2.putText(frame, str(redCount), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
    # cv2.putText(frame, key + " ball", (cX -25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)


    cv2.imshow('res', frame)
    # cv2.imshow('resTable', resTable)

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()

cap.release()


#!/usr/bin/env python


# Talk about the different lighting used
# Get the outer contour
# Try and get size of contour to determine if what is found is ball

import cv2
import numpy as np
import math
import argparse
import imutils
import time
import mysql.connector
import pymysql
import paramiko
import pandas as pd
import os
import asyncio
import websockets
import requests
import socket
import matplotlib
matplotlib.use("pdf")
from matplotlib import pyplot as plt
from collections import deque
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
from dotenv import load_dotenv


def computerVisionSystem(gameId):

    # query = '''SELECT * FROM tempTable;'''
    # data = pd.read_sql_query(query, conn)
    # print(data)

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name

    # cap = cv2.VideoCapture("udp://127.0.0.1:10000")
    # cap = cv2.VideoCapture("ball-clump-test.mov")
    # cap = cv2.VideoCapture("game6.mov")
    cap = cv2.VideoCapture("game5.mov")
    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('/Users/dan/Downloads/snooker-game2.mp4')

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    tableLower = (47, 100, 100)
    tableUpper = (67, 255, 255)
    lower = {
    #   'red':    (166,84,141),  # Video game colours
    #   'red':    (0,176,154), # HSV (old)
    #   'red':    (0,170,0), # HSV (old)
      'red':    (0,156,137), # HSV
    # 'red':    (0,171,84), # YCrCb (old)
    # 'red':    (48,184,37), # YCrCb
    #   'yellow': (23,59,119), # Video game colours
    #   'yellow': (11,139,215), # HSV (old)
      'yellow': (19,121,91), # HSV
    #   'yellow': (170,145,20), # YCrCb (old)
    #   'yellow': (209,131,0), # YCrCb
    # # #   'green':  (66,122,129), # Video game colours
    # #   'green':  (57,70,89), # HSV (old)
      'green':  (53,119,1), # HSV 
    #   'green':  (91,104,101), # YCrCb (old)
    #   'green':  (42,88,62), # YCrCb
    # # #   'brown':  (0,29,0), # Video game colours
    # #   'brown':  (0,41,49), # HSV (old)
      'brown':  (0,114,93), # HSV
    #   'brown':  (50,132,103), # YCrCb (old)
    #   'brown':  (68,32,96), # YCrCb
    # # #   'blue':   (97,100,117), # Video game colours
    # #   'blue':   (87,122,111), # HSV (old)
    #   'blue':   (91,129,102), # HSV
      'blue':   (107,156,137), # HSV
    #   'blue':   (60,78,147), # YCrCb (old)
    #   'blue':   (52,70,168), # YCrCb
    # # #   'pink':   (141,40,200), # Video game colours
    # #   'pink':   (169,76,149), # HSV (old)
      'pink':   (0,80,200), # HSV 
    #   'pink':   (96,242,150), # YCrCb (old)
    #   'pink':   (187,133,103), # YCrCb
    # # #   'black':  (53,26,0), # Video game colours
    # #   'black':  (103,56,16), # HSV (old)
    #   'black':  (65,31,0), # HSV 
    #   'black':  (101,35,6), # HSV 
    #   'black':  (103,56,16), # YCrCb (old)
    #   'black':  (0,96,84), # YCrCb
    # 'white': (223,108,118) #YCrCb
    'white': (0,0,200) #HSV
    }
    # Lower bounds: [101  35   6] black

    upper = {
    #   'red':    (179,255,255), # Video game colours
    #   'red':    (35,237,208), # HSV (old)
    #   'red':    (16,255,255), # HSV (old)
      'red':    (15,255,255), # HSV
    # 'red':    (110,255,255), # YCrCb (old)
    # 'red':    (255,255,255), # YCrCb
    #   'yellow': (50,255,255), # Video game colours
    #   'yellow': (169,227,255), # HSV (old)
      'yellow': (47,240,255), # HSV 
    #   'yellow': (254,220,73), # YCrCb (old)
    #   'yellow': (246,155,102), # YCrCb
    # # #   'green':  (86,255,255), # Video game colours
    # #   'green':  (82,96,138), # HSV (old)
      'green':  (80,255,249), # HSV 
    #   'green':  (138,115,132), # YCrCb (old)
    #   'green':  (129,112,130), # YCrCb
    # # #   'brown':  (48,174,143), # Video game colours
    # #   'brown':  (13,204,145), # HSV (old)
      'brown':  (30,222,150), # HSV 
    #   'brown':  (103,166,122), # YCrCb (old)
    #   'brown':  (129,165,117), # YCrCb
    # # #   'blue':   (117,255,255), # Video game colours
    # #   'blue':   (162,255,255), # HSV (old)
    #   'blue':   (130,234,223), # HSV 
      'blue':   (179,255,255), # HSV 
    #   'blue':   (126,112,196), # YCrCb (old)
    #   'blue':   (135,115,255), # YCrCb
    # # #   'pink':   (169,192,255), # Video game colours
    # #   'pink':   (176,199,255), # HSV (old)
      'pink':   (179,130,255), # HSV 
    #   'pink':   (185,242,150), # YCrCb (old)
    #   'pink':   (234,178,255), # YCrCb
    # # #   'black':  (120,120,75), # Video game colours
    # #   'black':  (133,156,88), # HSV (old)
    #   'black':  (117,127,112), # HSV 
    #   'black':  (132,141,129), # HSV 
    #   'black':  (133,156,88), # YCrCb (old)
    #   'black':  (49,126,179), # YCrCb
    # 'white': (255,129,137) #YCrCb
    'white': (78,40,255) # HSV
    }
    # Upper bounds: [132 141 129] black


    ballCoords = {
        'white': deque(maxlen=32),
        'yellow': deque(maxlen=32),
        'green': deque(maxlen=32),
        'brown': deque(maxlen=32),
        'blue': deque(maxlen=32),
        'pink': deque(maxlen=32)
        # 'black': deque(maxlen=32)
    }

    ballMoving = {
        'white': False,
        'yellow': False,
        'green': False,
        'brown': False,
        'blue': False,
        'pink': False
        # 'black': False
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

    totalReds = 10
    redCount = 0
    previousRedCount = 0
    blueCount = 0

    previousYellowCount = 0
    yellowPotConfidence = 0
    yellowCount = 0
    yellowPotted = False
    yellowDetectionRate = 0

    previousYellowX = 0
    previousYellowY = 0
    yellowCoords = deque(maxlen=32)
    yellowMoving = False


    previousGreenCount = 0
    greenPotConfidence = 0
    greenCount = 0
    greenPotted = False
    ballDetectionRate = 0

    previousBrownCount = 0
    brownPotConfidence = 0
    brownCount = 0
    brownPotted = False

    previousBlueCount = 0
    bluePotConfidence = 0
    blueCount = 0
    bluePotted = False

    previousPinkCount = 0
    pinkPotConfidence = 0
    pinkCount = 0
    pinkPotted = False

    previousWhiteCount = 0
    whitePotConfidence = 0
    whiteCount = 0
    whitePotted = False

    whiteCoords = deque(maxlen=32)

    x = []
    y = []

    
    cX = 0
    cY = 0

    # initialFrame = 8325 
    # initialFrame = 10500
    # initialFrame = 2500
    initialFrame = 500
    # initialFrame = 500
    # initialFrame = 9000 
    # initialFrame = 0 
    frameFromVideoStart = 0
    # initialFrame = 1600 # Just before yellow is potted
    # initialFrame = 5250
    # initialFrame = 9000
    # Explain why I check every frames and not any other number
    # Run some tests against other numbers
    frameCheck = 5
    numberOfRedsPotted = 0
    ballPottedConfidence = 0
    calculateBallSizes = True
    averagePeremiter = 0
    maxPerimeter = 0

    cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrame)

    # Read until video is completed
    while True:
        # Captures the live stream frame-by-frame
        _, frame = cap.read()
        # if(instruction == 'change player'):
            # print('switching games')

        # Width: 600 - Height: 337
        frame = imutils.resize(frame, width=600)
        # Crop video to only check the table and not stuff on surrounding the table
        frame = frame[25:245, 75:535] # Y, X

        # Added some black circles over the pockets so balls are not detected while in the pocket
        cv2.circle(frame, (24,18), 5, (0,0,0), 19) # Top left
        cv2.circle(frame, (237,17), 4, (0,0,0), 19) # Top Middle
        cv2.circle(frame, (450,15), 5, (0,0,0), 19) # Top Right
        cv2.circle(frame, (452,202), 5, (0,0,0), 19) # Bottom Right
        cv2.circle(frame, (239,207), 4, (0,0,0), 19) # Bottom Middle
        cv2.circle(frame, (25,205), 5, (0,0,0), 19) # Bottom left


        finalMask = 0
        finalMaskTable = 0
        finalEdges = 0


        blur = cv2.GaussianBlur(frame, (9,9), 0)
        # hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2YCrCb)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        # print(currentFrame)
        checkBallCount = False

        # Every 5 frames, give the system the ability to check the current ball count on the table
        # The first frame to be processed is always 1 + the initial frame and as a result, there will be no inital check of the current red balls
        # And redCount will be set to 0 as a result which also means the if statement to check whether to update the database will also be true (which add a lot of points to the datbase)
        # So check if current frame is 1 + initalFrame will seed the inital redCount and not update the database prematurely
        previousRedCount = redCount
        previousYellowCount = yellowCount
        previousGreenCount = greenCount
        previousBrownCount = brownCount
        previousBlueCount = blueCount
        previousPinkCount = pinkCount
        previousWhiteCount = whiteCount
        if((currentFrame == initialFrame + 1) or currentFrame % frameCheck == 0):
            redCount = 0
            yellowCount = 0
            greenCount = 0
            brownCount = 0
            blueCount = 0
            pinkCount = 0
            whiteCount = 0
            checkBallCount = True
        else:
            checkBallCount = False
        for key, value in upper.items():
            kernal = np.ones((5,5), np.uint8)
            mask = cv2.inRange(hsv, lower[key], upper[key])
            # mask = cv2.erode(mask, kernal, iterations=1)
            # mask = cv2.dilate(mask, kernal, iterations=1)
            # Morphology doesn't appear to be required with the new lighting
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
            # cv2.imshow(key, mask)

            # Add the blur and the threshold function to get make the results more circular 
            # They are currently not in as they're not needed at this stage and just slow things down
            # mask = cv2.GaussianBlur(mask, (7,7), 0)
            # kernal = np.ones((6,6), np.uint8)
            # mask = cv2.erode(mask, kernal, iterations=1)
            finalMask = mask
            # thresh = cv2.threshold(finalMask, 127, 255, 0)[-1]
            # contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            contours = cv2.findContours(finalMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            i = 0
            
            if(key == "red" and calculateBallSizes):
                averagePeremiter, maxPerimeter = getAverageAndMaxPerimeter(contours)
                calculateBallSizes = False
                print("average: " + str(averagePeremiter))
                print("max: " + str(maxPerimeter))

            connectedContours = False
            for c in contours:
                
                numberOfBallsConnected = 0
                if(key == 'yellow'):
                    previousYellowX = cX
                    previousYellowY = cY

                # Get X and Y of contour
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                else:
                    cX, cY = 0, 0

                if(key != 'red'):
                    center = (cX, cY)
                    ballCoords[key].appendleft(center)


                # TODO: Automatically detect average perimeters and largest contour size
                if(key == 'red'):
                    currentContourSize = cv2.arcLength(c, True)
                    # The largest contour size is around 40 so just add a bit more 
                    cv2.circle(frame, (cX, cY), 5, (255,255,255), -1)
                    if(currentContourSize > (averagePeremiter + 5)):
                        # cv2.putText(frame, str(key), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,), 2)
                        cv2.circle(frame, (cX, cY), 5, (255,0,0), -1)

                        connectedContours = True
                        numberOfBallsConnected = currentContourSize / averagePeremiter
                        # Subtract one as if we don't, we end up counting the one big connected contor plus the actual number of balls
                        numberOfBallsConnected = int(round(numberOfBallsConnected)) - 1
                    else:
                        # cv2.circle(frame, (cX, cY), 5, (255,255,255), -1)
                        # cv2.putText(frame, str(key), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                        pass
                else: 
                    cv2.circle(frame, (cX, cY), 5, (255,255,255), -1)
                    cv2.putText(frame, str(key), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

                i += 1
                    
                if(checkBallCount):
                    # When counting the number of balls make sure to reset the ball count at the beginning of the while loop
                    if(key == 'red'):
                        # Need check if connected contours 
                        if(connectedContours):
                            redCount += numberOfBallsConnected
                        redCount += 1
                    if(key == 'yellow'):
                        yellowCount += 1
                        previousYellowX = cX
                        previousYellowY = cY

                    if(key == 'green'):
                        greenCount += 1
                    
                    if(key == 'brown'):
                        brownCount += 1

                    if(key == 'blue'):
                        blueCount += 1

                    if(key == 'pink'):
                        pinkCount += 1

                    if(key == 'white'):
                        whiteCount += 1

        for key, value in ballCoords.items():
            if(len(ballCoords[key]) >= 15):
                dX = ballCoords[key][0][0] - ballCoords[key][10][0]
                dY = ballCoords[key][0][1] - ballCoords[key][10][1]
                if(np.abs(dX) >= 10 or np.abs(dY) >= 10):
                    ballMoving[key] = True
                else:
                    ballMoving[key] = False
        

        if(checkBallCount):
            # Every 5 frames check if the number of reds detected has changed
            # Not equal to is used to help the with calculating the confidence
            if(redCount != previousRedCount):
                # If it has (and it's not the first frame otherwise the confidence value will be incorrect) increment the confidence
                if(currentFrame != initialFrame + 1):
                    # The higher the number means less confidence in the pot as redCount has changed value a lot 
                    # The constant changing of value means something has temporarly obstructed view of the ball
                    ballPottedConfidence += 1
                
            if(yellowCount != previousYellowCount):
                if(currentFrame != initialFrame + 1):
                    yellowPotConfidence += 1
            if(yellowCount >= 1):
                yellowPotted = False

            if(greenCount != previousGreenCount):
                if(currentFrame != initialFrame + 1):
                    greenPotConfidence += 1
            if(greenCount >= 1):
                greenPotted = False

            if(brownCount != previousBrownCount):
                if(currentFrame != initialFrame + 1):
                    brownPotConfidence += 1
            if(brownCount >= 1):
                brownPotted = False

            if(blueCount != previousBlueCount):
                if(currentFrame != initialFrame + 1):
                    bluePotConfidence += 1
            if(blueCount >= 1):
                bluePotted = False

            if(pinkCount != previousPinkCount):
                if(currentFrame != initialFrame + 1):
                    pinkPotConfidence += 1
            if(pinkCount >= 1):
                pinkPotted = False

            if(whiteCount != previousWhiteCount):
                if(currentFrame != initialFrame + 1):
                    whitePotConfidence += 1
            if(whiteCount >= 1):
                whitePotted = False

        # print(whitePotConfidence)
        # Every 50 frames check if a ball has been potted (checking every 50 frames give some time to get a confidence values)
        if(currentFrame % 50 == 0):
            # Predicted red count = 10
            # If the red count ever becomes greater than the number of reds the system has found
            # That means a ball has been obscured for a long enough time for it to be detected as potted
            # But obviously wasn't potted and must have just been covered by a player taking a shot
            # False pot detected (i.e hand cover etc)
            
            if(redCount > totalReds):
                print("false pot detected on " + str(numberOfRedsPotted) + " balls")
                totalReds += numberOfRedsPotted
                # With a false pot been detected, we need to update the database and remove points that were added with that false pot
                updatePoints(gameId, numberOfRedsPotted, True)

                numberOfRedsPotted = 0
                totalReds = redCount
            else:
                # redCount < totalReds means a ball has lost detection and so has been potted
                # if the confidence values is less than 2 it means there was little flucation in the redCount so we can be confident a ball may have been potted
                if(redCount < totalReds and ballPottedConfidence <= 2):
                    print("red potted")
                    numberOfRedsPotted = totalReds - redCount
                    totalReds = (totalReds) - (totalReds - redCount)
                    ballPottedConfidence = 0
                    updatePoints(gameId, numberOfRedsPotted)
                    # difference = frameFromVideoStart - ballDetectionRate
                    # ballDetectionRate += difference
                
                ballPottedConfidence = 0
            
            if(yellowCount < 1 and yellowPotConfidence <= 2 and not yellowPotted and ballMoving['yellow']):
                print('yellow potted')
                yellowPotted = True
                yellowPotConfidence = 0
                updatePoints(gameId, 2)

            yellowPotConfidence = 0

            if(greenCount < 1 and greenPotConfidence <= 2 and not greenPotted and ballMoving['green']):
                print('green potted')
                greenPotted = True
                greenPotConfidence = 0
                updatePoints(gameId, 3)

            greenPotConfidence = 0
            
            if(brownCount < 1 and brownPotConfidence <= 2 and not brownPotted and ballMoving['brown']):
                print('brown potted')
                brownPotted = True
                brownPotConfidence = 0
                updatePoints(gameId, 4)

            brownPotConfidence = 0

            if(blueCount < 1 and bluePotConfidence <= 2 and not bluePotted and ballMoving['blue']):
                print('blue potted')
                bluePotted = True
                bluePotConfidence = 0
                updatePoints(gameId, 5)

            bluePotConfidence = 0
            
            if(pinkCount < 1 and pinkPotConfidence <= 2 and not pinkPotted and ballMoving['pink']):
                print('pink potted')
                pinkPotted = True
                pinkPotConfidence = 0
                updatePoints(gameId, 6)

            pinkPotConfidence = 0

            if(whiteCount < 1 and whitePotConfidence <= 2 and not whitePotted and ballMoving['white']):
                print('white potted')
                whitePotted = True
                whitePotConfidence = 0
                updatePoints(gameId, 4, False, True)

            whitePotConfidence = 0

        cv2.imshow('Computer Vision System', frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) == ord('p'):

            while True:
                key2 = cv2.waitKey(1) or 0xff
                cv2.imshow('Computer Vision System', frame)

                if key2 == ord('p'):
                    break
        
        frameFromVideoStart += 1

    cv2.destroyAllWindows()
     # Connect to database using ssh keys 
    cap.release()

def getAverageAndMaxPerimeter(contours):
    averagePeremiter = 0
    ballPerimeters = []
    for c in contours:
        currentContourSize = cv2.arcLength(c, True)
        averagePeremiter += currentContourSize
        ballPerimeters.append(currentContourSize)
    
    averageSize = np.average(ballPerimeters)
    maxPerimeter = max(ballPerimeters)

    return averageSize, maxPerimeter

def getActivePlayer(gameId):
    res = requests.get('https://ukce.danjscott.co.uk/api/game/active_player/' + str(gameId))
    print(res.json())
    activePlayer = res.json()['active_player']
    return activePlayer
    # selectQuery = '''SELECT active_player FROM games WHERE id = %s;'''
    # cursor.execute(selectQuery, (gameId))
    # activePlayer = cursor.fetchone()[0]

    # return activePlayer

def updatePoints(gameId, points, falsePot=False, whitePotted=False):
    activePlayer = getActivePlayer(gameId)
    data = {
        'activePlayer': activePlayer,
        'points': points
    }         
    url = 'https://ukce.danjscott.co.uk/api/game/update/' + str(gameId)
    if(falsePot):
        url += '?falsePot=true'    
    if(whitePotted):
        url += '?whitePotted=true'     
    print(url)   
    print(data)
    res = requests.post(url, data=data)
    print(res)

async def start(websocket, path):
    instruction = await websocket.recv()
    data = instruction.split('#')
    # print(data[1])
    data
    if(data[0] == 'start'):
        gameId = data[1]
        # playerTwo = data[2]
        print('Starting Game')
        computerVisionSystem(gameId)

def main():
    # computerVisionSystem(169)
    machineIp = socket.gethostbyname(socket.gethostname()) 
    print(socket.gethostbyname(socket.gethostname()))
    data = {
        'ip': machineIp
    }
    res = requests.post('https://ukce.danjscott.co.uk/api/game', data=data)
    if(res.status_code == 200):
        print('Waiting for game to start')
        start_server = websockets.serve(start, machineIp, 8765)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    else:
        print('Unable to start')
        

if __name__ == "__main__": main()

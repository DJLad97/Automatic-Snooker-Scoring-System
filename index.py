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
from collections import deque
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
from dotenv import load_dotenv


def computerVisionSystem(gameId):
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

    # cap = cv2.VideoCapture("udp://127.0.0.1:10000")
    cap = cv2.VideoCapture("ball-clump-test.mov")
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
    #   'black':  (103,56,16), # YCrCb (old)
    #   'black':  (0,96,84), # YCrCb
    # 'white': (223,108,118) #YCrCb
    'white': (0,0,200) #HSV
    }

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
    #   'black':  (133,156,88), # YCrCb (old)
    #   'black':  (49,126,179), # YCrCb
    # 'white': (255,129,137) #YCrCb
    'white': (78,40,255) # HSV
    }

    ballCoords = {
        'white': deque(maxlen=32),
        'yellow': deque(maxlen=32),
        'green': deque(maxlen=32),
        'brown': deque(maxlen=32),
        # 'blue': deque(maxlen=32),
        # 'pink': deque(maxlen=32),
        # 'black': deque(maxlen=32)
    }

    ballMoving = {
        'white': False,
        'yellow': False,
        'green': False,
        'brown': False,
        'blue': False,
        'pink': False,
        'black': False
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
    previousYellowX = 0
    previousYellowY = 0
    yellowCoords = deque(maxlen=32)
    yellowMoving = False


    previousGreenCount = 0
    greenPotConfidence = 0
    greenCount = 0
    greenPotted = False

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

    whiteCoords = deque(maxlen=32)

    
    cX = 0
    cY = 0

    # initialFrame = 1600 # Just before yellow is potted
    initialFrame = 500 
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

        # cv2.imshow('res', hsv)

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
        if((currentFrame == initialFrame + 1) or currentFrame % frameCheck == 0):
            redCount = 0
            yellowCount = 0
            greenCount = 0
            brownCount = 0
            blueCount = 0
            pinkCount = 0
            checkBallCount = True
        else:
            checkBallCount = False
            # previousRedCount = redCount
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
            # print(key + ': ' + str(len(contours)))
            i = 0
            
            if(key == "red" and calculateBallSizes):
                averagePeremiter, maxPerimeter = getAverageAndMaxPerimeter(contours)
                calculateBallSizes = False
                print("average: " + str(averagePeremiter))
                print("max: " + str(maxPerimeter))

            connectedContours = False
            for c in contours:
                # if(i == len(contours) - 1):
                    # previousRedCount = redCount + 1
                # else:
                
                numberOfBallsConnected = 0
                if(key == 'yellow'):
                    previousYellowX = cX
                    previousYellowY = cY
                # The following code is only needed to show what has been detected
                # Can be removed in final version to improve fps
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                else:
                    cX, cY = 0, 0

                if(key != 'red' and key != 'blue' and key != 'pink'):
                    center = (cX, cY)
                    ballCoords[key].appendleft(center)


                # average perimeter = 38.6685714 (hardcoded for this window width, ball size etc, )
                # print(cv2.arcLength(c, True))
                # TODO: Automatically detect average perimeters and largest contour size
                if(key == 'red'):
                    currentContourSize = cv2.arcLength(c, True)
                    # averagePeremiter += currentContourSize
                    # The largest contour size is around 40 so just add a bit more 
                    if(currentContourSize > (averagePeremiter + 5)):
                        # cv2.putText(frame, str(key), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,), 2)
                        # cv2.circle(frame, (cX, cY), 5, (255,0,0), -1)

                        connectedContours = True
                        numberOfBallsConnected = currentContourSize / averagePeremiter
                        # numberOfBallsConnected = currentContourSize / 38.6685714
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
                            # print(numberOfBallsConnected)
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

        # print(whiteCoords)
        for key, value in ballCoords.items():
            if(len(ballCoords[key]) >= 15):
                dX = ballCoords[key][0][0] - ballCoords[key][10][0]
                dY = ballCoords[key][0][1] - ballCoords[key][10][1]
                if(np.abs(dX) >= 10 or np.abs(dY) >= 10):
                    # print(key + ' ball is moving')
                    ballMoving[key] = True
                else:
                    # print(key + ' ball is not moving')
                    ballMoving[key] = False
            
        if(checkBallCount):
            # Every 5 frames check if the number of reds detected has changed
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


        # Every 50 frames check if a ball has been potted (checking every 50 frames give some time to get a confidence values)
        if(currentFrame % 50 == 0):
            # False pot detected (i.e hand cover etc)
            # Predicted red count = 10
            # If the red count ever becomes greater than the number of reds the system has found
            # That means a ball has been obscured for a long enough time for it to be detected as potted
            # But obviously wasn't potted and must have just been covered by a player taking a shot
            # RENAME the predictedRedCount
            if(redCount > totalReds):
                print("false pot detected on " + str(numberOfRedsPotted) + " balls")
                totalReds += numberOfRedsPotted
                # With a false pot been detected, we need to update the database and remove points that were added with that false pot
                with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                    conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                    with conn.cursor() as cursor:
                        # selectQuery = '''SELECT active_player FROM games WHERE id = %s;'''
                        # cursor.execute(selectQuery, (gameId))
                        # activePlayer = cursor.fetchone()[0]
                        activePlayer = getActivePlayer(cursor, gameId)
                        print(activePlayer)

                        if(activePlayer == 'player_one'): 
                            query = '''UPDATE games SET player_one_points = player_one_points - %s WHERE id = %s;'''
                        else:
                            query = '''UPDATE games SET player_two_points = player_two_points - %s WHERE id = %s;'''

                        print(query)
                        cursor.execute(query, (numberOfRedsPotted, gameId))
                        # Simple query for that just decrements the points count
                        # query = '''UPDATE games SET points = points - %s WHERE id = %s;'''
                    
                    conn.commit()
                    conn.close()
                    
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
                    # Connect to database using ssh keys 
                    with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                        conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                        with conn.cursor() as cursor:
                            activePlayer = getActivePlayer(cursor, gameId)
                            print(activePlayer)

                            if(activePlayer == 'player_one'): 
                                query = '''UPDATE games SET player_one_points = player_one_points + %s WHERE id = %s;'''
                            else:
                                query = '''UPDATE games SET player_two_points = player_two_points + %s WHERE id = %s;'''

                            # Simple query for that just increments the points count
                            # query = '''UPDATE games SET points = points + %s WHERE id = %s;'''
                            # query = '''UPDATE games SET player_one_points = points + %s WHERE id = %s;'''
                            cursor.execute(query, (numberOfRedsPotted, gameId))
                        
                        conn.commit()
                        conn.close()
                ballPottedConfidence = 0
            
            if(yellowCount < 1 and yellowPotConfidence <= 2 and not yellowPotted and ballMoving['yellow']):
                print('yellow potted')
                yellowPotted = True
                yellowPotConfidence = 0
                with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                    conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                    with conn.cursor() as cursor:
                        activePlayer = getActivePlayer(cursor, gameId)
                        print(activePlayer)

                        if(activePlayer == 'player_one'): 
                            query = '''UPDATE games SET player_one_points = player_one_points + 2 WHERE id = %s;'''
                        else:
                            query = '''UPDATE games SET player_two_points = player_two_points + 2 WHERE id = %s;'''
                        # Simple query for that just decrements the points count
                        # query = '''UPDATE games SET points = points + 2 WHERE id = %s;'''
                        cursor.execute(query, (gameId))
                    
                    conn.commit()
                    conn.close()
            yellowPotConfidence = 0

            if(greenCount < 1 and greenPotConfidence <= 2 and not greenPotted and ballMoving['green']):
                print('green potted')
                greenPotted = True
                greenPotConfidence = 0
                with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                    conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                    with conn.cursor() as cursor:
                        # Simple query for that just decrements the points count
                        # selectQuery = '''SELECT active_player FROM games WHERE id = %s;'''
                        # cursor.execute(selectQuery)
                        # result = cursor.fetchall()
                        activePlayer = getActivePlayer(cursor, gameId)
                        print(activePlayer)

                        if(activePlayer == 'player_one'): 
                            query = '''UPDATE games SET player_one_points = player_one_points + 3 WHERE id = %s;'''
                        else:
                            query = '''UPDATE games SET player_two_points = player_two_points + 3 WHERE id = %s;'''
                        # query = '''UPDATE games SET points = points + 3 WHERE id = %s;'''
                        cursor.execute(query, (gameId))
                    
                    conn.commit()
                    conn.close()
            greenPotConfidence = 0
            
            if(brownCount < 1 and brownPotConfidence <= 2 and not brownPotted and ballMoving['brown']):
                print('brown potted')
                brownPotted = True
                brownPotConfidence = 0
                with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                    conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                    with conn.cursor() as cursor:
                        activePlayer = getActivePlayer(cursor, gameId)
                        print(activePlayer)

                        if(activePlayer == 'player_one'): 
                            query = '''UPDATE games SET player_one_points = player_one_points + 4 WHERE id = %s;'''
                        else:
                            query = '''UPDATE games SET player_two_points = player_two_points + 4 WHERE id = %s;'''
                        # Simple query for that just decrements the points count
                        # query = '''UPDATE games SET points = points + 4 WHERE id = %s;'''
                        cursor.execute(query, (gameId))
                    
                    conn.commit()
                    conn.close()
            brownPotConfidence = 0

            if(blueCount < 1 and bluePotConfidence <= 2 and not bluePotted and ballMoving['blue']):
                print('blue potted')
                bluePotted = True
                bluePotConfidence = 0
                with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                    conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                    with conn.cursor() as cursor:
                        activePlayer = getActivePlayer(cursor, gameId)
                        print(activePlayer)

                        if(activePlayer == 'player_one'): 
                            query = '''UPDATE games SET player_one_points = player_one_points + 5 WHERE id = %s;'''
                        else:
                            query = '''UPDATE games SET player_two_points = player_two_points + 5 WHERE id = %s;'''
                        # Simple query for that just decrements the points count
                        # query = '''UPDATE games SET points = points + 5 WHERE id = %s;'''
                        cursor.execute(query, (gameId))
                    
                    conn.commit()
                    conn.close()
            bluePotConfidence = 0
            
            if(pinkCount < 1 and pinkPotConfidence <= 2 and not pinkPotted):
                print('pink potted')
                pinkPotted = True
                pinkPotConfidence = 0
                with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                    conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

                    with conn.cursor() as cursor:
                        activePlayer = getActivePlayer(cursor, gameId)
                        print(activePlayer)

                        if(activePlayer == 'player_one'): 
                            query = '''UPDATE games SET player_one_points = player_one_points + 6 WHERE id = %s;'''
                        else:
                            query = '''UPDATE games SET player_two_points = player_two_points + 6 WHERE id = %s;'''
                        # Simple query for that just decrements the points count
                        # query = '''UPDATE games SET points = points + 6 WHERE id = %s;'''
                        cursor.execute(query, (gameId))
                    
                    conn.commit()
                    conn.close()
            pinkPotConfidence = 0
            


        # May not be needed
        # res = cv2.bitwise_and(frame,frame, mask = finalMask)

        # Display test for number of red balls
        # cv2.putText(frame, "Yellows detected: " + str(yellowCount), (250, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        # cv2.putText(frame, "Pink detected: " + str(pinkCount), (50, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 2)
        # cv2.putText(frame, "Total Reds: " + str(totalReds), (250, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        # cv2.putText(frame, "Red Detected: " + str(redCount) + " - " + str(previousRedCount), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(frame, "Pinks Detected: " + str(pinkCount), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)


        cv2.imshow('res', frame)
        # cv2.imshow('mask', finalMask)

        # if cv2.waitKey(25) & 0xFF == ord('n'):
        #     currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        #     cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame + 500)
        # if cv2.waitKey(25) & 0xFF == ord('p'):
        #     currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        #     cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame - 500)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
     # Connect to database using ssh keys 
    cap.release()

    # Set player score to 0 when exiting app
    # with SSHTunnelForwarder( (ssh_host, ssh_port), ssh_username=ssh_user, ssh_pkey=mypkey, remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    #     conn = pymysql.connect(host='127.0.0.1', user=sql_username, passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)

    #     with conn.cursor() as cursor:
    #         # Simple query for that just increments the points count
    #         query = '''UPDATE games SET points = 0 WHERE id = %s;'''
    #         cursor.execute(query, (gameId))
        
    #     conn.commit()
    #     conn.close()

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

def getActivePlayer(cursor, gameId):
    selectQuery = '''SELECT active_player FROM games WHERE id = %s;'''
    cursor.execute(selectQuery, (gameId))
    activePlayer = cursor.fetchone()[0]

    return activePlayer

async def start(websocket, path):
    instruction = await websocket.recv()
    print(f"< {instruction}")
    data = instruction.split('#')
    # print(data[1])
    if(data[0] == 'start'):
        gameId = data[1]
        # playerTwo = data[2]
        computerVisionSystem(gameId)
    # computerVisionSystem()


def main():
    start_server = websockets.serve(start, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__": main()

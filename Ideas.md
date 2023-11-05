## Ideas
### Tracking System
##### Calibration Process:
- Places individual coluored ball under the camera and have the system try different colour ranges to accurate range for the ball
##### Rules System:
- Need to determine what colour ball is currently active e.g Red or coloured ball
- Detect if invalid ball has been hit 
##### Tracking:
- Use a binary image as input for optical flow 
- Look into flow field for own tracking
### App
Have some sort of progress section where the user can track their breaks and other stats like that 
Game stats, e.g fouls, highest break, shot time

## Challenges faced/upcoming:
- Trying to access webcam from OpenCV, caused by new Mojave update which added more security to what applications can access   mac hardware, fixed by using first party terminal 
- When I first started work on the system, I struggled in finding colour range for each ball. But fortunately I found a tool   that would take an image and then allow me to adjust sliders to filter out the background colours and only leave the         colour I wanted
- When setting up an actual pool/snooker table the lighting that I had use interfered quite heavily with the way the system    detected and tracked the balls. As a result I'm currently researching different tracking methods and colour space            (currently using the HSV colour space for colour detection)
- There are some snooker rules where you gain points if fouled.
  E.g no ball hit, hit a red ball when you need to hit a coloured ball and vice versa, white ball potted
  Implementing most of these rules will be quite a challenge as it will involve more than just tracking and detecting the balls (i.e will need to detect collision)

## Meeting Notes:
- Use a binary image as input for optical flow 
- Look into flow field for own tracking 
- Get complete prototype working, with score showing on app 
- When detecting pink, look for the pink as it will always start in the same place

## General Notes
- Talk about the different approaches used to create the system (e.g lighting, tracking algorithms, colour spaces)
- Explain why I have used the numbers that I've used to check frames in the confidence system and not any other number (Run some tests against other numbers to justify my decision for choosing those numbers)
- Generate graph for the confidence number
- Trello board: https://trello.com/b/fotFIF7U/dissertation

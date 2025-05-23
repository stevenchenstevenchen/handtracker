#This is a support Module mainly for the speech from text and also to aid the
#System into knowing when a finger is up or when a finger is down based on the
#joints

import cv2
import mediapipe as freedomtech
from gtts import gTTS
import os

drawingModule = freedomtech.solutions.drawing_utils
handsModule = freedomtech.solutions.hands

mod=handsModule.Hands()


h=480
w=640

def speak(a):
    tts = gTTS(text=a, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
def findpostion(frame1):
    """
    returns a list of [idx, x, y]
    where idx is the index for the specfic joint
    id = 0 wrist
    id = 4 thumb
    8 index
    12 middle
    16 pinky
    """
    hands=[]
    results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
       for handLandmarks in results.multi_hand_landmarks:
            drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
            # new_hand = []
            for id, pt in enumerate (handLandmarks.landmark):
                x = int(pt.x * w)
                y = int(pt.y * h)
                hands.append([id,x,y])
                # new_hand.append([id,x,y])
            # hands.append(new_hand)

    return hands            


#check rockstar 🤘 pinky up, index up, thumb up, everything else down
def rockstar(fingers):
    #fingers [index, middle, ring, pinkies, thumb]
    if fingers and fingers[0] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[2] == 0 and fingers[1] == 0:
        # print("True")
        return True
    # print("False")
    return False

#check pause ✊ everything down
def pause(fingers):
    #fingers [index, middle, ring, pinkies, thumb]
    if fingers and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[2] == 0 and fingers[1] == 0:
        print("True")
        return True
    print("False")
    return False

#check wave 🖐 everything up
def wave(fingers):
    #fingers [index, middle, ring, pinkies, thumb]
    if fingers and fingers[0] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[2] == 1 and fingers[1] == 1:
        # print("True")
        return True
    # print("False")
    return False

#check tailWag 👉 Gun sign
def tailWag(fingers):
    #fingers [index, middle, ring, pinkies, thumb]
    if fingers and fingers[0] == 1 and fingers[3] == 0 and fingers[4] == 1 and fingers[2] == 0 and fingers[1] == 0:
        # print("True")
        return True
    # print("False")
    return False

#check dab 🤙 sign
def dab(fingers):
    #fingers [index, middle, ring, pinkies, thumb]
    if fingers and fingers[0] == 0 and fingers[3] == 1 and fingers[4] == 1 and fingers[2] == 0 and fingers[1] == 0:
        # print("True")
        return True
    # print("False")
    return False


def findnameoflandmark(frame1):
     """
     list of names
     """
     list=[]
     results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
     if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:


            for point in handsModule.HandLandmark:
                 list.append(str(point).replace ("< ","").replace("HandLandmark.", "").replace("_"," ").replace("[]",""))
     return list





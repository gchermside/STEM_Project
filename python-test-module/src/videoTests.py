import cv2
import mediapipe as mp
import json
import Hand
import time
import Main
import os
print("Hello world")
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


#reads data.JSON into handStoarage
def readVideoFile():
    with open('videoData.json', 'r') as file:
        jsonReadableStorage = json.load(file)

    return [
        Hand.fromJson(handJson) for handJson in jsonReadableStorage
    ]
videoStorage = readVideoFile()
previousHandPics = []
handStopped = False
videoStarted = False
videoHands = []
waitTime = .2
cycleNum = 1

# add wait key. window waits until user presses a key
cv2.waitKey(0)
# and finally destroy/close all open windows
cv2.destroyAllWindows()

def isSame(previousHandPics):
    dif1 = compareHands(previousHandPics[0], hand)
    dif2 = compareHands(previousHandPics[1], hand)
    if dif1 < .05 and dif2 <.05:
        return True


# compares two hands and returns a number that is greater the farther they are from each other
def compareHands(hand1, hand2):
    difTotal = 0
    for i in range(0,21):
        currentX = hand1.landmarks[i][0] - hand2.landmarks[i][0]
        currentX = currentX * currentX
        currentY = hand1.landmarks[i][1] - hand2.landmarks[i][1]
        currentY = currentY * currentY
        currentZ = hand1.landmarks[i][2] - hand2.landmarks[i][2]
        currentZ = currentZ * currentZ
        curPointDif = currentX + currentY + currentZ
        difTotal = difTotal + curPointDif
        # hand1T = touching(hand1)
        # hand2T = touching(hand2)
        # for i in range(0, 4):
        #     difTotal = difTotal + abs(hand1T[i]-hand2T[i])
    return difTotal

def compareVideoHands(vh1, vh2):
    if len(vh1) <=4 or len(vh2) <=4:
        return -1
    difTotal = 0
    difTotal += compareHands(vh1[0], vh2[0])
    middle1 = round(len(vh1)/2)
    middle2 = round(len(vh2)/2)
    difTotal += compareHands(vh1[middle1], vh2[middle2])
    difTotal += compareHands(vh1[round(middle1/2)], vh2[round(middle2/2)])
    difTotal += compareHands(vh1[round(len(vh1)/4*3)], vh2[round(len(vh2)/4*3)])
    difTotal += compareHands(vh1[len(vh1)-1], vh2[len(vh2)-1])
    return difTotal/5

#function that addes a new hand picture to hand storage
#it will either put it in a list of other hands for the same word
# or if it is a unique word, it will make a new list only including that hand for that word.
# def addNewWord(word, hand):
#     if word != "none":
#         if word in handStorage:
#             handStorage[word].append(hand)
#         else:
#             handStorage[word] = [hand]
#     else:
#         print("ok, we won't store that photo for you")

# this function points moves the hand so the wrist is at 0,0 and makes it a consistant
# porportion(the length between point 0 and 1 will always be the same on hands)
def regularize(hand):
    xShift = hand.landmarks[0][0]
    yShift = hand.landmarks[0][1]
    zShift = hand.landmarks[0][2]
    for lm in hand.landmarks:
        lm[0] = lm[0] - xShift
        lm[1] = lm[1] - yShift
        lm[2] = lm[2] - zShift
    p1 = hand.landmarks[1]
    mult = 1/(((p1[0])**2 + (p1[0])**2 + (p1[2])**2)**(1/2))
    for lm in hand.landmarks:
        lm[0] = lm[0] * mult
        lm[1] = lm[1] * mult
        lm[2] = lm[2] * mult

#function that returns a list of the most similar hands in handStorage to the passed in hand object
# def find(hand):
#     words = [("no match", 150)]
#     for signName in handStorage.keys():
#         for possibleHand in handStorage[signName]:
#             closeness = compareHands(hand, possibleHand)
#             if closeness<150:
#                 for i in range(0,len(words)):
#                     if closeness<words[i][1]:
#                         words.insert(i,(signName, closeness))
#                         break
#     return words

#function that takes in a hand object and return an array of which fingertips are touching
#the thumb, from index to pinky
def touching(hand):
    fingers = [0, 0, 0, 0]
    howClose = .0075
    for i in range(8, 21):
        if i%4 == 0:
            pointDist = ((hand.landmarks[i][0]-hand.landmarks[4][0])**2 +
                         (hand.landmarks[i][1]-hand.landmarks[4][1])**2 +
                         (hand.landmarks[i][2]-hand.landmarks[4][2])**2)
            if(pointDist<howClose):
                fingers[i//4 - 2] = 1
    return fingers



#this is a function where I'm plauing around with pose
def readPose(poseResults):
    nose = [poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x,
            poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y,
            poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].z]
    right_index = [poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x,
                   poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y,
                   poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].z]
    # left_index = [poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x,
    #         poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y,
    #         poseResults.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].z]
    disRHandToFace = [abs(nose[0]-right_index[0]), abs(nose[1]-right_index[1]), abs(nose[2]-right_index[2])]
    print(nose)
    print(right_index)
    print(disRHandToFace)
    if(disRHandToFace[0]>.25 or disRHandToFace[1]>.25):
        print("your hand is far from your face")
    else:
        print("your hand is near your face")
    # print(left_index)



# For webcam input:
cap = cv2.VideoCapture(0)

#starts using pose
previousTime = time.time()
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    #starts using hand
    with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            #hand
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            handResults = hands.process(image)
            poseResults = pose.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if handResults.multi_hand_landmarks:
                for hand_landmarks in handResults.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            # draws on pose lines
            mp_drawing.draw_landmarks(
                image,
                poseResults.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            key_pressed =  cv2.waitKey(5)
            if key_pressed % 256 == 27:
                break
            if (time.time() - previousTime) > waitTime:
                try:
                    handResults.multi_hand_landmarks[0]
                except:
                    #this is just placeholder code
                    noHand = True
                else:
                    cv2.imshow('Capture', cv2.flip(image, 1))
                    #since mirroring is being wrong, I'm switching the handedness
                    isRightHand = True
                    if(handResults.multi_handedness[0] == "Right"):
                        isRightHand = False
                    hand = Hand.Hand(
                        isRightHand= isRightHand,
                        landmarks = [[lm.x, lm.y, lm.z] for lm in handResults.multi_hand_landmarks[0].landmark],
                        world_landmarks = [[lm.x, lm.y, lm.z] for lm in handResults.multi_hand_world_landmarks[0].landmark]
                    )
                    if videoStarted:
                        videoHands.append(hand)
                        fileName = "pics\\savedImage"+str(cycleNum)+".jpg"
                        cv2.imwrite(fileName, image)
                        print("pic added")
                        if cycleNum % 2 == 0:
                            if len(previousHandPics) >1:
                                if isSame(previousHandPics):
                                    print("you held still, I will stop capturing data")
                                    break;
                                previousHandPics = [previousHandPics[len(previousHandPics)-1]]
                            previousHandPics.append(hand)
                        previousTime = time.time()
                        cycleNum = cycleNum+1
                    else:
                        if handStopped:
                            if len(previousHandPics) >1:
                                if not isSame(previousHandPics):
                                    print("you started moving, I will start capturing data")
                                    videoHands.append(hand)
                                    fileName = "pics\\savedImage0.jpg"
                                    cv2.imwrite(fileName, image)
                                    videoStarted = True
                                    waitTime = .1
                                    previousHandPics = []
                                else:
                                    print("still still, start moving")
                                    previousHandPics = [previousHandPics[len(previousHandPics)-1]]
                            previousHandPics.append(hand)
                            previousTime = time.time()
                        else:
                            if len(previousHandPics) >1:
                                if isSame(previousHandPics):
                                    print("you held still, I will wait till you start")
                                    handStopped = True
                                else:
                                    print("not still, I'm still waiting")
                                previousHandPics = [previousHandPics[len(previousHandPics)-1]]
                            previousHandPics.append(hand)
                            previousTime = time.time()

print("you survived till the end!")
print(compareVideoHands(videoStorage, videoHands))


with open('videoData.json', 'w') as file:
    jsonThing = []
    for hand in videoHands:
        jsonThing.append(hand.toJson())
    json.dump(jsonThing, file, indent=2)



cap.release()
#
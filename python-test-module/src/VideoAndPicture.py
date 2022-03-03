
import cv2
import mediapipe as mp
import json
import Hand
import time
import Frame
import functions
import Pose

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose



def buildFrame(handResults, previousMovement):
    isRightHand = True
    if(handResults.multi_handedness[0] == "Right"):
        isRightHand = False
    hand1 = Hand.Hand(
        isRightHand= isRightHand,
        landmarks = [[lm.x, lm.y, lm.z] for lm in handResults.multi_hand_landmarks[0].landmark],
        world_landmarks = [[lm.x, lm.y, lm.z] for lm in handResults.multi_hand_world_landmarks[0].landmark]
    )
    movement = []
    movement.append(hand1.landmarks[0][0] - previousMovement[0])
    previousMovement[0] = hand1.landmarks[0][0]
    movement.append(hand1.landmarks[0][1] - previousMovement[1])
    previousMovement[1] = hand1.landmarks[0][1]
    movement.append(hand1.landmarks[0][2] - previousMovement[2])
    previousMovement[2] = hand1.landmarks[0][2]
    functions.regularize(hand1)
    hand2 = None
    try:
        handResults.multi_hand_landmarks[1]
    except:
        hand2 = None
    else:
        hand2 = Hand.Hand(
            isRightHand= not isRightHand,
            landmarks = [[lm.x, lm.y, lm.z] for lm in handResults.multi_hand_landmarks[1].landmark],
            world_landmarks = [[lm.x, lm.y, lm.z] for lm in handResults.multi_hand_world_landmarks[1].landmark]
        )
        functions.regularize(hand2)
    pose = None
    realFrame = Frame.videoFrame(hand1, hand2, pose, movement)

    return realFrame



def readVideoFile(file):
    with open(file, 'r') as file:
        jsonReadableStorage = json.load(file)
    return {
        signName: [[Frame.fromJson(frameJson) for frameJson in videoJson] for videoJson in jsonReadableStorage[signName]] for signName in jsonReadableStorage.keys()
    }

def isSame(previousFrames, frame):
    dif1 = functions.compareHands(previousFrames[0].hand1, frame.hand1)
    dif2 = functions.compareHands(previousFrames[1].hand1, frame.hand1)
    difMovment = previousFrames[1].movement[0] + previousFrames[1].movement[1] + previousFrames[1].movement[2]
    difMovment += frame.movement[0] + frame.movement[1] + frame.movement[2]
    print(f"difMovement is: {difMovment}")
    if dif1 < 15 and dif2 < 15 and difMovment <3:
        return True
    return False

def compareVideoHands(vh1, vh2):
    if len(vh1) <=4 or len(vh2) <=4:
        return -1
    difTotal = 0
    difTotal += functions.compareHands(vh1[0], vh2[0])
    middle1 = round(len(vh1)/2)
    middle2 = round(len(vh2)/2)
    difTotal += functions.compareHands(vh1[middle1], vh2[middle2])
    difTotal += functions.compareHands(vh1[round(middle1/2)], vh2[round(middle2/2)])
    difTotal += functions.compareHands(vh1[round(len(vh1)/4*3)], vh2[round(len(vh2)/4*3)])
    difTotal += functions.compareHands(vh1[len(vh1)-1], vh2[len(vh2)-1])
    return difTotal/5

print("hello world")
# add wait key. window waits until user presses a key
cv2.waitKey(0)
# and finally destroy/close all open windows
cv2.destroyAllWindows()


videoOrPicture = input("Do you want to take  video or picture? (type v or p)")
if videoOrPicture == "v":
    videoStorage = readVideoFile("video1Hand.json")
    previousFrames = []
    handStopped = False
    videoStarted = False
    currentVideo = []
    waitTime = .2
    cycleNum = 1
    previousMovement = [0,0,0]
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
                        currentFrame = buildFrame(handResults, previousMovement)
                        previousMovement = currentFrame.movement
                        if videoStarted:
                            currentVideo.append(currentFrame)
                            fileName = "pics\\savedImage"+str(cycleNum)+".jpg"
                            cv2.imwrite(fileName, image)
                            print("pic added")
                            if cycleNum % 2 == 0:
                                if len(previousFrames) >1:
                                    if isSame(previousFrames, currentFrame):
                                        print("you held still, I will stop capturing data")
                                        break
                                    previousFrames = [previousFrames[len(previousFrames)-1]]
                                previousFrames.append(currentFrame)
                            previousTime = time.time()
                            cycleNum = cycleNum+1
                        else:
                            if handStopped:
                                if len(previousFrames) >1:
                                    if not isSame(previousFrames, currentFrame):
                                        print("you started moving, I will start capturing data")
                                        currentVideo.append(currentFrame)
                                        fileName = "pics\\savedImage0.jpg"
                                        cv2.imwrite(fileName, image)
                                        videoStarted = True
                                        waitTime = .1
                                        previousFrames = []
                                    else:
                                        print("still still, start moving")
                                        previousFrames = [previousFrames[len(previousFrames)-1]]
                                previousFrames.append(currentFrame)
                                previousTime = time.time()
                            else:
                                if len(previousFrames) >1:
                                    if isSame(previousFrames, currentFrame):
                                        print("you held still, I will wait till you start")
                                        handStopped = True
                                    else:
                                        print("not still, I'm still waiting")
                                    previousFrames = [previousFrames[len(previousFrames)-1]]
                                previousFrames.append(currentFrame)
                                previousTime = time.time()
    print("you made it!")
    shouldFind = input("Please enter if you would like to find similar signs to this (yes or no): ")
    if shouldFind == "Yes" or shouldFind == "yes":
        listOfSimilarWords = functions.findVideo(currentVideo, videoStorage)
        print(f"Possible word matches are: {listOfSimilarWords}")
    signName = input("Type the sign name or none to delete ")
    functions.addNewThing(signName, currentVideo, videoStorage)
    with open('video1Hand.json', 'w') as file:
        jsonThing = {}
        for key, videos in videoStorage.items():
            jsonVideos = []
            for video in videos:
                jsonVideo = []
                for frame in video:
                    jsonVideo.append(frame.toJson())
                jsonVideos.append(jsonVideo)
            jsonThing[key] = jsonVideos
        json.dump(jsonThing, file, indent=2)

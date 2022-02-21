#imports
import cv2
import mediapipe as mp
import json
import Hand
import Frame
import Pose

print("Hello world")
#makes media pipe work very useful
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose




# reads data.JSON into frameStorage
def readFrameFile(file):
    with open(file, 'r') as file:
        jsonReadableStorage = json.load(file)
    return {
        signName: [Frame.fromJson(frameJson) for frameJson in jsonReadableStorage[signName]] for signName in jsonReadableStorage.keys()
    }
frame1Storage = readFrameFile('frames1Hand.json')
frame2Storage = readFrameFile('frames2Hand.json')

#reads data.JSON into handStorage
def readFile():
    with open('data.json', 'r') as file:
        jsonReadableStorage = json.load(file)

    return {
        signName: [Hand.fromJson(frameJson) for frameJson in jsonReadableStorage[signName]] for signName in jsonReadableStorage.keys()
    }

#this in incase the data in the file got overridden
# handStorage = readFile()
#
# frame1Storage = {
#     signName: [Frame.Frame(hand, None, None) for hand in handStorage[signName]] for signName in handStorage.keys()
# }





# add wait key. window waits until user presses a key
cv2.waitKey(0)
# and finally destroy/close all open windows
cv2.destroyAllWindows()





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


#function that addes a new frame picture to hand storage
#it will either put it in a list of other frames for the same word
# or if it is a unique word, it will make a new list only including that frame for that word.
def addNewFrame(word, frame):
    if word != "none":
        if frame.hand2 == None:
            if word in frame1Storage:
                frame1Storage[word].append(frame)
            else:
                frame1Storage[word] = [frame]
        else:
            if word in frame2Storage:
                frame2Storage[word].append(frame)
            else:
                frame2Storage[word] = [frame]

    else:
        print("ok, we won't store that photo for you")




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
def find(frame):
    words = [("no match", 150)]
    if frame.pose != None:
        #FIXME pose doesn't work
        if frame.hand2 != None:
            for signName in frame2Storage.keys():
                for possibleHand in frame2Storage[signName]:
                    closeness = compareHands(frame.hand1, possibleHand.hand1)
                    closeness += compareHands(frame.hand2, possibleHand.hand2)
                    if closeness<150:
                        for i in range(0,len(words)):
                            if closeness<words[i][1]:
                                words.insert(i,(signName, closeness))
                                break
            return words
        else:
            for signName in frame1Storage.keys():
                for possibleHand in frame1Storage[signName]:
                    closeness = compareHands(frame.hand1, possibleHand.hand1)
                    if closeness<150:
                        for i in range(0,len(words)):
                            if closeness<words[i][1]:
                                words.insert(i,(signName, closeness))
                                break
            return words
    else:
        if frame.hand2 != None:
            for signName in frame2Storage.keys():
                for possibleHand in frame2Storage[signName]:
                    closeness = compareHands(frame.hand1, possibleHand.hand1)
                    closeness += compareHands(frame.hand2, possibleHand.hand2)
                    if closeness<150:
                        for i in range(0,len(words)):
                            if closeness<words[i][1]:
                                words.insert(i,(signName, closeness))
                                break
            return words
        else:
            for signName in frame1Storage.keys():
                for possibleHand in frame1Storage[signName]:
                    closeness = compareHands(frame.hand1, possibleHand.hand1)
                    if closeness<150:
                        for i in range(0,len(words)):
                            if closeness<words[i][1]:
                                words.insert(i,(signName, closeness))
                                break
            return words




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

def writeFileFrame1():
    with open('frames1Hand.json', 'w') as file1:
        jsonFile1 = {}
        for key in frame1Storage.keys():
            keyList1 = []
            for frame in frame1Storage[key]:
                if frame.hand2 is None:
                    keyList1.append(frame.toJson())
                else:
                    print("error  writing to file, frame storage1 has hand2")
            if len(keyList1) >= 1:
                jsonFile1[key] = keyList1
        json.dump(jsonFile1, file1, indent=2)


def writeFileFrame2():
    with open('frames2Hand.json', 'w') as file:
        jsonThing = {
            key: [frame.toJson() for frame in frame2Storage[key]] for key in frame2Storage.keys()
        }
        json.dump(jsonThing, file, indent=2)


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
    if(disRHandToFace[0]>.25 or disRHandToFace[1]>.25):
        print("your hand is far from your face")
    else:
        print("your hand is near your face")
    # print(left_index)



# For webcam input:
cap = cv2.VideoCapture(0)

#starts using pose
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
            # mp_drawing.draw_landmarks(
            #     image,
            #     poseResults.pose_landmarks,
            #     mp_pose.POSE_CONNECTIONS,
            #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

            key_pressed =  cv2.waitKey(5)

            if key_pressed % 256 == 27:
                break
            elif key_pressed % 256 == 32:

                try:
                    handResults.multi_hand_landmarks[0]
                except:
                    print("no hand in frame")
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
                    poseNeeded = input("Please enter yes if the pose in important or no if it is not: ")
                    realFrame = Frame.Frame(hand, hand2, None)
                    if poseNeeded == "yes":
                        realFrame = Frame.Frame(hand, hand2, Pose.Pose([[lm.x, lm.y, lm.z] for lm in poseResults.pose_landmarks.landmark]))
                    readPose(poseResults)
                    fingersTouching = touching(hand)
                    print(f"thumb is touching these fingers: {fingersTouching}")
                    regularize(hand)
                    userInput = input("Please enter yes if that was an example handshape, none to delete, or find to find a match: ")
                    if(userInput == "find") :
                        guess = find(realFrame)
                        print(f"guess {guess}")
                        word = input("Please type what word it was supposed to be or none to delete the picture: ")
                        addNewFrame(word, realFrame)
                    elif(userInput == "yes"):
                        word = input("ok, and what word was it, or none to delete: ")
                        addNewFrame(word, realFrame)
                    else:
                        print("we won't store that photo")
                    writeFileFrame2()
                    writeFileFrame1()
                    shouldContinue = input("Would you like to continue? Type yes or no: ")
                    if(shouldContinue == "yes"):
                        print("ok, take another picture")
                    elif(shouldContinue == "no"):
                        break
                    else:
                        print("That wasn't a yes or no, I'm going to go break now, sorry.")




cap.release()
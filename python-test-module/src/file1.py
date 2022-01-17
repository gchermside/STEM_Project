import cv2
import mediapipe as mp
import json
import Hand
print("Hello world")
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

resultsList = []
with open('data.json', 'r') as file:
    handStorage = json.load(file)


# add wait key. window waits until user presses a key
cv2.waitKey(0)
# and finally destroy/close all open windows
cv2.destroyAllWindows()

def compareHands(hand1, hand2):
    difTotal = 0
    for i in range(0,21):
        currentX = hand1["landmarks"][i][0] - hand2["landmarks"][i][0]
        currentX = currentX * currentX
        currentY = hand1["landmarks"][i][1] - hand2["landmarks"][i][1]
        currentY = currentY * currentY
        currentZ = hand1["landmarks"][i][2] - hand2["landmarks"][i][2]
        currentZ = currentZ * currentZ
        curPointDif = currentX + currentY + currentZ
        difTotal = difTotal + curPointDif
    return difTotal

def regularize(hand):
    xShift = hand.landmark[0].x
    yShift = hand.landmark[0].y
    zShift = hand.landmark[0].z
    for lm in hand.landmark:
        lm.x = lm.x - xShift
        lm.y = lm.y - yShift
        lm.z = lm.z - zShift
    p1 = hand.landmark[1]
    mult = 1/(((p1.x)**2 + (p1.y)**2 + (p1.z)**2)**(1/2))
    for lm in hand.landmark:
        lm.x = lm.x * mult
        lm.y = lm.y * mult
        lm.z = lm.z * mult

def find(hand):
    word = "no match"
    sureness = 150
    for possibleMatch in handStorage:
        closeness = compareHands(hand, possibleMatch)
        if closeness<sureness:
            sureness = closeness
            word = possibleMatch["hand_shape"]
    return word


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
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
        elif key_pressed % 256 == 32:
            cv2.imshow('Capture', cv2.flip(image, 1))
            resultsList.append(results)
            #since mirroring is being wrong, I'm switching the handedness
            isRightHand = True
            if(results.multi_handedness[0] == "Right"):
                isRightHand = False
            regularize(results.multi_hand_landmarks[0])
            userInput = input("Please enter what handshape that was, none to delete the picture, or find to find what sign it is: ")
            if(userInput == "none") :
                print("ok, we won't store that photo")
            elif(userInput == "find") :
                hand = {
                    "hand_shape": "unknown",
                    "isRightHand": isRightHand,
                    "landmarks": [[lm.x, lm.y, lm.z] for lm in results.multi_hand_landmarks[0].landmark],
                    "world_landmarks": [[lm.x, lm.y, lm.z] for lm in results.multi_hand_world_landmarks[0].landmark],
                }
                guess = find(hand)
            else:
                hand = {
                    "hand_shape": userInput,
                    "isRightHand": isRightHand,
                    "landmarks": [[lm.x, lm.y, lm.z] for lm in results.multi_hand_landmarks[0].landmark],
                    "world_landmarks": [[lm.x, lm.y, lm.z] for lm in results.multi_hand_world_landmarks[0].landmark],
                }
                handStorage.append(hand)
            shouldContinue = input("Would you like to continue? Type yes or no: ")
            if(shouldContinue == "yes"):
                print("ok, take another picture")
            elif(shouldContinue == "no"):
                break
            else:
                print("That wasn't a yes or no, I'm going to go break now, sorry.")


    with open('data.json', 'w') as file:
        json.dump(handStorage, file, indent=2)


cap.release()
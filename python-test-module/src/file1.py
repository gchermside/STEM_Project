import cv2
import mediapipe as mp
import json
import Hand
print("Hello world")
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

resultsList = []

def readFile():
    with open('data.json', 'r') as file:
        jsonReadableStorage = json.load(file)

    return {
        signName: [Hand.fromJson(handJson) for handJson in jsonReadableStorage[signName]] for signName in jsonReadableStorage.keys()
    }
handStorage = readFile()

# add wait key. window waits until user presses a key
cv2.waitKey(0)
# and finally destroy/close all open windows
cv2.destroyAllWindows()

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

def addNewWord(word, hand):
    if word != "none":
        if word in handStorage:
            handStorage[word].append(hand)
        else:
            handStorage[word] = [hand]
    else:
        print("ok, we won't store that photo for you")


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

def find(hand):
    words = [("no match", 150)]
    for signName in handStorage.keys():
        for possibleHand in handStorage[signName]:
            closeness = compareHands(hand, possibleHand)
            if closeness<150:
                for i in range(0,len(words)):
                    if closeness<words[i][1]:
                        words.insert(i,(signName, closeness))
                        break
    return words


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
            hand = Hand.Hand(
                isRightHand= isRightHand,
                landmarks = [[lm.x, lm.y, lm.z] for lm in results.multi_hand_landmarks[0].landmark],
                world_landmarks = [[lm.x, lm.y, lm.z] for lm in results.multi_hand_world_landmarks[0].landmark]
            )
            fingersTouching = touching(hand)
            print(f"thumb is touching these fingers: {fingersTouching}")
            regularize(hand)
            userInput = input("Please enter yes if that was an example handshape, none to delete, or find to find a match: ")
            if(userInput == "find") :
                guess = find(hand)
                print(f"guess {guess}")
                word = input("Please type what word it was supposed to be or none to delete the picture: ")
                addNewWord(word, hand)
            elif(userInput == "yes"):
                word = input("ok, and what word was it, or none to delete: ")
                addNewWord((word, hand))
            else:
                print("we won't store that photo")
            shouldContinue = input("Would you like to continue? Type yes or no: ")
            if(shouldContinue == "yes"):
                print("ok, take another picture")
            elif(shouldContinue == "no"):
                break
            else:
                print("That wasn't a yes or no, I'm going to go break now, sorry.")


    with open('data.json', 'w') as file:
        jsonThing = {
            key: [hand.toJson() for hand in handStorage[key]] for key in handStorage.keys()
        }
        json.dump(jsonThing, file, indent=2)


cap.release()
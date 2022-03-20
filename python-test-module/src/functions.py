import array
import numpy
import math
from numpy import array

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



#cos similarity between two vectors(hands)
def cosSimilarity(hand1, hand2):
    # a*b=||a||*||b||*cos(theta)
    # CS = (a*b)/(||a||*||b||)
    # print("hi")
    # a = array([])
    # b = array([])
    gen1 = []
    gen2 = []
    for i in range(0,21):
        for g in range(0,3):
            gen1.append(hand1.landmarks[i][g])
            # a += hand1.landmarks[i][g]
    for i in range(0,21):
        for g in range(0,3):
            gen2.append(hand2.landmarks[i][g])
            # b += hand2.landmarks[i][g]
    a = array(gen1)
    b = array(gen2)
    c = a * b
    top = 0
    for y in c:
        top += y
    # print(f"Top is {top}")
    la = 0
    for j in a:
        la += j*j
    la = math.sqrt(la)
    lb = 0
    for j in b:
        lb += j*j
    lb = math.sqrt(lb)
    bottom = la*lb
    # print(f"Bottom is {bottom}")
    cs = (top/bottom)
    return cs


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


# this function points moves the hand so the wrist is at 0,0 and makes it a consistant
# porportion(the length between point 0 and 1 will always be the same on hands)
def regularizeJsonHand(originalHand):
    hand = originalHand
    xShift = hand[0]["x"]
    yShift = hand[0]["y"]
    zShift = hand[0]["z"]
    for lm in hand:
        lm["x"] = lm["x"] - xShift
        lm["y"] = lm["y"] - yShift
        lm["z"] = lm["z"] - zShift
    p1 = hand[1]
    mult = 1/(((p1["x"])**2 + (p1["y"])**2 + (p1["z"])**2)**(1/2))
    for lm in hand:
        lm["x"] = lm["x"] * mult
        lm["y"] = lm["y"] * mult
        lm["z"] = lm["z"] * mult
    return hand


def addNewThing(word, thing, dictionary):
    word.lower()
    if word != "none" and word != "None":
        if word in dictionary:
            dictionary[word].append(thing)
        else:
            dictionary[word] = [thing]
    else:
        print("ok, we won't store that photo for you")


def compareVideos(v1, v2):
    if len(v1) <=4 or len(v2) <=4:
        return -1
    difTotal = 0
    difTotal += compareVideoSpots(v1[0], v2[0])
    middle1 = round(len(v1)/2)
    middle2 = round(len(v2)/2)
    difTotal += compareVideoSpots(v1[middle1], v2[middle2])
    difTotal += compareVideoSpots(v1[round(middle1/2)], v2[round(middle2/2)])
    difTotal += compareVideoSpots(v1[round(len(v1)/4*3)], v2[round(len(v2)/4*3)])
    difTotal += compareVideoSpots(v1[len(v1)-1], v2[len(v2)-1])
    return difTotal/5

def compareVideoSpots(f1, f2):
    if f1.hand2 == None and f2.hand2 == None:
        return compareHands(f1.hand1, f2.hand1)
    if f1.hand2 != None and f2.hand2 != None:
        return (compareHands(f1.hand1, f2.hand1) + compareHands(f1.hand2, f2.hand2))/2
    else:
        return compareHands(f1.hand1, f2.hand1) + 50

def findVideo(video, storage):
    words = [("no match", 150)]
    for signName in storage.keys():
        for possibleMatch in storage[signName]:
            closeness = compareVideos(video, possibleMatch)
            if closeness<150:
                for i in range(0,len(words)):
                    if closeness<words[i][1]:
                        words.insert(i,(signName, closeness))
                        break
    return words


def regularlizeVideo(video):
    NUM_OF_FRAMES = 15
    length  = len(video)
    newVideo = []
    frames1 = 0
    frames2 = 0
    for frame in video:
        if len(frame) == 0:
            print("empty frame")
        elif len(frame) == 1:
            frames1 += 1
        else:
            print("two hands")
            frames2 += 1
    if frames1 == len(video):
        #This is a one handed sign
        print("one handed sign")
        if len(video) > NUM_OF_FRAMES:
            for i in range(0, NUM_OF_FRAMES):
                percent, spot = math.modf(length * i/NUM_OF_FRAMES)
                spotInt = int(length * i/NUM_OF_FRAMES)
                newHand = interpolateHand(video[spotInt][0], video[int(spotInt+1)][0], percent)
                newVideo.append([newHand])
            return newVideo
        else:
            print("as for now, probably too short")

    elif frames2 >= frames1:
        # this is a two handed sign
        print("not using two handed signs yet")
    else:
        print("this sign is ambiguous, will use later")
    return None


def interpolateCoordinate(p1, p2, percent):
    return ((p2-p1) * percent) + p1


def interpolatePoint(p1, p2, percent):
    newPoint = {'x': interpolateCoordinate(p1['x'], p2['x'], percent),
                'y': interpolateCoordinate(p1['y'], p2['y'], percent),
                'z': interpolateCoordinate(p1['z'], p2['z'], percent)}
    return newPoint


def interpolateHand(hand1, hand2, percent):
    newHand = []
    for point1 in hand1:
        for point2 in hand2:
            newPoint = interpolatePoint(point1, point2, percent)
            newHand.append(newPoint)
    return newHand


def vectorVideo(video):
    vector = []
    for frame in video:
        for hand in frame:
            for point in hand:
                vector.append(point['x'])
                vector.append(point['y'])
                vector.append(point['z'])
    return vector

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

def addNewThing(word, thing, dictionary):
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
s
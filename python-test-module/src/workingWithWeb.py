import boto3
import passwords
import os
import pickle
import json
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


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



def toVectorandRegularize(image):
    vector = []
    if len(image) == 1:
        for unRegHand in image:
            hand = regularizeJsonHand(unRegHand)
            for points in hand:
                vector.append(points["x"])
                vector.append(points["y"])
                vector.append(points["z"])
    return vector


def readPictureDic(dic):
    X = [] #data
    y = [] #targets
    for key, items in dic.items():
        if "  " in key:
            print("spaces, skipping")
        else:
            if len(key) >1:
                print("not single letter or number, skipping")
            else:
                for item in items:
                    vector = toVectorandRegularize(item)
                    if vector == [] or y == "":
                        print("dud, skipping")
                    else:
                        X.append(vector)
                        y.append(key)
    return X, y

def readVideoDic(dic):
    X = [] #data
    y = [] #targets
    for key, items in dic.items():
        for item in items:
            vector = vectorVideo(item)
            if vector == [] or y == "" or vector == None:
                print("dud, skipping")
            else:
                X.append(vector)
                y.append(key)
    return X, y



def vectorVideo(video):
    vector = []
    for frame in video:
        for hand in frame:
            for point in hand:
                try:
                    vector.append(point['x'])
                    vector.append(point['y'])
                    vector.append(point['z'])
                except:
                    print("error in vector")
                    print(f"hand is {hand}")
                    return None
    print('video vector len is ', len(vector))
    return vector


def machineLearning(X, y):
    XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size = .10)
    # print(f"length of training {len(XTrain)}")
    model = trainModel(XTrain, yTrain)
    prediction = model.predict(XTest)
    totalWrong = 0
    for i in range(0, len(yTest)):
        if prediction[i] != yTest[i]:
            totalWrong = totalWrong+1
        print(f"prediction {prediction[i]} is actually {yTest[i]}")
    print(f"percentage wrong: {totalWrong/len(yTest) * 100}")
    print(totalWrong)
    print(len(yTest))
    return (totalWrong/len(yTest) * 100), model

# percentage wrong: 2.4285714285714284

def trainModel(XTrain, yTrain):
    model = MLPClassifier(hidden_layer_sizes=(150,100,50), max_iter=2000,activation = 'relu',solver='adam',random_state=1) #change this line to test new models
    model.fit(XTrain, yTrain)
    return model


client = boto3.client(
    's3',
    aws_access_key_id = str(passwords.AWSAccessKeyId),
    aws_secret_access_key = str(passwords.AWSSecretKey),
    region_name = 'us-east-1'
)



def saveModel(model, fileName):
    with open(f"../models/{fileName}.pkl", "wb") as outfile:
        pickle.dump(model, outfile, protocol=5)


def loadModel(fileName):
    with open(f"../models/{fileName}.pkl", "rb") as infile:
        return pickle.load(infile)



def readLandmark(directory, subDir):
    landmarksJson = directory+"/"+subDir+"/landmarks.json"
    with open(landmarksJson, 'r') as landmarkFile:
        return json.load(landmarkFile)




def readInData():
    imageHandDic = {}
    videoHandDic = {}
    directory = "C:/Users/Genevieve/Documents/programming/STEM_Project/s3Data/uploads/"
    entries = os.listdir(directory)
    for subDir in entries:
        landmarksJson = directory+"/"+subDir+"/landmarks.json"
        infoJson = directory+"/"+subDir+"/info.json"
        with open(landmarksJson, 'r') as landmarkFile:
            jsonReadableLandmarks = json.load(landmarkFile)
            with open(infoJson, "r") as infoFile:
                jsonReadableInfo = json.load(infoFile)
                signName = jsonReadableInfo['signName']
                signName = signName.lower()
                try:
                    if jsonReadableInfo['isVideo'] == True:
                        addNewThing(signName, jsonReadableLandmarks, videoHandDic)
                    else:
                        addNewThing(signName, jsonReadableLandmarks, imageHandDic)
                except:
                    thisIsAPlaceHolder = 0
    return imageHandDic, videoHandDic


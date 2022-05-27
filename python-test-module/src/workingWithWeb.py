import passwords
import os
import pickle
import json
import library
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split



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
            hand = library.regularizeJsonHand(unRegHand)
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
    print("reading video dic")
    X = [] #data
    y = [] #targets
    for key, items in dic.items():
        for vector in items:
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





def saveModel(model, fileName):
    with open(f"../models/{fileName}.pkl", "wb") as outfile:
        print("going to dump model")
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
            try:
                with open(infoJson, "r") as infoFile:
                    jsonReadableInfo = json.load(infoFile)
                    if "  " in jsonReadableInfo['signName']:
                        print("bad name is ", jsonReadableInfo['signName'], ")")
                        print("bad file is ", infoJson)
                        print("bad username is ", jsonReadableInfo['userName'])
                        if jsonReadableInfo['userName'] == "":
                            print("no username")
                            print("is video is ", jsonReadableInfo["isVideo"])
                            print("may capture data is ", jsonReadableInfo["mayCaptureData"])
                        if jsonReadableInfo['userName'] == "Joshua Beckman":
                            signName = jsonReadableInfo['signName'].strip().lower()
                            addSign(jsonReadableInfo, signName, jsonReadableLandmarks, videoHandDic, imageHandDic)
                        if jsonReadableInfo["userName"] == "Kurt Metz":
                            print("is video is ", jsonReadableInfo["isVideo"])
                    else:
                        signName = jsonReadableInfo['signName']
                        signName = signName.lower()
                        addSign(jsonReadableInfo, signName, jsonReadableLandmarks, videoHandDic, imageHandDic)
            except BaseException as err:
                print("opening info file error",str(err))
    return imageHandDic, videoHandDic


def addSign(jsonReadableInfo, signName, jsonReadableLandmarks, videoHandDic, imageHandDic):
    try:
        if jsonReadableInfo['isVideo'] == True:
            addNewThing(signName, jsonReadableLandmarks, videoHandDic)
        else:
            addNewThing(signName, jsonReadableLandmarks, imageHandDic)
    except:
        thisIsAPlaceHolder = 0


def buildVideo1and2dics(videoHandDicNotRegularized, LEN_OF_ONE_HANDED_VECTOR):
    videoHandDic1 = {}
    videoHandDic2 = {}
    for key, value in videoHandDicNotRegularized.items():
        for video in value:
            newVideo = library.regularlizeVideo(video)
            if newVideo is not None:
                print("length", len(newVideo))
                if len(newVideo) == LEN_OF_ONE_HANDED_VECTOR:
                    addNewThing(key, newVideo, videoHandDic1)
                elif len(newVideo) == LEN_OF_ONE_HANDED_VECTOR*2:
                    addNewThing(key, newVideo, videoHandDic2)
                else:
                    print("this shouldn't happen")
    return videoHandDic1, videoHandDic2

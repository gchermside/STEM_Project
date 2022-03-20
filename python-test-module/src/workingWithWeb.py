import boto3
import passwords
import json
import functions
import os
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
import json
from sklearn.model_selection import train_test_split
from sklearn import tree
def toVectorandRegularize(image):
    vector = []
    if len(image) == 1:
        for unRegHand in image:
            hand = functions.regularizeJsonHand(unRegHand)
            for points in hand:
                vector.append(points["x"])
                vector.append(points["y"])
                vector.append(points["z"])
    return vector


def readPictureDic(dic):
    X = [] #data
    y = [] #targets
    for key, items in dic.items():
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
            vector = functions.vectorVideo(item)
            if vector == [] or y == "":
                print("dud, skipping")
            else:
                X.append(vector)
                y.append(key)
    return X, y

def machineLearning(X, y):
    XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size = .10)
    # print(f"length of training {len(XTrain)}")
    model = MLPClassifier(hidden_layer_sizes=(150,100,50), max_iter=2000,activation = 'relu',solver='adam',random_state=1) #change this line to test new models
    model.fit(XTrain, yTrain)
    prediction = model.predict(XTest)
    totalWrong = 0
    for i in range(0, len(yTest)):
        if prediction[i] != yTest[i]:
            totalWrong = totalWrong+1
        print(f"prediction {prediction[i]} is actually {yTest[i]}")
    print(f"percentage wrong: {totalWrong/len(yTest) * 100}")
    print(totalWrong)
    print(len(yTest))
    return totalWrong/len(yTest) * 100

# percentage wrong: 2.4285714285714284

client = boto3.client(
    's3',
    aws_access_key_id = str(passwords.AWSAccessKeyId),
    aws_secret_access_key = str(passwords.AWSSecretKey),
    region_name = 'us-east-1'
)

# Creating the high level object oriented interface


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
                        functions.addNewThing(signName, jsonReadableLandmarks, videoHandDic)
                    else:
                        functions.addNewThing(signName, jsonReadableLandmarks, imageHandDic)
                except:
                    thisIsAPlaceHolder = 0
    return imageHandDic, videoHandDic


imageHandDic, videoHandDicNotRegularized = readInData()
print(f"length of old dic {len(videoHandDicNotRegularized)}")
num = 0
for value in videoHandDicNotRegularized.values():
    for video in value:
        num += 1
print(f"num is {num}")
vorp = input("Do you want to test video or picture?(type v or p): ")
if vorp == "v":
    # training model for video
    print("ok")
    videoHandDic = {}
    for key, value in videoHandDicNotRegularized.items():
        for video in value:
            newVideo = functions.regularlizeVideo(video)
            if newVideo is not None:
                functions.addNewThing(key, newVideo, videoHandDic)
    # machine learning
    X, y = readVideoDic(videoHandDic)
    print(len(y))
    print(y)
    total = 0
    count = 0
    for i in range(0, 10):
        count = count+1
        total += machineLearning(X, y)
    print("overall average is ")
    print(total/count)
else:
    # training model on picture data
    X, y = readPictureDic(imageHandDic)
    print(len(X))
    print(len(y))
    total = 0
    count = 0
    for i in range(0, 40):
        count = count+1
        total += machineLearning(X, y)
    print("overall average is ")
    print(total/count)
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import json
from sklearn.model_selection import train_test_split

def sklearnDemo():
    model = RandomForestClassifier()
    data = [
        [ 1,  2,  3],  # 2 samples, 3 features
        [11, 12, 13]
    ]
    target = [0, 1]  # classes of each sample
    model.fit(data, target)
    prediction =model.predict([[2,2,4], [1,12,8]])
    print(prediction)


def machineLearning(X, y):
    XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size = .20)
    print(f"xTrain is {XTrain}")
    print(f"xTest is {XTest}")
    print(f"yTrain is {yTrain}")
    print(f"yTest is {yTest}")
    print(f"length of training {len(XTrain)}")
    model = RandomForestClassifier()
    model.fit(XTrain, yTrain)
    prediction =model.predict(XTest)
    print(prediction)
    print(yTest)
    for i in range(0, len(yTest)):
        print(f"prediction {prediction[i]} is acutally {yTest[i]}")

def readFile():
    with open("src/frames1Hand.json", "r") as file:
        jsonFile = json.load(file)
    y = []
    X = []
    for key, frames in jsonFile.items():
        for frame in frames:
            vector = frameJsonToVector(frame)
            if vector != None:
                X.append(vector)
                y.append(key)
            else:
                print("one bad value")
    return X,y

def frameJsonToVector(frameJson):
    handPoints = frameJson["hand1"]["landmarks"]
    assert len(handPoints) == 21
    vector = []
    if handPoints[0] != [0,0,0]:
        return None
    else:
        for point in handPoints:
            assert len(point) == 3
            for cordinate in point:
                vector.append(cordinate)
    return vector

X, y = readFile()
machineLearning(X, y)

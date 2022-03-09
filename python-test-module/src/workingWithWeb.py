import boto3
import passwords
import json
import functions
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
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


def readDic(dic):
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

def machineLearning(X, y):
    XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size = .30)
    print(f"xTrain is {XTrain}")
    print(f"xTest is {XTest}")
    print(f"yTrain is {yTrain}")
    print(f"yTest is {yTest}")
    print(f"length of training {len(XTrain)}")
    model = RandomForestClassifier() #change this line to test new models
    model.fit(XTrain, yTrain)
    prediction =model.predict(XTest)
    print(prediction)
    print(yTest)
    totalWrong = 0
    for i in range(0, len(yTest)):
        if prediction[i] != yTest[i]:
            totalWrong = totalWrong+1
        print(f"prediction {prediction[i]} is actually {yTest[i]}")
    print(f"percentage wrong: {totalWrong/len(yTest) * 100}")
    print(totalWrong)
    print(len(yTest))

# percentage wrong: 2.4285714285714284

client = boto3.client(
    's3',
    aws_access_key_id = str(passwords.AWSAccessKeyId),
    aws_secret_access_key = str(passwords.AWSSecretKey),
    region_name = 'us-east-1'
)

# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = str(passwords.AWSAccessKeyId),
    aws_secret_access_key = str(passwords.AWSSecretKey),
    region_name = 'us-east-1'
)


clientResponse = client.list_buckets()

# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')


# Print the data frame
my_bucket = resource.Bucket("asl-dictionary-uploads")
summaries = my_bucket.objects.all()
jsonFilesKeys = []
jsonLandmarkFiles = []
jsonInfoFiles = []
for file in summaries:
    if file.key.endswith("landmarks.json"):
        jsonFilesKeys.append(file.key)
        obj = client.get_object(
            Bucket = 'asl-dictionary-uploads',
            Key = file.key
        )
        jsonObj = json.load(obj['Body'])
        jsonLandmarkFiles.append(jsonObj)
    if file.key.endswith("info.json"):
        jsonFilesKeys.append(file.key)
        obj = client.get_object(
            Bucket = 'asl-dictionary-uploads',
            Key = file.key
        )
        jsonObj = json.load(obj['Body'])
        jsonInfoFiles.append(jsonObj)
imageHandDic = {}
videoHandDic = {}
oldHandDic = {}
for num in range(0, len(jsonInfoFiles)):
    try:
        if jsonInfoFiles[num]["isVideo"] == "true":
            functions.addNewThing(jsonInfoFiles[num]["signName"], jsonLandmarkFiles[num], videoHandDic)
        else:
            functions.addNewThing(jsonInfoFiles[num]["signName"], jsonLandmarkFiles[num], imageHandDic)
    except:
       functions.addNewThing(jsonInfoFiles[num]["signName"], jsonLandmarkFiles[num], oldHandDic)

X, y = readDic(imageHandDic)
print(len(X))
print(len(y))
machineLearning(X, y)

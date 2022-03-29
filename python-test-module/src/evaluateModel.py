from workingWithWeb import *

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
    print(y)
    total = 0
    count = 0
    model = None
    for i in range(0, 1):
        count = count+1
        totalPercent, model = machineLearning(X, y)
        total += totalPercent
    print("overall average is for videos is ")
    print(total/count)
else:
    # training model on picture data
    X, y = readPictureDic(imageHandDic)
    print(len(X))
    print(len(y))
    total = 0
    count = 0
    for i in range(0, 20):
        count = count+1
        totalPercent, model = machineLearning(X, y)
        total += totalPercent
    print("overall average for picture is ")
    print(total/count)
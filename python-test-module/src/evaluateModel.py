from workingWithWeb import *
import functions

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
    videoHandDic1 = {}
    videoHandDic2 = {}
    for key, value in videoHandDicNotRegularized.items():
        for video in value:
            newVideo = functions.regularlizeVideo(video)
            if newVideo is not None:
                if len(newVideo[0]) == 1:
                    functions.addNewThing(key, newVideo, videoHandDic1)
                elif len(newVideo[0]) == 2:
                    functions.addNewThing(key, newVideo, videoHandDic2)
                else:
                    print("this shouldn't happen")
    # machine learning
    X, y = readVideoDic(videoHandDic1)
    print(y)
    total = 0
    count = 0
    model = None
    for i in range(0, 5):
        count = count+1
        totalPercent, model = machineLearning(X, y)
        total += totalPercent
    print("overall average is for one handed videos is ")
    print(total/count)

    X, y = readVideoDic(videoHandDic2)
    print(y)
    total = 0
    count = 0
    model = None
    for i in range(0, 5):
        count = count+1
        totalPercent, model = machineLearning(X, y)
        total += totalPercent
    print("overall average for two handed videos is ")
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
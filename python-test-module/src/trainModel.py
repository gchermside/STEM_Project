from workingWithWeb import *

NUM_OF_FRAMES = 15
LEN_OF_ONE_HANDED_VECTOR = 990
imageHandDic, videoHandDicNotRegularized = readInData()
videoHandDic1, videoHandDic2 = buildVideo1and2dics(videoHandDicNotRegularized, LEN_OF_ONE_HANDED_VECTOR)
X, y = readVideoDic(videoHandDic2) #use imageHandDic, videoHandDic1, or videoHandDic2 #must either readPictureDic or readViceoDic
print("y train is", y)
model = trainModel(X, y)
print("model made")
saveModel(model, "video2") # change file name to picture video1, or video2


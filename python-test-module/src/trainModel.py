from workingWithWeb import *

NUM_OF_FRAMES = 15
LEN_OF_ONE_HANDED_VECTOR = 990
imageHandDic, videoHandDicNotRegularized = readInData()
videoHandDic1, videoHandDic2 = buildVideo1and2dics(videoHandDicNotRegularized, LEN_OF_ONE_HANDED_VECTOR)
X, y = readVideoDic(videoHandDic2) #use imageHandDic, videoHandDic1, or videoHandDic2
print("X train is", X)
model = trainModel(X, y)
saveModel(model, "video2") # change file name


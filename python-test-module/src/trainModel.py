from workingWithWeb import *


imageHandDic, videoHandDicNotRegularized = readInData()
X, y = readPictureDic(imageHandDic)
model = trainModel(X, y)
saveModel(model, "picture")


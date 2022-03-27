from workingWithWeb import *

directory = "C:/Users/Genevieve/Documents/programming/STEM_Project/s3Data/uploads/"
subDir = "2022-03-08T01_25_34.288Z-977039"
landmarks = readLandmark(directory, subDir)
vector = toVectorandRegularize(landmarks)
if vector == []:
    print("dud")


model = loadModel("picture")
prediction = model.predict([vector])
print(prediction)

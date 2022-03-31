from workingWithWeb import *

directory = "C:/Users/Genevieve/Documents/programming/STEM_Project/uploads"
subDir = "2022-03-27T02_29_44.607Z-4963915"
landmarks = readLandmark(directory, subDir)
vector = toVectorandRegularize(landmarks)
print(vector)
if vector == []:
    print("dud")


model = loadModel("picture")
prediction = model.predict([vector])
print(prediction)

# C:\Users\Genevieve\Documents\programming\STEM_Project\uploads\2022-03-27T02_15_21.496Z-5392117
# C:/Users/Genevieve/Documents/programming/STEM_Project/s3Data/uploads/2022-03-27T02_15_21.496Z-5392117/landmarks.json

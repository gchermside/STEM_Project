from workingWithWeb import *


def readInData():
    imageDic = {}
    videoDic = {}
    directory = "C:/Users/Genevieve/Documents/programming/STEM_Project/s3Data/uploads/"
    entries = os.listdir(directory)
    for subDir in entries:
        landmarksJson = directory+"/"+subDir+"/landmarks.json"
        infoJson = directory+"/"+subDir+"/info.json"
        with open(landmarksJson, 'r') as landmarkFile:
            jsonReadableLandmarks = json.load(landmarkFile)
            try:
                with open(infoJson, "r") as infoFile:
                    jsonReadableInfo = json.load(infoFile)
                    if "  " in jsonReadableInfo['signName']:
                        print("bad name is ", jsonReadableInfo['signName'], ")")
                        print("bad file is ", infoJson)
                        print("bad username is ", jsonReadableInfo['userName'])
                        if jsonReadableInfo['userName'] == "":
                            print("no username")
                            print("is video is ", jsonReadableInfo["isVideo"])
                            print("may capture data is ", jsonReadableInfo["mayCaptureData"])
                        if jsonReadableInfo['userName'] == "Joshua Beckman":
                            signName = jsonReadableInfo['signName'].strip().lower()
                            # addSign(jsonReadableInfo, signName, jsonReadableLandmarks, videoHandDic, imageHandDic)
                        if jsonReadableInfo["userName"] == "Kurt Metz":
                            print("is video is ", jsonReadableInfo["isVideo"])
                    else:
                        signName = jsonReadableInfo['signName'].strip().lower()
                        try:
                            if jsonReadableInfo['isVideo'] is True:
                                videoUrl = subDir+"/video.webm"
                                addNewThing(signName, videoUrl, videoDic)
                            else:
                                pictureUrl = subDir+"/picture.jpeg"
                                addNewThing(signName, pictureUrl, imageDic)
                        except BaseException as err:
                            print("no picture/video or old data",str(err))
            except BaseException as err:
                print("opening info file error",str(err))
    return imageDic, videoDic




imageDic, videoDic = readInData()
print(json.dumps(imageDic))
print(json.dumps(videoDic))
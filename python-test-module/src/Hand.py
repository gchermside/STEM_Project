import json

def fromJson(json):
    if json == 0:
        return None
    return Hand(json["isRightHand"], json["landmarks"], json["world_landmarks"])

class Hand:
    def __init__(self, isRightHand, landmarks, world_landmarks):
        self.isRightHand = isRightHand
        self.landmarks = landmarks
        self.world_landmarks = world_landmarks

    def toJson(self):
        return {
            "isRightHand": self.isRightHand,
            "landmarks": self.landmarks,
            "world_landmarks": self.world_landmarks,
        }
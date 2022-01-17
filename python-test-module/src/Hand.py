import json

class Hand:
    def __init__(self, isRightHand, landmarks, world_landmarks):
        self.isRightHand = isRightHand
        self. landmarks = landmarks
        self.world_landmarks = world_landmarks

    def toJSON(self):
        return json.dumps(self,  default=lambda o: o.__dict__, indent=2)


import Hand

def fromJson(json):
    if json["pose"] == 0:
        return Frame(Hand.fromJson(json["hand1"]), Hand.fromJson(json["hand2"]), None)
    return Frame(Hand.fromJson(json["hand1"]), Hand.fromJson(json["hand2"]), None) #FIXME: pose doesn't work

class Frame:
    def __init__(self, hand1, hand2, pose):
        self.hand1 = hand1
        self.hand2 = hand2
        self.pose = pose


    def toJson(self):
        if(self.hand2 == None):
            if self.pose == None:
                return {
                    "hand1": self.hand1.toJson(),
                    "hand2": 0,
                    "pose": 0,
                }
            else:
                return {
                    "hand1": self.hand1.toJson(),
                    "hand2": 0,
                    "pose": -1, ##FIXME: should break code
                }
        else:
            if self.pose == None:
                return {
                    "hand1": self.hand1.toJson(),
                    "hand2": self.hand2.toJson(),
                    "pose": 0,
                }
            else:
                return {
                    "hand1": self.hand1.toJson(),
                    "hand2": self.hand2.toJson(),
                    "pose": -1, #FIXME: should break code
                }



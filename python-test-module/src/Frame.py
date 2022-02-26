import Hand
import Pose


def fromJson(json):
    if json["pose"] == 0:
        return Frame(Hand.fromJson(json["hand1"]), Hand.fromJson(json["hand2"]), None)
    else:
        print(Pose.fromJson(json["pose"]))
        return Frame(Hand.fromJson(json["hand1"]), Hand.fromJson(json["hand2"]), Pose.fromJson(json["pose"]))

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
                    "pose": self.pose.toJson(),
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
                    "pose": self.pose.toJson(),
                }


class videoFrame(Frame):
    def __init__(self, hand1, hand2, pose, movement):
        self.movement = movement
        # invoking the __init__ of the parent class
        Frame.__init__(self, hand1, hand2, pose)

def fromJson(self, points):
    return Pose(points)

class Pose:
    def __init__(self, points):
        landmarks = points

    def toJson(self):
        return self.landmarks

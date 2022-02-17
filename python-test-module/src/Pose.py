def fromJson(points):
    return Pose(points)

class Pose:
    def __init__(self, points):
        self.landmarks = points

    def toJson(self):
        return self.landmarks
class Point():
    x , y, z = 0, 0, 0
    def print_point(self):
        return 'X' + str(round(self.x,4)) + 'Y' + str(round(self.y,4)) \
                + 'Z' + str(round(self.z,4))






point = Point()
print(point.__dict__)
point.x = -0.32932
point.y = 8.34
point.z = 23323.0232
print(point.__dict__)
point.a = 0.3
print(point.print_point())
print(point.a)
print(point.__dict__)

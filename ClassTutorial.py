
# Create Point and Rectangle Classes


class Point:
    pass


class Rectangle:
    pass


# Create Point object/instance with name 'blank'
blank = Point()
# blank contains point attributes for x and y coordinates
blank.x = 3.0
blank.y = 4.0
# Create rectangle object/instance with width and height attributes
box = Rectangle()
box.width = 100.0
box.height = 200.0
# Embed box object with a point object titled 'box.corner'
box.corner = Point()
box.corner.x = 0.0
box.corner.y = 0.0
# function returns a point object with Center attributes


def findCenter(box):
    p = Point()
    p.x = box.corner.x + box.width/2.0
    p.y = box.corner.y - box.height/2.0
    return p

# prints point object attributes


def printPoint(p):
    print(str(p.x) + ',' + str(p.y))

# alter box dimensions


def growRect(box, dwidth, dheight):
    box.width += dwidth
    box.height += dheight


# Create center variable that contains findCenter object
center = findCenter(box)
# Print x and y attribute values
printPoint(center)

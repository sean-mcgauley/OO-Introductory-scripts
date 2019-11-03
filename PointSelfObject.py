class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    # Displays a string version of object if an operation requires a string

    def __str__(self):
        return f'({self.x}, {self.y})'
    # Adds two point objects together

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    # if left operand is a point uses __mul__
    # computes dot product

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
    # if left operand is primitive type and right is a point uses __rmul__
    # Performs scalar multiplication

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y)
    # if left operand is a point but right is not this will fail
    # See Appendix B for further discussion

    def multadd(x, y, z):
        return x * y + z
    # Define reverse function for Point class

    def reverse(self):
        self.x, self.y = self.y, self.x
    # Invoke reverse on Point class through frontAndBack
    # def frontAndBack(self):
     #   import copy
      #  back = copy.copy(self)
       # back.reverse()
        #print (str(self) + str(back))
# Can create function for specific class only as above or for all types as below


def frontAndBack(front):
    import copy
    back = copy.copy(front)
    back.reverse()
    print(str(front) + str(back))

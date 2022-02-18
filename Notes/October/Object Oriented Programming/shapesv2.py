"""
Daniel Xu
Object Oriented Programming - Shapes Class #2
October 22nd, 2021
Professor Park
"""

import math

class Shape:
    kind = 'shape' # a CLASS attribute
    num = 0
    
    def __init__(self, name):
        """ Object constructor for the Shape class """
        self.name = name   # Object instance attributes
        self.xpos = 0
        self.ypos = 0
        
        Shape.num += 1
    
    def get_position(self):
        """ Return the (x, y) position of the object"""
        """ "get_position" is called an accessor, you can present the 
            illusion that the object still has a position, while still being
            allowed to change the framework of the object """
        return (self.xpos, self.ypos)
    
    def move_by(self, dx, dy):
        """ Move the location of the shape by some delta """
        """ move_by is called a mutator """
        self.xpos += dx
        self.ypos += dy
    
    def __repr__(self):
        """ Output a human_readable description of the shape """
        return self.name + "(" + self.kind +") @ " + str(self.get_position())
        
class Circle(Shape):
    
    kind = 'circle'
    num = 0
    
    def __init__(self, name, radius):
        
        super().__init__(name)
        self.radius = radius
        Circle.num += 1
    
    def area(self):
        return math.pi * self.radius **2
    
    def circumference(self):
        return 2 * math.pi * self.radius
    
    
    def __repr__(self):
        return super().__repr__() + ' with radius = ' + str(self.radius)
    
    def __eq__(self, other):
        return self.radius == other.radius and \
               self.get_position() == other.get_position()
               
    
class ResizableCircle(Circle):
    
    kind = "resizable circle"
    num = 0
    
    def __init__(self, name, radius):
        super().__init__(name,radius) #I'm a circle !
        ResizableCircle.num += 1
        
    def set_radius(self, radius):
        """ Set the radius of the circle """
        self.radius = radius


def main():
    blob = Shape('Blob')
    print(blob)
    
    blob.move_by(1,2)
    blob.move_by(2, 3)
    print(blob)
    
    c = Circle('Circle of life', 10)
    rc = ResizableCircle('Mr.Circle', 10)
    
    print('\n\nDrawing Pad Status:')
    shapes = [blob, c, rc]
    for shape in shapes:
        print(shape)
    
    print('\n\ntype of shapes:')
    for shape_class in [Shape, ResizableCircle, Circle]:
        print(shape_class.kind+'s', shape_class.num)
                
main()
        
        
        
        
        
        
        
        
        
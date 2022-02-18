"""
Daniel Xu
Object Oriented Programming - Shapes Class
October 22nd, 2021
Professor Park
"""

import math

class Shape:
    def __init__(self):
        """ Object constructor fot the Shape class. Putting a double underscore
            before an attribute will sort of lock the attribute and prevent you
            from changing it """
        self.xpos = 0
        self.ypos = 0
        
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
    
    def move_to(self, new_xpos, new_ypos):
        self.xpos = new_xpos
        self.ypos = new_ypos
        

class Circle(Shape):
    def __init__(self, radius):
         
        #Instantiate the 'parent class: I am a named shape!
        #This takes the attributes which were defined in the parent class
        #and adds them to the subclass' attributes
        super().__init__()
        
        #Customize myself: I am a particular kind of shape!
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius **2
    
    def circumference(self):
        return 2 * math.pi * self.radius
    
class Square(Shape):
    def __init__(self, side):
        
        super().__init__()
        self.side = side
    
    def area(self):
        return self.side ** 2




def main():
    my_shape = Shape()
    curr_x = my_shape.xpos
    curr_y = my_shape.ypos
    curr_x, curr_y = my_shape.get_position()
    print(curr_x, curr_y)
    
main()
    
    

        
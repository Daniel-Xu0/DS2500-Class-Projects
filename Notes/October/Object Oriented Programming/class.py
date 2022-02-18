"""
Daniel Xu
Object Oriented Programming - Classes
October 22nd, 2021
Professor Park
"""

class Test:
    def __init__(self, val1, diameter, name_core):
        self.attribute1 = val1
        self.circumference = diameter * 3.14
        self.obj_name = 'Val:' + name_core+ '<END>'
        
    def increment_by(self, delta):
        self.attribute1 +=  delta
    
    def __str__(self):
        return "Object of type Test: " + self.obj_name
    
    def __repr__(self):
        return "Object of type Test: " + self.obj_name
        
def main():
    my_var = Test(17, 3.5, "circle1")
    print(my_var.attribute1)
    print(my_var.circumference)
    print(my_var.obj_name)
    print(my_var.attribute1 + my_var.circumference)
    my_var.increment_by(10)
    print(my_var.attribute1)
    
    foo = Test(69, 69, "sixty-nine")
    foo.increment_by(47)
    
main()
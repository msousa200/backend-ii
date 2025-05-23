from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Calculate the area of the shape"""
        pass
    
    @abstractmethod
    def draw(self):
        """Return a string representation of drawing the shape"""
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius * self.radius
    
    def draw(self):
        return f"Drawing a circle with radius {self.radius}"

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side * self.side
    
    def draw(self):
        return f"Drawing a square with side {self.side}"

def shape_factory(shape_type, **kwargs):
    """Factory function to create shape objects
    
    Args:
        shape_type: String indicating which shape to create
        **kwargs: Parameters needed for the specific shape
    
    Returns:
        A shape object instance
    """
    shape_type = shape_type.lower()
    
    if shape_type == "circle":
        return Circle(kwargs.get("radius", 0))
    elif shape_type == "square":
        return Square(kwargs.get("side", 0))
    else:
        raise ValueError(f"Unknown shape type: {shape_type}")

if __name__ == "__main__":
    circle = shape_factory("circle", radius=5)
    print(circle.draw())
    print(f"Circle area: {circle.area()}")
    
    square = shape_factory("square", side=4)
    print(square.draw())
    print(f"Square area: {square.area()}")
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        """Method to be called when the observed subject changes state"""
        pass

class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        """Add an observer to the notification list"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Remove an observer from the notification list"""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self):
        """Notify all observers of state change"""
        for observer in self._observers:
            observer.update(self)

class Shape(ABC, Subject):
    def __init__(self):
        Subject.__init__(self)
    
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
        super().__init__()
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value
        self.notify()  
    
    def area(self):
        return 3.14159 * self._radius * self._radius
    
    def draw(self):
        return f"Drawing a circle with radius {self._radius}"

class Square(Shape):
    def __init__(self, side):
        super().__init__()
        self._side = side
    
    @property
    def side(self):
        return self._side
    
    @side.setter
    def side(self, value):
        self._side = value
        self.notify()
    
    def area(self):
        return self._side * self._side
    
    def draw(self):
        return f"Drawing a square with side {self._side}"

class AreaObserver(Observer):
    def update(self, subject):
        print(f"Area updated: {subject.area()}")

class DrawingObserver(Observer):
    def update(self, subject):
        print(f"Drawing updated: {subject.draw()}")

def shape_factory(shape_type, **kwargs):
    """Factory function to create shape objects"""
    shape_type = shape_type.lower()
    
    if shape_type == "circle":
        return Circle(kwargs.get("radius", 0))
    elif shape_type == "square":
        return Square(kwargs.get("side", 0))
    else:
        raise ValueError(f"Unknown shape type: {shape_type}")

if __name__ == "__main__":
    circle = shape_factory("circle", radius=5)
    
    area_observer = AreaObserver()
    drawing_observer = DrawingObserver()
    
    circle.attach(area_observer)
    circle.attach(drawing_observer)
    
    print("Changing circle radius to 10:")
    circle.radius = 10
    
    square = shape_factory("square", side=4)
    square.attach(area_observer)
    square.attach(drawing_observer)
    
    print("\nChanging square side to 6:")
    square.side = 6
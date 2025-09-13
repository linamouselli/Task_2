#Task 2
# Part1: SOLID
# SRP - Single Responsibility


class Report:
    def __init__(self, data):
        self.data = data

    def build_text(self) -> str:
        text = "\n".join(self.data)
        return text

class FileSave:
    @staticmethod
    def save_text(file_name: str, content: str) -> None:
        with open(file_name, "w") as f:
            f.write(content)

builder = Report(data=["A", "B", "C"])
my_text = builder.build_text()
FileSave.save_text("report.txt", my_text)

#------------------------------------------------------------------------------

#OCP - Open/Closed
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * (self.radius ** 2)

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height

my_circle = Circle(radius=10)
print(f"Circle Area {my_circle.area()}")
my_square = Square(side=10)
print(f"Square Area {my_square.area()}")
my_rectangle = Rectangle(width=8, height=5)
print(f"Rectangle Area {my_rectangle.area()}")
print("-----------------------------------------------------------")
#------------------------------------------------------------------------------

# LSP - Liskov Substitution

class Bird:
    def __init__(self, name):
        self.name = name

class CanFly(Bird):
    @staticmethod
    def fly():
        print("Flying")

class CantFly(Bird):
    pass

class Ostrich(CantFly):
    pass


#------------------------------------------------------------------------------

# ٍISP - Interface Segregation

class Worker:
    def __init__(self, name):
        self.name = name

class CanWork(Worker):
    def work(self):
        print(f"I am {self.name} and I can work")

class CanEat(Worker):
    def eat(self):
        print(f"I am {self.name} and I can eat")

robot = CanWork("Focal_Robot")
robot.work()
print("-----------------------------------------------------------")

#------------------------------------------------------------------------------

# DIP - Dependency Inversion

class Database(ABC):
    @abstractmethod
    def fetch(self):
        pass

class MySQLDB(Database):
    def fetch(self):
        return "Get data from MySQL Database"

class MemoryDB(Database):
    def fetch(self):
        return "Get data from MemoryDB Database"

class Service:
    def __init__(self, database: Database):
        self.database = database

    def get_data(self):
        return self.database.fetch()

my_sql_db = Service(MySQLDB())
print(my_sql_db.get_data())

memory_db = Service(MemoryDB())
print(memory_db.get_data())

print("-----------------------------------------------------------")

#------------------------------------------------------------------------------
# Part2: Design Patterns
# 1- Strategy Pattern

class PaymentStrategy:
    def __init__(self, amount):
        self.amount = amount

    def apply_discount(self, amount):
        pass

class PayFull(PaymentStrategy):
    def apply_discount(self, amount):
        return f"Pay Full: {amount}"

class PayPercentDiscount(PaymentStrategy):
    def __init__(self, amount, percentage):
        super().__init__(amount)
        self.percentage = percentage
    def apply_discount(self, amount):
        return f"Pay with Percent Discount: {amount - (amount * self.percentage / 100)}"

class PayFixedDiscount(PaymentStrategy):
    def __init__(self, amount, fixed_amount):
        super().__init__(amount)
        self.fixed_amount = fixed_amount
    def apply_discount(self, amount):
        return f"Pay with Fixed Discount: {max(0, amount - self.fixed_amount)}"

class PaymentProcess:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def payment(self, amount):
        return self.strategy.apply_discount(amount)

process = PaymentProcess(PayFull(1000))
print(process.payment(1000))
process = PaymentProcess(PayPercentDiscount(1000, 10))
print(process.payment(1000))
process = PaymentProcess(PayFixedDiscount(1000, 20))
print(process.payment(1000))

print("-----------------------------------------------------------")

#------------------------------------------------------------------------------

# 2- Observer Pattern

class Subject:
    def __init__(self):
        self._observers = []
        self._state = None

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        self.notify_observers()

class Observer:
    def __init__(self, name):
        self.name = name

    def update(self, state):
        pass

class EmailObserver(Observer):

    def update(self, state):
        print(f"I am the observer {self.name} and I received an email that the state has been updated to {state} [EMAIL]")

class SMSObserver(Observer):

    def update(self, state):
        print(f"I am the observer {self.name} and the received a SMS that the state has been updated to {state} [SMS]")

subject = Subject()
observer1 = EmailObserver("Email Obs")
observer2 = SMSObserver("SMS Obs")

subject.add_observer(observer1)
subject.add_observer(observer2)

subject.set_state('Ready')

print("-----------------------------------------------------------")


#------------------------------------------------------------------------------

# 3 - Factory Pattern

class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        print("Woof!")

class Cat(Animal):
    def speak(self):
        print("Meow!")

class AnimalFactory:
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            return "Unknown Animal"


my_dog = AnimalFactory.create_animal(animal_type = "dog")
my_dog.speak()


print("-----------------------------------------------------------")


#------------------------------------------------------------------------------

# 4 - Adapter Pattern

class OldPrinter:
    def print_text(self, msg):
        print(f"Old Printer: {msg}")

class NewPrinter:

    def print_text(self, msg, style):
        print(f"New Printer: {msg}, {style}")

class AdapterPrinter:
    def __init__(self, printer, style=None):
        self.printer = printer
        self.style = style

    def print_msg(self, msg):
        if isinstance(self.printer, OldPrinter):
            return self.printer.print_text(msg)
        elif isinstance(self.printer, NewPrinter):
            return self.printer.print_text(msg, self.style)
        else:
            return "not supported"

old = OldPrinter()
new = NewPrinter()
adapter1 = AdapterPrinter(old)
adapter2 = AdapterPrinter(new, "A4")
adapter1.print_msg("Hello from OldPrinter")
adapter2.print_msg("Hello from NewPrinter")

print("-----------------------------------------------------------")

#------------------------------------------------------------------------------

# 5 - Singleton Pattern

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Logger()
b = Logger()

print(a is b)
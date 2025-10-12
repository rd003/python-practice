class Student:
    def __init__(self):
        self.name=None
        self.age = None

    def print_details(self):
        print(f"Name: {self.name}, Age: {self.age}")


stu = Student()
stu.name="Jon"
stu.age = 20
stu.print_details()

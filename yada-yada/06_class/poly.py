class Animal:
    def __init__(self,name):
        self.name=name

class Dog(Animal):
    def __init__(self,name,breed):
        super().__init__(name)
        self.breed=breed

d = Dog("Bhadru","Kotdwari")
print(f"{d.name} {d.breed}")
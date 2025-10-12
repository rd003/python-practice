class Animal:
    def speak(self):
        print("Animalspeaks")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

dog = Dog()
dog.speak()
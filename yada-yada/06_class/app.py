class Car:
    def __init__(self,brand,model):
        self.brand = brand
        self.model = model

    def drive(self):
        print(f"{self.brand} {self.model} is driving")    


def main():
   my_car = Car("Tesla","Model 3")
   my_car.drive()
   
if __name__ == "__main__":
    main()
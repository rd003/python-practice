# specific error

# try:
#     print(10* (1/0))
# except ZeroDivisionError:
#     print("Divide by zero error")    

# Generic error

# try:
#     print(10* (1/0))
# except Exception as e:
#     print(e.args) 
#     print(type(e))
#     print(e) 

# Raise exception

# def greeting(name=None):
#     if name is None:
#         raise ValueError("Missing argument : 'name'")
#     print(f"Hello {name}!")

# if __name__ == "__main__":
#     greeting()

# Generic exception

def greeting(name=None):
    if name is None:
        raise Exception("Missing argument : 'name'")
    print(f"Hello {name}!")

if __name__ == "__main__":
    greeting()
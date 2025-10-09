import json
import uuid 

FILE_PATH = "./04_crud_with_json_file/person.json"    

def load_data(): 
    try:
        with open(FILE_PATH,"r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []    

def save_data(person_list):
    try:
        with open(FILE_PATH,"w") as f:
            json.dump(person_list,f,indent=4)
            return True        
    except (IOError,OSError) as e:
        print(f"Error saving data: Unable to write to file - {e}")
        return False
    except TypeError as e:
        print(f"Error saving data: Cannot serialize data - {e}")
        return False
    
def insert():
    person_list= load_data()

    print("Please provide following details:")
    name = input("name: ")
    age = int(input("age: "))
    person = {"id":str(uuid.uuid4()),"name":name,"age":age}

    person_list.append(person)    
    save_data(person_list)
    print("\nData is added")    

def delete():
    person_list = load_data() 
    if not person_list:
        print('No data is available')
        return
    person_id = input('Enter person id to delete:')
    # if person list does not contain person id print message
    for index,person in enumerate(person_list):
        if person["id"] == person_id:
            delete_person = person_list.pop(index)
            save_data(person_list)
            print("person is deleted")
            break  
    else:
        print("Invalid person id")

def get_all():
    print(load_data())

def main():
    while True:
        choice = input("""
            1. Insert
            2. Delete
            3. Get all
            4. Exit

            Enter your choice:                                     
            """)
        
        match choice:
            case '1':
                insert()
            case '2':
                delete()
            case '3':
                get_all()
            case '4':
                break
            case _:
                print('Enter valid choice.')

if __name__ == "__main__":
    main()                                   
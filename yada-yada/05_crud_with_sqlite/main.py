import sqlite3

conn = sqlite3.connect("./05_crud_with_sqlite/person.db")
cur = conn.cursor()
cur.row_factory = sqlite3.Row  # Add this line

def initialize_db():
    cur.execute("""
      CREATE TABLE IF NOT EXISTS people(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INT
        )
    """)

def add_person():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    sql = """
          insert into people(name,age)
          values (?,?)
          """;  
    cur.execute(sql,(name,age)) 
    conn.commit()
    print("Successfully added a record") 

def get_people():
    sql = "select id,name,age from people"
    result = cur.execute(sql)
    people = result.fetchall()
    for person in people:
        print(f"id: {person['id']}, Name: {person['name']}, age: {person['age']}")

def delete_person():
    person_id = int(input("Enter the id to delete: "))
    sql = "delete from people where id=?"
    cur.execute(sql,(person_id,))
    print("Record is deleted")

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
           case "1":
                add_person()
           case "2":
                delete_person()
           case "3":
                get_people()
           case "4":
                break
           case _:
                print("Please select a valid choice")                

if __name__ == "__main__":
    initialize_db()
    main()
    conn.close()

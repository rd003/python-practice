import requests 

api_url = 'https://jsonplaceholder.typicode.com/todos'

def get_todo(id):
    response = requests.get(f'{api_url}/{id}')
    print(response.status_code)
    print(response.text)
    print(response.json())

def add_todo():
    todo = {
            "userId": 1,
            "title": "hahaha",
            "completed": False
          }
    response = requests.post(api_url,json=todo)
    print(response.json())


if __name__ == "__main__":
    # get_todo(1)    
    add_todo()
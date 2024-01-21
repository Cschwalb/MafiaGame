import requests
from bs4 import BeautifulSoup

global usn
global pw
global csrf_token
global login_url
usn = ""
pw = ""
csrf_token = ""
login_url = ""

def populateGlobalVariables():
    with open('data.txt', 'r') as f:
        data = f.read()
    f.close()
    lines = data.splitlines()
    for line in lines:
        words = line.split()
        usn = words[0]
        pw = words[1]
    login_url = 'https://toughsociety.com'


def getusn():
    with open('data.txt', 'r') as f:
        data = f.read()
    f.close()
    lines = data.splitlines()
    for line in lines:
        words = line.split()
        return words[0]


def getpw():
    with open('data.txt', 'r') as f:
        data = f.read()
    f.close()
    lines = data.splitlines()
    for line in lines:
        words = line.split()
        return words[1]

def login():
    login_url = 'https://toughsociety.com'
    session = requests.Session()
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
    print(usn)
    print(pw)
    login_data ={
        'LoginUsername': getusn(),
        'LoginPassword': getpw(),
        '__RequestVerificationToken': str(csrf_token)
    }
    login_response = session.post(login_url, login_data)
    print(login_response.status_code)
    print(login_response.text)
    if 'Updated every minute' in login_response.text:
        print('Login successful')
    else:
        print('login failed')
    session.close()


login()

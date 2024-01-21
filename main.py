import requests
from bs4 import BeautifulSoup

usn = ""
pw = ""
csrf_token = ''


def populateGlobalVariables():
    with open('data.txt', 'r') as f:
        data = f.read()
    lines = data.splitlines()
    info = []
    for line in lines:
        words = line.split()
        usn = words[0]
        pw = words[1]


def login():
    with requests.session() as session:
        page = session.get('http://toughsociety.com/')
        html = BeautifulSoup(page.content, 'html.parser')
        csrf_token = html.find('input', {'name' : '__RequestVerificationToken'})['value']
        print(csrf_token)
        data_to_login = {'LoginUsername': usn, 'LoginPassword': pw, '__RequestVerificationToken' : csrf_token}
        r = requests.post('http://toughsociety.com/', data_to_login)
        print(r.text)

populateGlobalVariables()
login()

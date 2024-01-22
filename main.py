import requests
from bs4 import BeautifulSoup
import time

usn = ""
pw = ""
csrf_token = ""
login_url = ""

def populateGlobalVariables():
    global usn, pw, login_url
    with open('data.txt', 'r') as f:
        data = f.read()
    lines = data.splitlines()
    if lines and len(lines[0].split()) == 2:
        usn, pw = lines[0].split()
    else:
        raise ValueError("data.txt does not contain the expected format.")
    login_url = 'https://toughsociety.com'


def login():
    try:
        populateGlobalVariables()
        session = requests.Session()
        response = session.get(login_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        login_data = {
            'LoginUsername': usn,
            'LoginPassword': pw,
            '__RequestVerificationToken': str(csrf_token)
        }
        login_response = session.post(login_url, login_data)
        print(login_response.status_code)
        if 'Updated every minute' in login_response.text:
            print('Login successful')
            return session  # Return the session if login is successful
        else:
            print('Login failed')
            return None  # Return None if login fails
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None in case of exception

def jailbreakthetesla():
    session = login()
    if not session:
        print("Login Failed.  Exiting.")
        return
    jail_url = 'https://www.toughsociety.com/rank/jail'
    response = session.get(jail_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and select the radio button
    radio_button = soup.find('input', {'id': 'j756354'})
    print(radio_button.text)
    if radio_button:
        # Prepare the data for submission
        form_data = {'j756354': radio_button['value']}

        retry_count = 0
        while True:
            retry_count += 1

            # Submit the form
            response = session.post(jail_url, data=form_data)
            if "from jail!" in response.text:
                print(f"Successful on attempt #{retry_count}")
                break
            else:
                print("Unsuccessful, retrying...")
                # Find the countdown element and wait
                countdown_element = soup.find('td', {'data-countdown': True})
                countdown = int(countdown_element['data-countdown']) if countdown_element else 30
                print(countdown)
                time.sleep(countdown)

    # Additional processing based on response
    # ...


if __name__ == "__main__":
    jailbreakthetesla()

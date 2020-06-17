import requests
from datetime import datetime
from random import randint, uniform, choices
import string
from time import sleep

base_url = "http://192.168.0.52:5000/"

def create_random_data():
    if randint(0, 1) == 0:
        # whether a user within range decided to use sanitiser
        ignored = False
    else:
        ignored = True

    data = {
        "location": random_string(10),
        "distance": uniform(0, 2),
        "volume_dispensed": 1.0,
        "ignored": ignored,
        "datetime": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    }

    return data

# creates a random sequence of digits and letters up to N length
def random_string(N):
    s = ''.join(choices(string.ascii_uppercase + string.digits, k=N))
    return s


# sends data to server to be saved on mysql database
def send_data():
    data = create_random_data()

    response = requests.post(base_url + "dispenser", json=data)
    print(response.text)

def main():
    # continuously send data to simulate a high volume scenario
    while True:
        send_data()
        sleep(0.5)

if __name__ == "__main__":
    main()
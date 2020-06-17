import requests
from datetime import datetime as dt
from random import randint, uniform, choices
import string
from time import sleep
import json

base_url = "http://localhost:5000/"

# device config vars
device_id = None
name = ""
location = ""

try:
    # load config file
    with open ("./config.json", "r") as config:
        # load json file as dictionary
        config = json.load(config)

        # update device variables
        device_id = config["device_id"]
        name = config["name"]
        location = config["location"]

        print("config succesfully applied")

except FileNotFoundError:
    print("File config.json not found")

if not location:
    location = input("Enter location for Dispenser: ")

# update config.json and variables
def update_config(config, convert=True):
    if convert:
        # convert from json to dictionary
        config = json.loads(config)

    # save config.json file
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def apply_config():
    try:
        # load config file
        with open ("./config.json", "r") as config:
            # load json file as dictionary
            config = json.load(config)

            # update device variables
            update_config(config, convert=False)
            print("config succesfully applied")

    except FileNotFoundError:
        print("File config.json not found")

def register_dispenser():
    #location = input("Enter location for Dispenser: ")
    created = dt.now().strftime("%d/%m/%Y, %H:%M:%S")

    data = {
        "device_id": device_id,
        "name": name,
        "location": location,
        "created": dt.now().strftime("%d/%m/%Y, %H:%M:%S")
        }

    response = requests.post(base_url + "dispenser/register", json=data)

    print(response.text)
    print(response.status_code)

    if response.status_code == 201:
        update_config(response.text)
        print("config succesfully updated")

def create_random_data():
    if randint(0, 1) == 0:
        # whether a user within range decided to use sanitiser
        ignored = False
    else:
        ignored = True

    data = {
        "device_id": device_id,
        "distance": uniform(0, 2),
        "volume_dispensed": 1.0,
        "fluid_level": 669.0,
        "ignored": ignored,
        "datetime": dt.now().strftime("%d/%m/%Y, %H:%M:%S")
    }

    return data

# creates a random sequence of digits and letters up to N length
def random_string(N):
    s = ''.join(choices(string.ascii_uppercase + string.digits, k=N))
    return s

# sends data to server to be saved on database
def send_data():
    data = create_random_data()

    response = requests.post(base_url + "dispenser", json=data)
    print(response.text)

def main():
    # apply configuration settings
    #apply_config()

    # register
    register_dispenser()

    # continuously send data to simulate a high volume scenario
    while True:
        send_data()
        sleep(1.0)

if __name__ == "__main__":
    main()
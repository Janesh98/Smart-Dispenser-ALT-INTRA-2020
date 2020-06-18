import requests
from datetime import datetime as dt
from random import randint, uniform, choices
import string
from time import sleep
import json

class Client:
    def __init__(self, base_url):

        self.base_url = base_url

        # device config vars
        self.device_id = None
        self.name = ""
        self.location = ""
        self.created = ""

        self.fluid_capacity = 1000.0
        self.fluid_dispense_volume = 1.0
        self.fluid_level = self.fluid_capacity

    # update config.json and variables
    def update_config(self, config):
        # convert from json to dictionary
        config = json.loads(config)

        # update device config variables
        self.update_vars(config)

        # save config.json file
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

    def update_vars(self, config):
        self.device_id = config["device_id"]
        self.name = config["name"]
        self.location = config["location"]
        self.created = config["created"]

    def apply_config(self):
        try:
            # load config file
            with open ("./config.json", "r") as config:
                # load json file as dictionary
                config = json.load(config)

                self.update_vars(config)

                # ask user for location
                if not self.location:
                    self.location = input("Enter location for Dispenser: ")

                print("config succesfully applied")

        except FileNotFoundError:
            print("File config.json not found")

    def register_dispenser(self):
        data = {
            "device_id": self.device_id,
            "name": self.name,
            "location": self.location,
            "created": dt.now().strftime("%d/%m/%Y, %H:%M:%S")
            }

        response = requests.post(self.base_url + "dispenser/register", json=data)

        print(response.text)
        print(response.status_code)

        if response.status_code == 201:
            self.update_config(response.text)
            print("config succesfully updated")

    # sends data to server to be saved on database
    def post_data(self):
        data = self.create_random_data()

        response = requests.post(self.base_url + "dispenser", json=data)
        print(response.text)

    def run(self):
        # apply configuration settings
        self.apply_config()

        # register
        self.register_dispenser()

        # continuously send data to simulate a high volume scenario
        while True:
            self.post_data()
            sleep(1.0)

    # dispense sanitiser
    def dispense(self):
        # refill fluid level
        if self.fluid_level <= 0.0:
            print("fluid levels low, refilling...")
            self.fluid_level = self.fluid_capacity
            print("fluid levels successfully refilled")
        
        else:
            self.fluid_level -= self.fluid_dispense_volume

        return self.fluid_level

    def create_random_data(self):
        if randint(0, 1) == 0:
            # whether a user within range decided to use sanitiser
            ignored = False
        else:
            ignored = True

        data = {
            "device_id": self.device_id,
            "distance": uniform(0, 2),
            "volume_dispensed": 1.0,
            "fluid_level": self.dispense(),
            "ignored": ignored,
            "datetime": dt.now().strftime("%d/%m/%Y, %H:%M:%S")
        }

        return data

if __name__ == "__main__":
    client = Client("http://192.168.0.52:5000/")
    client.run()
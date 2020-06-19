import requests

base_url = "http://192.168.0.52:8080/api/"

def get_data(url):
    response = requests.get(base_url + url)
    return response.json()

def compute_statistics(dispensers, dispenser_data):
    overall_ignored = []
    for dispenser in dispensers:
        ignored = []
        name = dispenser["name"]
        location = dispenser["location"]
        created = dispenser["created"]
        id_1 = dispenser["device_id"]
        for data in dispenser_data:
            id_2 = data["device_id"]
            if id_1 == id_2:
                ignored.append(data["ignored"])
        
        # % dispenser was ignored
        ignored_rate = sum(ignored) / len(ignored)
        # % dispenser was not ignored
        adherence_rate = 1 - ignored_rate

        overall_ignored.append(ignored_rate)

        print("{}\nlocation: {}\ncreated: {}\ndevice_id: {:d}\nIgnored rate: {:.2f}%\nAdherence rate: {:.2f}%\n".format(name, location, created, id_1, ignored_rate, adherence_rate))

    overall_ignored_rate = sum(overall_ignored) / len(overall_ignored)
    overall_adherance_rate = 1 - overall_ignored_rate

    print("Overall ignored rate: {:.2f}%".format(overall_ignored_rate))
    print("Overall adherance rate: {:.2f}%".format(overall_adherance_rate))

def main():
    dispensers = get_data("dispenser/all")
    dispenser_data = get_data(("dispenser/data/all"))

    compute_statistics(dispensers, dispenser_data)

if __name__ == "__main__":
    main()
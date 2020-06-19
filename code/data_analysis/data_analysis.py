import requests
import matplotlib.pyplot as plt

base_url = "http://192.168.0.52:8080/api/"

def get_data(url):
    response = requests.get(base_url + url)
    return response.json()

def compute_statistics(dispensers, dispenser_data):
    overall_ignored = []
    overall_dispensals = []
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

        # number of times dispenser was used
        # False ignore entries mean a dispensal occurred
        # dispensal count is the sum of False entries
        dispensal_count = len(ignored) - sum(ignored)

        # append everything from one list to another
        overall_dispensals.extend(ignored)

        overall_ignored.append(ignored_rate)

        print("{}\nLocation: {}\nCreated: {}\nDevice_id: {:d}\nIgnored rate: {:.2f}%\nAdherence rate: {:.2f}%\nTotal dispensals: {:d}\n".format(name, location, created, id_1, ignored_rate, adherence_rate, dispensal_count))

    overall_ignored_rate = sum(overall_ignored) / len(overall_ignored)
    overall_adherance_rate = 1 - overall_ignored_rate

    overall_total_dispensals = sum(overall_dispensals)

    print("Overall ignored rate: {:.2f}%".format(overall_ignored_rate))
    print("Overall adherance rate: {:.2f}%".format(overall_adherance_rate))
    print("Overall total dispensals: {:d}".format(overall_total_dispensals))

    plot_dispensals(overall_dispensals)

def plot_dispensals(dispensals):
    # convert True to 1 and False to 0
    for i in range(len(dispensals)):
        if dispensals[i] == True:
            dispensals[i] = 1
        else:
            dispensals[i] = 0

    # convert list to show the total dispensals so far for each time period
    # e.g [0, 1, 1, 0] becomes [0, 1, 2, 2]
    for i in range(1, len(dispensals)):
        dispensals[i] += dispensals[i-1]

    plt.title("Total dispensals over time")
    plt.xlabel("Time")
    plt.ylabel("Dispensals")
    plt.plot(dispensals, label="Dispensals")
    plt.grid()
    plt.legend()
    plt.show()

def main():
    dispensers = get_data("dispenser/all")
    dispenser_data = get_data(("dispenser/data/all"))

    compute_statistics(dispensers, dispenser_data)

if __name__ == "__main__":
    main()
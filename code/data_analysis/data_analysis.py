import requests
import matplotlib.pyplot as plt

base_url = "http://localhost:8080/api/"

def get_data(url):
    response = requests.get(base_url + url)
    return response.json()

def compute_statistics(dispensers, dispenser_data):
    overall_ignored = []
    overall_dispenses = []
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
        ignored_rate = sum(ignored) / len(ignored) * 100
        # % dispenser was not ignored
        adherence_rate = 100 - ignored_rate

        # number of times dispenser was used
        # False ignore entries mean a dispensal occurred
        # dispensal count is the sum of False entries
        dispensal_count = len(ignored) - sum(ignored)

        # append everything from one list to another
        overall_dispenses.extend(ignored)

        overall_ignored.append(ignored_rate)

        print("{}\nLocation: {}\nCreated: {}\nDevice_id: {:d}\nIgnored rate: {:.2f}%\nAdherence rate: {:.2f}%\nTotal dispenses: {:d}\n".format(name, location, created, id_1, ignored_rate, adherence_rate, dispensal_count))

    overall_ignored_rate = sum(overall_ignored) / len(overall_ignored)
    overall_adherence_rate = 100 - overall_ignored_rate

    overall_total_dispenses = sum(overall_dispenses)

    print("Overall ignored rate: {:.2f}%".format(overall_ignored_rate))
    print("Overall adherence rate: {:.2f}%".format(overall_adherence_rate))
    print("Overall total dispenses: {:d}".format(overall_total_dispenses))

    plot_dispenses(overall_dispenses)

def plot_dispenses(dispenses):
    # convert True to 1 and False to 0
    for i in range(len(dispenses)):
        if dispenses[i] == True:
            dispenses[i] = 1
        else:
            dispenses[i] = 0

    # convert list to show the total dispenses so far for each time period
    # e.g [0, 1, 1, 0] becomes [0, 1, 2, 2]
    for i in range(1, len(dispenses)):
        dispenses[i] += dispenses[i-1]

    plt.title("Total dispenses over time")
    plt.xlabel("Time")
    plt.ylabel("Dispenses")
    plt.plot(dispenses, label="Dispenses")
    plt.grid()
    plt.legend()
    plt.show()

def main():
    dispensers = get_data("dispenser/all")
    dispenser_data = get_data(("dispenser/data/all"))

    compute_statistics(dispensers, dispenser_data)

if __name__ == "__main__":
    main()
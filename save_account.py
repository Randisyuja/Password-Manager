import json
from tkinter import messagebox


def save(website, email, password):
    new_data = {
        "website": website,
        "email": email,
        "password": password,
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("database.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("database.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data

            numeric_keys = [int(k) for k in data.keys() if k.isdigit()]
            next_index = str(max(numeric_keys) + 1) if numeric_keys else "0"

            data[next_index] = new_data

            with open("database.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
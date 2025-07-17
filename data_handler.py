import json
from tkinter import messagebox, END
from constants import *


def save_data(website_entry, email_entry, password_entry):
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        "website": website,
        "email": email,
        "password": password,
    }

    if not website or not password:
        messagebox.showinfo("Oops", "Please fill in all required fields.")
        return

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    numeric_keys = [int(k) for k in data if k.isdigit()]
    next_key = str(max(numeric_keys) + 1) if numeric_keys else "0"
    data[next_key] = new_data

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo("Successful", "Account has been added successfully.")
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


def find_password(website_entry, tree):
    from tkinter import messagebox
    for item in tree.get_children():
        tree.delete(item)

    keyword = website_entry.get().lower()

    try:
        with open(DATA_FILE, "r") as file:
            database = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data file found.")
        return

    matches = [val for val in database.values() if keyword in val["website"].lower()]
    if matches:
        for item in matches:
            tree.insert("", "end", values=(item["website"], item["email"], item["password"]))
    else:
        messagebox.showinfo("Not Found", f"No data found for {keyword}.")

    website_entry.delete(0, END)


def tampilkan_data(tree):
    tree.delete(*tree.get_children())
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    for item in data.values():
        tree.insert("", "end", values=(item["website"], item["email"], item["password"]))


def edit_data(tree, website_entry, email_entry, password_entry, add_button, refresh_callback):
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to edit.")
        return

    values = tree.item(selected, "values")
    old_website, old_email = values[0], values[1]

    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)
    website_entry.insert(0, old_website)
    email_entry.insert(0, old_email)
    password_entry.insert(0, values[2])

    def update_record():
        new_website = website_entry.get()
        new_email = email_entry.get()
        new_password = password_entry.get()

        if not new_website or not new_password:
            messagebox.showwarning("Warning", "Website and password cannot be empty.")
            return

        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            keys_to_delete = [k for k, v in data.items() if v["website"] == old_website and v["email"] == old_email]
            for k in keys_to_delete:
                del data[k]

            numeric_keys = [int(k) for k in data if k.isdigit()]
            next_key = str(max(numeric_keys) + 1) if numeric_keys else "0"

            data[next_key] = {
                "website": new_website,
                "email": new_email,
                "password": new_password
            }

            with open(DATA_FILE, "w") as file:
                json.dump(data, file, indent=4)

            refresh_callback(tree)
            messagebox.showinfo("Success", "Record updated successfully.")

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)

        except FileNotFoundError:
            messagebox.showerror("Error", "Data file not found.")

        add_button.config(text="Add", command=lambda: save_data(website_entry, email_entry, password_entry))

    add_button.config(text="Update", command=update_record)


def delete_data(tree, refresh_callback):
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to delete.")
        return

    from tkinter import messagebox
    if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
        return

    values = tree.item(selected, "values")
    website, email = values[0], values[1]

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        keys_to_delete = [k for k, v in data.items() if v["website"] == website and v["email"] == email]
        for k in keys_to_delete:
            del data[k]

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

        refresh_callback(tree)
        messagebox.showinfo("Success", "Record deleted successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found.")

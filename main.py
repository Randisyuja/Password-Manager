from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import json
from generate_password import generate_password
from save_account import save

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCK_IMG_PATH = os.path.join(SCRIPT_DIR, "img/lock.png")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def callpassword():
    password_entry.delete(0, END)
    password = generate_password()
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def callsave():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    save(website, email, password)

    if save:
        messagebox.showinfo(title="Successful", message="New account has been added.")
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    for item in tree.get_children():
        tree.delete(item)

    website = website_entry.get()

    try:
        with open("database.json") as data_file:
            database = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        data = [value for key, value in database.items() if website in value["website"].lower()]
        if data:
            for info in data:
                tree.insert("", "end", values=(info["website"], info["email"], info["password"]))
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")
    finally:
        website_entry.delete(0, END)


# ---------------------------- SHOW DATA ------------------------------- #
def tampilkan_data():
    for item in tree.get_children():
        tree.delete(item)

    try:
        with open("database.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    for website, info in data.items():
        tree.insert("", "end", values=(info["website"], info["email"], info["password"]))


def edit_data():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a record to edit.")
        return

    values = tree.item(selected_item, "values")
    old_website = values[0]
    old_email = values[1]

    # Isi form dengan data yang dipilih
    website_entry.delete(0, END)
    website_entry.insert(0, values[0])
    email_entry.delete(0, END)
    email_entry.insert(0, values[1])
    password_entry.delete(0, END)
    password_entry.insert(0, values[2])

    # Update database setelah user mengedit di form lalu klik tombol Add lagi
    def update_record():
        new_website = website_entry.get()
        new_email = email_entry.get()
        new_password = password_entry.get()

        if not new_website or not new_password:
            messagebox.showwarning("Warning", "Website and Password cannot be empty.")
            return

        try:
            with open("database.json", "r") as file:
                data = json.load(file)

            # Delete old record
            keys_to_delete = [key for key, val in data.items()
                              if val["website"] == old_website and val["email"] == old_email]
            for key in keys_to_delete:
                del data[key]

            # Add new record
            new_key = new_website + new_email
            data[new_key] = {
                "website": new_website,
                "email": new_email,
                "password": new_password
            }

            with open("database.json", "w") as file:
                json.dump(data, file, indent=4)

            tampilkan_data()
            messagebox.showinfo("Success", "Record updated successfully.")

            # Bersihkan form setelah update
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)

        except FileNotFoundError:
            messagebox.showerror("Error", "Data file not found.")

    # Ganti tombol Add jadi Update sementara
    add_button.config(text="Update", command=update_record)


def delete_data():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a record to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")
    if not confirm:
        return

    values = tree.item(selected_item, "values")
    website_to_delete = values[0]
    email_to_delete = values[1]

    try:
        with open("database.json", "r") as file:
            data = json.load(file)

        keys_to_delete = [key for key, val in data.items()
                          if val["website"] == website_to_delete and val["email"] == email_to_delete]

        if not keys_to_delete:
            messagebox.showinfo("Info", "Record not found in the database.")
            return

        for key in keys_to_delete:
            del data[key]

        with open("database.json", "w") as file:
            json.dump(data, file, indent=4)

        tampilkan_data()
        messagebox.showinfo("Success", "Record deleted successfully.")

    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=50)
footer = Label(window, text="© 2025 Randi Syuja. All rights reserved.", fg="gray", font=("Arial", 10))
footer.grid(row=99, column=0, columnspan=10, pady=(100, 0))



canvas = Canvas(height=200, width=200)
original_image = Image.open(LOCK_IMG_PATH)
resized_image = original_image.resize((200, 200))  # Resize ke canvas 200x200
logo_img = ImageTk.PhotoImage(resized_image)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=1, column=1)

# Labels
judul = Label(text="Password Manager", font="Arial 20 bold")
judul.grid(row=2, column=1, columnspan=1)
website_label = Label(text="Website:")
website_label.grid(row=3, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=4, column=0)
password_label = Label(text="Password:")
password_label.grid(row=5, column=0)
akun_label = Label(text="Account Lists", font="Arial 16 bold")
akun_label.grid(row=0, column=6, columnspan=3, padx=(100,0))

# Entries
website_entry = Entry(width=48)
website_entry.grid(row=3, column=1)
website_entry.focus()
email_entry = Entry(width=70)
email_entry.grid(row=4, column=1, columnspan=2)
password_entry = Entry(width=48)
password_entry.grid(row=5, column=1)

# Buttons
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=3, column=2, padx=(15, 0), pady=(10, 10))
generate_password_button = Button(text="Generate Password", command=callpassword)
generate_password_button.grid(row=5, column=2, padx=(15, 0), pady=(10, 10))
add_button = Button(text="Add", width=30, command=callsave)
add_button.grid(row=6, column=1, columnspan=1)
tampil_data = Button(window, text="Tampilkan Data", width=15, command=tampilkan_data)
tampil_data.grid(row=3, column=6, pady=10)
edit_button = Button(window, text="Edit", width=15, command=edit_data)
edit_button.grid(row=4, column=6, pady=10, padx=10)
delete_button = Button(window, text="Delete", width=15, command=delete_data)
delete_button.grid(row=5, column=6, pady=10, padx=10)


# Treeview (tabel)
tree = ttk.Treeview(window, columns=("Website", "Email", "Password"), show="headings")
tree.heading("Website", text="Website")
tree.heading("Email", text="Email")
tree.heading("Password", text="Password")
tree.grid(row=1, column=6, columnspan=3, padx=(50, 0), pady=10)

window.mainloop()

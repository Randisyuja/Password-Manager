from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from password_generator import generate_password
from data_handler import save_data, find_password, tampilkan_data, edit_data, delete_data, copy_password
from constants import LOCK_IMG_PATH, MASTER_FILE
from authentication import save_master_password, validate_master_password
import os


def main_app():
    window = Tk()
    window.title("Password Manager")
    window.config(padx=100, pady=50)

    # Footer
    footer = Label(window, text="© 2025 Randi Syuja. All rights reserved.", fg="gray", font=("Arial", 10))
    footer.grid(row=99, column=0, columnspan=10, pady=(100, 0))

    # Canvas and Logo
    canvas = Canvas(height=200, width=200)
    original_image = Image.open(LOCK_IMG_PATH)
    resized_image = original_image.resize((200, 200))
    logo_img = ImageTk.PhotoImage(resized_image)
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(row=1, column=1)

    # Labels
    Label(text="Password Manager", font="Arial 20 bold").grid(row=2, column=1)
    Label(text="Website:").grid(row=3, column=0)
    Label(text="Email/Username:").grid(row=4, column=0)
    Label(text="Password:").grid(row=5, column=0)
    Label(text="Account Lists", font="Arial 16 bold").grid(row=0, column=6, columnspan=3, padx=(100, 0))

    # Entry Fields
    website_entry = Entry(width=48)
    website_entry.grid(row=3, column=1)
    website_entry.focus()
    email_entry = Entry(width=70)
    email_entry.grid(row=4, column=1, columnspan=2)
    password_entry = Entry(width=48)
    password_entry.grid(row=5, column=1)

    # Treeview
    tree = ttk.Treeview(window, columns=("Website", "Email", "Password"), show="headings")
    for col in ("Website", "Email", "Password"):
        tree.heading(col, text=col)
    tree.grid(row=1, column=6, columnspan=3, padx=(50, 0), pady=10)

    # Buttons
    Button(text="Search", width=15, command=lambda: find_password(website_entry, tree)).grid(row=3, column=2, padx=(15, 0))
    Button(text="Generate Password", command=lambda: generate_password(password_entry)).grid(row=5, column=2, padx=(15, 0))
    add_button = Button(text="Add", width=30, command=lambda: save_data(website_entry, email_entry, password_entry))
    add_button.grid(row=6, column=1, columnspan=1)
    Button(window, text="Tampilkan Data", width=15, command=lambda: tampilkan_data(tree)).grid(row=3, column=6, pady=10)
    Button(window, text="Edit", width=15, command=lambda: edit_data(tree, website_entry, email_entry, password_entry, add_button, tampilkan_data)).grid(row=4, column=6, pady=10, padx=10)
    Button(window, text="Delete", width=15, command=lambda: delete_data(tree, tampilkan_data)).grid(row=5, column=6, pady=10, padx=10)
    Button(window, text="Copy Password", width=15, command=lambda: copy_password(window, tree)).grid(row=6, column=6, pady=10)

    window.mainloop()


login_window = Tk()
login_window.title("Login - Password Manager")
login_window.geometry("300x180")


def check_password():
    input_pw = pw_entry.get()
    if not os.path.exists(MASTER_FILE):
        save_master_password(input_pw)
        messagebox.showinfo("Success", "Master password set. Restart app.")
        login_window.destroy()
    elif validate_master_password(input_pw):
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Error", "Wrong master password!")


Label(login_window, text="Enter Master Password:", font=("Arial", 12)).pack(pady=20)
pw_entry = Entry(login_window, show="*", width=25)
pw_entry.pack()
Button(login_window, text="Login", command=check_password).pack(pady=10)

pw_entry.focus()
login_window.mainloop()

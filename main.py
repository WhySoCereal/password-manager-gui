from tkinter import *
import tkinter.messagebox as message_box
import random as rd
import pyperclip
import json
# documentation tkinter = https://web.archive.org/web/20200313162549/http://effbot.org/tkinterbook/canvas.htm


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [rd.choice(letters) for _ in range(rd.randint(8, 10))]
    password_list += [rd.choice(symbols) for _ in range(rd.randint(2, 4))]
    password_list += [rd.choice(numbers) for _ in range(rd.randint(2, 4))]

    rd.shuffle(password_list)
    password = "".join(password_list)
    
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_pressed():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not website or not password:
        message_box.showerror(title="Error", message="Please fill out all fields.")
        return

    new_data = {website: {
        "email": email,
        "password": password
    }}

    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        with open("data.json", mode="w") as data_file:
            json.dump(new_data, data_file, indent=4)

    else:
        data.update(new_data)

        with open("data.json", mode="w") as data_file:
            json.dump(data, data_file, indent=4)

    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def search_website():
    website = website_entry.get()

    if not website:
        return

    with open("data.json", mode="r") as data_file:
        try:
            websites = json.load(data_file)
            email = websites[website]["email"]
            password = websites[website]["password"]
        except KeyError:
            message_box.showerror("Error", "Website doesn't exist")
        except FileNotFoundError:
            message_box.showerror("Error", "No data file found.")
        else:
            message_box.showinfo(website, f"Email: {email}\nPassword: {password}")
            pyperclip.copy(password)


# ---------------------------- UI SETUP ------------------------------- #
# Window Setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1)
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "bri_alldred@live.co.uk")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
generate_button = Button(text="Generate Password", command=generate_pass)
generate_button.grid(row=3, column=2)
add_button = Button(text="Add", command=add_pressed, width=36)
add_button.grid(row=4, column=1, columnspan=2)
search_website_button = Button(text="Search for website", command=search_website)
search_website_button.grid(row=1, column=2)

window.mainloop()

import tkinter as tk
from tkinter import messagebox
import json
from cryptography.fernet import Fernet

# Initialize the encryption key (in a real-world scenario, this should be securely stored)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Create a simple JSON file to store password data
PASSWORDS_FILE = "passwords.json"

# Function to encrypt data
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

# Function to save passwords to the JSON file
def save_passwords():
    passwords = {}
    passwords["master_password"] = encrypt_data(master_password_entry.get())
    passwords["entries"] = []
    for entry in password_entries:
        encrypted_entry = {
            "website": encrypt_data(entry["website"]),
            "username": encrypt_data(entry["username"]),
            "password": encrypt_data(entry["password"])
        }
        passwords["entries"].append(encrypted_entry)
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(passwords, f)

# Function to load passwords from the JSON file
def load_passwords():
    try:
        with open(PASSWORDS_FILE, "r") as f:
            passwords = json.load(f)
            return passwords
    except FileNotFoundError:
        return None

# Function to handle the "View Passwords" button click
def view_passwords():
    passwords = load_passwords()
    if passwords is None:
        return
    for entry in passwords["entries"]:
        decrypted_entry = {
            "website": decrypt_data(entry["website"]),
            "username": decrypt_data(entry["username"]),
            "password": decrypt_data(entry["password"])
        }
        print(decrypted_entry)

# Function to handle the "Add Entry" button click
def add_entry():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if not website or not username or not password:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    password_entries.append({"website": website, "username": username, "password": password})
    clear_entry_fields()

# Function to clear entry fields
def clear_entry_fields():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Password Manager")

# Create and arrange GUI elements
master_password_label = tk.Label(root, text="Master Password:")
master_password_label.pack()
master_password_entry = tk.Entry(root, show="*")
master_password_entry.pack()

website_label = tk.Label(root, text="Website:")
website_label.pack()
website_entry = tk.Entry(root)
website_entry.pack()

username_label = tk.Label(root, text="Username/Email:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

add_button = tk.Button(root, text="Add Entry", command=add_entry)
add_button.pack()

view_button = tk.Button(root, text="View Passwords", command=view_passwords)
view_button.pack()

# Initialize the list to store password entries
password_entries = []

# Start the main GUI loop
root.mainloop()

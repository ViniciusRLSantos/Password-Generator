import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from Apps.password_list import PasswordList
import secrets
import string
import json


class PasswordGenerator(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.title_label = ttk.Label(self, text="Password Generator", font=(20)).grid(column=0, row=0, columnspan=3)
        
        # Service
        self.service_label = ttk.Label(self, text="Service: ").grid(column=0, row=1, sticky=E)
        self.service_variable = tk.StringVar()
        self.service_entry = ttk.Entry(self, textvariable=self.service_variable, width=30).grid(column=1, row=1)
        
        # User/ E-Mail
        self.user_label = ttk.Label(self, text="User: ").grid(column=0, row=2, sticky=E)
        self.user_variable = tk.StringVar()
        self.user_entry = ttk.Entry(self, textvariable=self.user_variable, width=30).grid(column=1, row=2)
        
        # Password
        self.password_label = ttk.Label(self, text="Password: ").grid(column=0, row=3, sticky=E)
        self.password_generated = tk.StringVar()
        self.password_generated_display = ttk.Label(self, textvariable=self.password_generated, width=18).grid(column=1, row=3)
        
        self.password_length_label = ttk.Label(self, text="Length: ").grid(column=0, row=4, sticky=E)
        self.password_length_variable = tk.IntVar()
        self.password_length_variable.set(12)
        self.password_length_slider = tk.Scale(self, from_=8, to=18, orient="horizontal", variable=self.password_length_variable, length=40, sliderlength=20).grid(column=1, row=4, sticky=(N, W))
        
        # Buttons
        self.generate_button = ttk.Button(self, text="Generate", command=lambda: self.generate_password(self.password_length_variable.get())).grid(column=2, row=3)
        self.save_button = ttk.Button(self, text="Save Password", command=self.save_password).grid(column=2, row=1)
        self.load_button = ttk.Button(self, text="Load Password", command=lambda: self.load_password(self.services_combobox.get())).grid(column=2, row=2)
        self.view_passwords_button = ttk.Button(self, text="View Passwords", command=lambda: PasswordList(self)).grid(column=2, row=4)
        
        # Services ComboBox to load password from
        with open("saved_passwords.json", "r") as file:
            saved_services = json.load(file)
        services = list(saved_services.keys())
        self.load_from_label = ttk.Label(self, text="Service to load: ").grid(column=1, row=5, sticky=E)
        self.services_combobox = ttk.Combobox(self, values=services)
        self.services_combobox.grid(column=2, row=5, columnspan=3, sticky=W)
        for widget in self.winfo_children():
            widget.grid(padx=0, pady=1)
        
    
    def generate_password(self, length: int = 10):
        letters = string.ascii_letters
        digits = string.digits
        special_keys = string.punctuation
        all_keys = letters + digits + special_keys
        password = ""
        for i in range(length):
            password = password + all_keys[secrets.randbelow(len(all_keys))]
        # return password
        self.password_generated.set(password)
    
    
    def save_password(self):
        with open("saved_passwords.json", "r") as file:
            password_list = json.load(file)
        
        service = self.service_variable.get()
        user = self.user_variable.get()
        password = self.password_generated.get()
        
        if service == "" or user == "" or password == "":
            showinfo(title="Blank Entries", message="Please fill in all blank entries for this to work.")
            return
        
        password_list[service] = {
            "User": user,
            "Password": password
        }
        with open("saved_passwords.json", "w") as file:
            json.dump(password_list, file, indent=4)
    
    
    def load_password(self, service_name: str):
        
        if self.services_combobox.get() == "":
            showinfo(title="Blank Entry", message="Cannot load a blank service name.")
            return
        
        with open("saved_passwords.json", "r") as file:
            password_list = json.load(file)
        
        self.service_variable.set(self.services_combobox.get())
        self.user_variable.set(password_list[service_name]["User"])
        self.password_generated.set(password_list[service_name]["Password"])


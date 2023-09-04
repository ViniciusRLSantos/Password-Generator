from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import json


class PasswordList(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Passwords List")
        # self.geometry("800x600")
        
        self.title_label = ttk.Label(self, text="List of Passwords").grid(column=0, row=0)
        
        # Creates and configures the password tree
        columns = ("service", "user", "password")
        self.password_tree = Treeview(self, columns=columns, show="headings", height=5)
        self.password_tree.heading("service", text="Service")
        self.password_tree.heading("user", text="User/E-Mail")
        self.password_tree.heading("password", text="Password")
        self.password_tree.column("service", minwidth=100)
        self.password_tree.column("user", minwidth=100)
        self.password_tree.column("password", minwidth=100)
        self.password_tree.grid(column=0, row=0, sticky=NSEW)
        
        
        # Inserts data to the password tree
        with open("saved_passwords.json", "r") as file:
            password_dictionary = json.load(file)
        password_services = list(password_dictionary.keys())
        password_list = []
        for service in password_services:
            password_list.append((service, password_dictionary[service]["User"], password_dictionary[service]["Password"]))
        for password in password_list:
            self.password_tree.insert("", tk.END, values=password)
        
        # Close Button
        self.close_button = ttk.Button(self, text="Close", command=self.destroy).grid(column=0, row=2)
        
        for widget in self.winfo_children():
            widget.grid(padx=1, pady=2)
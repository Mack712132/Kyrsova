import csv
import os
import tkinter as tk
from tkinter import messagebox, ttk

DATABASE_FILE = "contacts.csv"

def create_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Address", "Email", "Mobile", "Home"])

def add_contact():
    name = name_entry.get()
    address = address_entry.get()
    email = email_entry.get()
    mobile = mobile_entry.get()
    home = home_entry.get()

    with open(DATABASE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, address, email, mobile, home])
    
    messagebox.showinfo("Успіх", "Контакт успішно доданий.")
    clear_entries()

def load_contacts_for_edit():
    with open(DATABASE_FILE, newline="") as file:
        reader = csv.reader(file)
        contacts = list(reader)

    name_to_edit_combo['values'] = [contact[0] for contact in contacts[1:]]

def load_contact_details(*args):
    selected_name = name_to_edit_combo.get()
    with open(DATABASE_FILE, newline="") as file:
        reader = csv.reader(file)
        contacts = list(reader)
        for contact in contacts:
            if contact[0] == selected_name:
                name_edit_entry.delete(0, tk.END)
                address_edit_entry.delete(0, tk.END)
                email_edit_entry.delete(0, tk.END)
                mobile_edit_entry.delete(0, tk.END)
                home_edit_entry.delete(0, tk.END)

                name_edit_entry.insert(0, contact[0])
                address_edit_entry.insert(0, contact[1])
                email_edit_entry.insert(0, contact[2])
                mobile_edit_entry.insert(0, contact[3])
                home_edit_entry.insert(0, contact[4])
                break

def edit_contact():
    old_name = name_to_edit_combo.get()
    new_name = name_edit_entry.get()
    new_address = address_edit_entry.get()
    new_email = email_edit_entry.get()
    new_mobile = mobile_edit_entry.get()
    new_home = home_edit_entry.get()

    with open(DATABASE_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        contacts = list(reader)

    with open(DATABASE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for contact in contacts:
            if contact[0] == old_name:
                writer.writerow([new_name, new_address, new_email, new_mobile, new_home])
            else:
                writer.writerow(contact)

    messagebox.showinfo("Успіх", "Контакт успішно відредагований.")
    clear_edit_entries()
    load_contacts_for_edit()

def view_contacts():
    with open(DATABASE_FILE, newline="") as file:
        reader = csv.reader(file)
        contacts = list(reader)
        if len(contacts) > 1:
            contacts.sort(key=lambda x: x[0]) 
            contact_list = "\n".join(["Ім'я: {}, Адреса: {}, Email: {}, Мобільний: {}, Домашній: {}".format(*contact) for contact in contacts[1:]])
            messagebox.showinfo("Контакти", contact_list)
        else:
            messagebox.showinfo("Порожній довідник", "Довідник порожній.")

def delete_contact():
    name_to_delete = name_to_delete_entry.get()

    with open(DATABASE_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        contacts = list(reader)

    with open(DATABASE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for contact in contacts:
            if contact[0] != name_to_delete:
                writer.writerow(contact)

    messagebox.showinfo("Успіх", "Контакт успішно видалений.")
    clear_delete_entry()

def search_contacts():
    search_term = search_term_entry.get()
    found_contacts = []

    with open(DATABASE_FILE, newline="") as file:
        reader = csv.reader(file)
        next(reader)  
        for contact in reader:
            if (search_term in contact[0]) or (search_term in contact[3]) or (search_term in contact[4]):
                found_contacts.append(contact)

    if found_contacts:
        found_contact_list = "\n".join(["Ім'я: {}, Адреса: {}, Email: {}, Мобільний: {}, Домашній: {}".format(*contact) for contact in found_contacts])
        messagebox.showinfo("Знайдені контакти", found_contact_list)
    else:
        messagebox.showinfo("Контакти не знайдені", "Контактів за вказаним прізвищем або номером телефону не знайдено.")
    clear_search_entry()

def clear_entries():
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    mobile_entry.delete(0, tk.END)
    home_entry.delete(0, tk.END)

def clear_edit_entries():
    name_to_edit_combo.set('')
    name_edit_entry.delete(0, tk.END)
    address_edit_entry.delete(0, tk.END)
    email_edit_entry.delete(0, tk.END)
    mobile_edit_entry.delete(0, tk.END)
    home_edit_entry.delete(0, tk.END)

def clear_delete_entry():
    name_to_delete_entry.delete(0, tk.END)

def clear_search_entry():
    search_term_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Телефонний довідник")

tab_control = ttk.Notebook(root)
tab_add = ttk.Frame(tab_control)
tab_edit = ttk.Frame(tab_control)
tab_view_delete = ttk.Frame(tab_control)
tab_search = ttk.Frame(tab_control)

tab_control.add(tab_add, text='Додати контакт')
tab_control.add(tab_edit, text='Редагувати контакт')
tab_control.add(tab_view_delete, text='Переглянути/Видалити контакт')
tab_control.add(tab_search, text='Пошук контакту')
tab_control.pack(expand=1, fill='both')

tk.Label(tab_add, text="Ім'я та прізвище:").grid(row=0, column=0, sticky="w")
tk.Label(tab_add, text="Адреса:").grid(row=1, column=0, sticky="w")
tk.Label(tab_add, text="Електронна пошта:").grid(row=2, column=0, sticky="w")
tk.Label(tab_add, text="Мобільний телефон:").grid(row=3, column=0, sticky="w")
tk.Label(tab_add, text="Домашній телефон:").grid(row=4, column=0, sticky="w")

name_entry = tk.Entry(tab_add)
address_entry = tk.Entry(tab_add)
email_entry = tk.Entry(tab_add)
mobile_entry = tk.Entry(tab_add)
home_entry = tk.Entry(tab_add)

name_entry.grid(row=0, column=1)
address_entry.grid(row=1, column=1)
email_entry.grid(row=2, column=1)
mobile_entry.grid(row=3, column=1)
home_entry.grid(row=4, column=1)

add_button = tk.Button(tab_add, text="Додати контакт", command=add_contact)
add_button.grid(row=5, columnspan=2)

tk.Label(tab_edit, text="Виберіть контакт для редагування:").grid(row=0, column=0, sticky="w")
name_to_edit_combo = ttk.Combobox(tab_edit, postcommand=load_contacts_for_edit)
name_to_edit_combo.grid(row=0, column=1)
name_to_edit_combo.bind("<<ComboboxSelected>>", load_contact_details)

tk.Label(tab_edit, text="Нове ім'я та прізвище:").grid(row=1, column=0, sticky="w")
name_edit_entry = tk.Entry(tab_edit)
name_edit_entry.grid(row=1, column=1)

tk.Label(tab_edit, text="Нова адреса:").grid(row=2, column=0, sticky="w")
address_edit_entry = tk.Entry(tab_edit)
address_edit_entry.grid(row=2, column=1)

tk.Label(tab_edit, text="Нова електронна пошта:").grid(row=3, column=0, sticky="w")
email_edit_entry = tk.Entry(tab_edit)
email_edit_entry.grid(row=3, column=1)

tk.Label(tab_edit, text="Новий мобільний телефон:").grid(row=4, column=0, sticky="w")
mobile_edit_entry = tk.Entry(tab_edit)
mobile_edit_entry.grid(row=4, column=1)

tk.Label(tab_edit, text="Новий домашній телефон:").grid(row=5, column=0, sticky="w")
home_edit_entry = tk.Entry(tab_edit)
home_edit_entry.grid(row=5, column=1)

edit_button = tk.Button(tab_edit, text="Редагувати контакт", command=edit_contact)
edit_button.grid(row=6, columnspan=2)

view_button = tk.Button(tab_view_delete, text="Переглянути контакти", command=view_contacts)
view_button.grid(row=0, columnspan=2)

tk.Label(tab_view_delete, text="Ім'я контакту для видалення:").grid(row=1, column=0, sticky="w")
name_to_delete_entry = tk.Entry(tab_view_delete)
name_to_delete_entry.grid(row=1, column=1)

delete_button = tk.Button(tab_view_delete, text="Видалити контакт", command=delete_contact)
delete_button.grid(row=2, columnspan=2)

tk.Label(tab_search, text="Пошук за прізвищем або номером телефону:").grid(row=0, column=0, sticky="w")
search_term_entry = tk.Entry(tab_search)
search_term_entry.grid(row=0, column=1)

search_button = tk.Button(tab_search, text="Пошук контакту", command=search_contacts)
search_button.grid(row=1, columnspan=2)

create_database()

root.mainloop()

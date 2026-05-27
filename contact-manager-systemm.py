import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "contacts.txt"

contacts_cache = []

def load_contacts():
    
    global contacts_cache
    contacts_cache = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                data = line.strip().split(" | ")
                if len(data) == 3:
                    contacts_cache.append(data)
    except FileNotFoundError:
        open(FILE_NAME, "w").close()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    return contacts_cache


def save_contacts(contacts):
    
    try:
        with open(FILE_NAME, "w") as file:
            for c in contacts:
                file.write(" | ".join(c) + "\n")
    except Exception as e:
        messagebox.showerror("Save Error", str(e))

def refresh_table(data=None):
    for row in table.get_children():
        table.delete(row)

    contacts = data if data is not None else contacts_cache

    if not contacts:
        table.insert("", "end", values=("", "No contact found", "", ""))
        return

    for i, c in enumerate(contacts, start=1):
        tag = "even_row" if i % 2 == 0 else "odd_row"
        table.insert("", "end", values=(i, c[0], c[1], c[2]), tags=(tag,))

def is_valid_ph_number(phone):
    
    if phone.startswith("+"):
        phone = phone[1:]
        
    if not phone.isdigit():
        return False
    
    if phone.startswith("09") and len(phone) == 11:
        return True
    
    if phone.startswith("639") and len(phone) == 12:
        return True
    return False

def add_contact():
    try:
        name, phone, address = [e.get().strip() for e in (name_entry, phone_entry, address_entry)]

        if not name or not phone or not address:
            messagebox.showwarning("Error", "Please fill all fields!")
            return

        if not is_valid_ph_number(phone):
            messagebox.showwarning(
                "Invalid Input",
                "Enter a valid PH number.\n"
                "Accepted formats: 09XXXXXXXXX or 639XXXXXXXXX"
            )
            return

        new_contact = [name, phone, address]
        contacts_cache.append(new_contact)             

        with open(FILE_NAME, "a") as file:             
            file.write(" | ".join(new_contact) + "\n")

        clear_fields()
        refresh_table()
        status_label.config(text=f"'{name}' added successfully.")

    except Exception as e:
        messagebox.showerror("Add Error", str(e))

def delete_contact():
    try:
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact first!")
            return

        values = table.item(selected)["values"]
        if not values or values[1] == "No contact found":
            return

        index = int(values[0]) - 1

        confirm = messagebox.askyesno("Confirm Delete", "Do you want to delete this contact?")
        if not confirm:
            return

        if 0 <= index < len(contacts_cache):
            removed = contacts_cache.pop(index)         
            save_contacts(contacts_cache)               

        refresh_table()
        status_label.config(text=f"'{removed[0]}' deleted successfully.")

    except Exception as e:
        messagebox.showerror("Delete Error", str(e))

def update_contact():
    try:
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact first!")
            return

        values = table.item(selected)["values"]
        if not values or values[1] == "No contact found":
            return

        new_name  = name_entry.get().strip()
        new_phone = phone_entry.get().strip()
        new_addr  = address_entry.get().strip()

        if not new_name or not new_phone or not new_addr:
            messagebox.showwarning("Error", "Please fill all fields!")
            return

        if not is_valid_ph_number(new_phone):
            messagebox.showwarning(
                "Invalid Input",
                "Enter a valid PH number.\n"
                "Accepted formats: 09XXXXXXXXX or 639XXXXXXXXX"
            )
            return

        index = int(values[0]) - 1

        if 0 <= index < len(contacts_cache):
            contacts_cache[index] = [new_name, new_phone, new_addr]  
            save_contacts(contacts_cache)                              

        refresh_table()
        clear_fields()
        status_label.config(text=f"'{new_name}' updated successfully.")

    except Exception as e:
        messagebox.showerror("Update Error", str(e))

def search_contact(event=None):
    query = search_entry.get().strip().lower()

    if query == "":
        refresh_table()             # Show all when search is cleared
        return

    filtered = [
        c for c in contacts_cache  # Scan cache only — no file read
        if query in c[0].lower() or query in c[1].lower()
    ]

    refresh_table(filtered)

def sort_by_name():
    contacts_cache.sort(key=lambda x: x[0].lower())    
    save_contacts(contacts_cache)                        
    refresh_table(contacts_cache)
    status_label.config(text="Sorted A → Z successfully!")

def on_select(event):
    try:
        selected = table.focus()
        if not selected:
            return

        values = table.item(selected)["values"]
        if not values or values[1] == "No contact found":
            return

        for entry in (name_entry, phone_entry, address_entry):
            entry.delete(0, tk.END)

        name_entry.insert(0, values[1])
        phone_entry.insert(0, values[2])
        address_entry.insert(0, values[3])

    except Exception as e:
        messagebox.showerror("Select Error", str(e))

def clear_fields():
    for entry in (name_entry, phone_entry, address_entry):
        entry.delete(0, tk.END)

def call_contact():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact first!")
        return

    values = table.item(selected)["values"]
    if not values or values[1] == "No contact found":
        return

    phone = values[2]
    messagebox.showinfo("Call", f"Calling {phone}...")

def message_contact():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact first!")
        return

    values = table.item(selected)["values"]
    if not values or values[1] == "No contact found":
        return

    phone = values[2]

    msg_window = tk.Toplevel(root)
    msg_window.title("Send Message")
    msg_window.geometry("350x250")
    msg_window.configure(bg="#83004f")

    tk.Label(
        msg_window,
        text=f"Send message to: {phone}",
        bg="#83004f", fg="white",
        font=("Segoe UI", 11, "bold")
    ).pack(pady=10)

    message_entry = tk.Text(msg_window, height=6, width=35)
    message_entry.pack(pady=10)

    def send_message():
        message = message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Empty", "Type a message first!")
            return
        messagebox.showinfo("Sent", f"Message sent to {phone}!")
        msg_window.destroy()

    tk.Button(
        msg_window,
        text="Send",
        bg="#06b6d4", fg="white",
        font=("Segoe UI", 10, "bold"),
        command=send_message
    ).pack(pady=5)

root = tk.Tk()
root.title("CONTACT MANAGER")
root.geometry("1050x650")
root.configure(bg="#83004f")

left = tk.Frame(root, bg="#83004f", width=300)
left.pack(side="left", fill="y")

tk.Label(
    left,
    text="CONTACT MANAGER",
    bg="#83004f", fg="white",
    font=("Segoe UI", 20, "bold")
).pack(pady=15, padx=15)

tk.Label(left, text="FULL NAME *",      bg="#83004f", fg="#ffffff").pack(anchor="w", padx=20)
name_entry = tk.Entry(left, bg="#fcbce2", fg="black", insertbackground="black", font=("Segoe UI", 11), width=28)
name_entry.pack(padx=20, pady=4, fill="x", ipady=3)

tk.Label(left, text="PHONE NUMBER *",   bg="#83004f", fg="#ffffff").pack(anchor="w", padx=20)
phone_entry = tk.Entry(left, bg="#fcbce2", fg="black", insertbackground="black", font=("Segoe UI", 11), width=28)
phone_entry.pack(padx=20, pady=4, fill="x", ipady=3)

tk.Label(left, text="ADDRESS",          bg="#83004f", fg="#ffffff").pack(anchor="w", padx=20)
address_entry = tk.Entry(left, bg="#fcbce2", fg="black", insertbackground="black", font=("Segoe UI", 11), width=28)
address_entry.pack(padx=20, pady=4, fill="x", ipady=3)

btn_font = ("Segoe UI", 11)

tk.Button(left, text="Add Contact",     bg="#3d6fc1", fg="white", font=btn_font, command=add_contact   ).pack(padx=20, pady=10, fill="x", ipady=2)
tk.Button(left, text="Update Contact",  bg="#8b5cf6", fg="white", font=btn_font, command=update_contact).pack(padx=20, pady=10, fill="x", ipady=2)
tk.Button(left, text="Delete Contact",  bg="#ef4444", fg="white", font=btn_font, command=delete_contact).pack(padx=20, pady=10, fill="x", ipady=2)
tk.Button(left, text="Clear Fields",    bg="#8f887e", fg="white", font=btn_font, command=clear_fields  ).pack(padx=20, pady=10, fill="x", ipady=2)
tk.Button(left, text="Call Contact",    bg="#22c55e", fg="white", font=btn_font, command=call_contact  ).pack(padx=75, pady=5,  fill="x", ipady=5)
tk.Button(left, text="Message Contact", bg="#06b6d4", fg="white", font=btn_font, command=message_contact).pack(padx=75, pady=5, fill="x", ipady=5)

right = tk.Frame(root, bg="#83004f")
right.pack(side="right", expand=True, fill="both")

header = tk.Frame(right, bg="#83004f")
header.pack(fill="x", padx=15, pady=(8, 0))

tk.Label(
    header,
    text="ALL CONTACTS",
    bg="#83004f", fg="white",
    font=("Segoe UI", 10)
).pack(side="left", anchor="w", padx=10, pady=5)

search_frame = tk.Frame(header, bg="#83004f")
search_frame.pack(side="right", padx=5)

tk.Label(search_frame, text="🔍", bg="#83004f", fg="#d1d5db", font=("Segoe UI", 11)).pack(side="left", padx=(8, 4))

search_entry = tk.Entry(search_frame, width=25, font=("Segoe UI", 11))
search_entry.pack(side="left", ipady=3)
search_entry.bind("<KeyRelease>", search_contact)

status_label = tk.Label(right, text="", bg="#83004f", fg="#ffc2ee", font=("Segoe UI", 9))
status_label.pack(side="bottom", anchor="w", pady=3, padx=12, ipady=2)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",         background="#fcbce2", foreground="black", fieldbackground="#83004f")
style.configure("Treeview.Heading", background="#83004f", foreground="white")
style.configure("Treeview",         rowheight=28)

columns = ("No.", "Name", "Phone Number", "Address")
table = ttk.Treeview(right, columns=columns, show="headings", height=25)

table.heading("No.",          text="No.")
table.heading("Name",         text="Name ⇅", command=sort_by_name)
table.heading("Phone Number", text="Phone Number")
table.heading("Address",      text="Address")

table.column("No.",          width=50,  anchor="center")
table.column("Name",         width=200)
table.column("Phone Number", width=170)
table.column("Address",      width=260)

table.pack(padx=15, pady=8, fill="both", expand=True)
table.bind("<<TreeviewSelect>>", on_select)

load_contacts()
refresh_table()

root.mainloop()

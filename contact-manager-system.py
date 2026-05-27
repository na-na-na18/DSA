import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "contacts.txt"

def load_contacts():
    contacts = []

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                data = line.rstrip("\n").split(" | ")

                if len(data) == 3:
                    contacts.append(data)

    except FileNotFoundError:
        open(FILE_NAME, "w").close()

    except Exception as error:
        messagebox.showerror("Error", str(error))

    return contacts


def save_contacts(contacts):
    try:
        with open(FILE_NAME, "w") as file:
            for contact in contacts:
                file.write(" | ".join(contact) + "\n")

    except Exception as error:
        messagebox.showerror("Save Error", str(error))


def validate_fields(name, phone):
    if not name or not phone:
        messagebox.showwarning(
            "Required Fields",
            "Full Name and Phone Number are required."
        )
        return False

    allowed_chars = "0123456789+- "

    if not all(char in allowed_chars for char in phone):
        messagebox.showwarning(
            "Invalid Phone Number",
            "Phone number can only contain numbers, spaces, + and -"
        )
        return False

    return True

def refresh_table(data=None):
    for row in table.get_children():
        table.delete(row)

    contacts = data if data else load_contacts()

    if not contacts:
        table.insert("", "end", values=("", "No contact found", "", ""))
        return

    for index, contact in enumerate(contacts, start=1):
        tag = "even" if index % 2 == 0 else "odd"

        table.insert(
            "",
            "end",
            values=(
                index,
                contact[0],
                contact[1],
                contact[2]
            ),
            tags=(tag,)
        )

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    address = address_entry.get().strip()

    if not validate_fields(name, phone):
        return

    contacts = load_contacts()
    contacts.append([name, phone, address])
    save_contacts(contacts)
    refresh_table()
    clear_fields()
    status_label.config(text="Contact added successfully.")

def delete_contact():
    selected = table.focus()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    values = table.item(selected)["values"]

    if not values or values[1] == "No contact found":
        return

    confirm = messagebox.askyesno(
        "Delete Contact",
        "Do you want to delete this contact?"
    )

    if not confirm:
        return

    contacts = load_contacts()

    index = int(values[0]) - 1

    contacts.pop(index)
    save_contacts(contacts)
    refresh_table()
    clear_fields()
    status_label.config(text="Contact deleted successfully.")

def update_contact():
    selected = table.focus()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    values = table.item(selected)["values"]

    if not values or values[1] == "No contact found":
        return

    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    address = address_entry.get().strip()

    if not validate_fields(name, phone):
        return

    contacts = load_contacts()

    index = int(values[0]) - 1

    contacts[index] = [name, phone, address]
    save_contacts(contacts)
    refresh_table()
    clear_fields()
    status_label.config(text="Contact updated successfully.")

def on_select(event):
    selected = table.focus()

    if not selected:
        return

    values = table.item(selected)["values"]

    if not values or values[1] == "No contact found":
        return

    clear_fields()

    name_entry.insert(0, values[1])
    phone_entry.insert(0, values[2])
    address_entry.insert(0, values[3])


def search_contact(event=None):
    query = search_entry.get().lower()

    contacts = load_contacts()

    filtered_contacts = [
        contact
        for contact in contacts
        if query in contact[0].lower()
        or query in contact[1].lower()
    ]

    refresh_table(filtered_contacts)


def call_contact():
    selected = table.focus()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    values = table.item(selected)["values"]

    messagebox.showinfo(
        "Call",
        f"Calling {values[2]}..."
    )

def message_contact():
    selected = table.focus()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    values = table.item(selected)["values"]

    messagebox.showinfo(
        "Message",
        f"Messaging {values[2]}..."
    )

root = tk.Tk()

root.title("CONTACT MANAGER")
root.geometry("1050x650")
root.configure(bg="#83004f")

left = tk.Frame(
    root,
    bg="#83004f",
    width=300
)

left.pack(side="left", fill="y")

tk.Label(
    left,
    text="CONTACT MANAGER",
    bg="#83004f",
    fg="white",
    font=("Segoe UI", 20, "bold")
).pack(pady=15)

name_frame = tk.Frame(left, bg="#83004f")
name_frame.pack(anchor="w", padx=20)

tk.Label(
    name_frame,
    text="FULL NAME",
    bg="#83004f",
    fg="white"
).pack(side="left")

tk.Label(
    name_frame,
    text=" *",
    bg="#83004f",
    fg="red",
    font=("Segoe UI", 10, "bold")
).pack(side="left")

name_entry = tk.Entry(
    left,
    bg="#fcbce2",
    fg="black",
    font=("Segoe UI", 11)
)

name_entry.pack(
    padx=20,
    pady=5,
    fill="x",
    ipady=3
)

phone_frame = tk.Frame(left, bg="#83004f")
phone_frame.pack(anchor="w", padx=20)

tk.Label(
    phone_frame,
    text="PHONE NUMBER",
    bg="#83004f",
    fg="white"
).pack(side="left")

tk.Label(
    phone_frame,
    text=" *",
    bg="#83004f",
    fg="red",
    font=("Segoe UI", 10, "bold")
).pack(side="left")

phone_entry = tk.Entry(
    left,
    bg="#fcbce2",
    fg="black",
    font=("Segoe UI", 11)
)

phone_entry.pack(
    padx=20,
    pady=5,
    fill="x",
    ipady=3
)

tk.Label(
    left,
    text="ADDRESS",
    bg="#83004f",
    fg="white"
).pack(anchor="w", padx=20)

address_entry = tk.Entry(
    left,
    bg="#fcbce2",
    fg="black",
    font=("Segoe UI", 11)
)

address_entry.pack(
    padx=20,
    pady=5,
    fill="x",
    ipady=3
)

button_font = ("Segoe UI", 11)

tk.Button(
    left,
    text="Add Contact",
    bg="#3d6fc1",
    fg="white",
    font=button_font,
    command=add_contact
).pack(padx=20, pady=10, fill="x")

tk.Button(
    left,
    text="Update Contact",
    bg="#8b5cf6",
    fg="white",
    font=button_font,
    command=update_contact
).pack(padx=20, pady=10, fill="x")

tk.Button(
    left,
    text="Delete Contact",
    bg="#ef4444",
    fg="white",
    font=button_font,
    command=delete_contact
).pack(padx=20, pady=10, fill="x")

tk.Button(
    left,
    text="Clear Fields",
    bg="#78716c",
    fg="white",
    font=button_font,
    command=clear_fields
).pack(padx=20, pady=10, fill="x")

tk.Button(
    left,
    text="Call Contact",
    bg="#22c55e",
    fg="white",
    font=button_font,
    command=call_contact
).pack(padx=60, pady=5, fill="x")

tk.Button(
    left,
    text="Message Contact",
    bg="#06b6d4",
    fg="white",
    font=button_font,
    command=message_contact
).pack(padx=60, pady=5, fill="x")

right = tk.Frame(root, bg="#83004f")

right.pack(
    side="right",
    expand=True,
    fill="both"
)

header = tk.Frame(right, bg="#83004f")

header.pack(
    fill="x",
    padx=15,
    pady=10
)

tk.Label(
    header,
    text="VIEW ALL CONTACTS",
    bg="#83004f",
    fg="white",
    font=("Segoe UI", 11, "bold")
).pack(side="left")

search_entry = tk.Entry(
    header,
    width=30,
    font=("Segoe UI", 11)
)
search_entry.pack(side="right", ipady=3)
search_entry.bind("<KeyRelease>", search_contact)
style = ttk.Style()
style.theme_use("default")
style.configure(
    "Treeview",
    background="#fcbce2",
    foreground="black",
    rowheight=28,
    fieldbackground="#fcbce2"
)
style.configure(
    "Treeview.Heading",
    background="#83004f",
    foreground="white"
)

columns = (
    "No.",
    "Name",
    "Phone Number",
    "Address"
)

table = ttk.Treeview(
    right,
    columns=columns,
    show="headings",
    height=20
)

for column in columns:
    table.heading(column, text=column)

table.column("No.", width=50, anchor="center")
table.column("Name", width=220)
table.column("Phone Number", width=180)
table.column("Address", width=300)

table.pack(
    padx=15,
    pady=10,
    fill="both",
    expand=True
)

table.bind("<<TreeviewSelect>>", on_select)

status_label = tk.Label(
    right,
    text="",
    bg="#83004f",
    fg="#ffc2ee",
    font=("Segoe UI", 9)
)

status_label.pack(
    side="bottom",
    anchor="w",
    padx=15,
    pady=5
)

refresh_table()
root.mainloop()

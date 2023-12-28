import tkinter as tk
from tkinter import messagebox
from datetime import date
import mysql.connector

def show_help():
    help_text = """
    Welcome to KinokunIra Membership Registration!

    Please fill in the following information:
    - Name: Your full name.
    - Date of Birth (YYYY-MM-DD): Your date of birth in the specified format.
    - Email (xxx@xxx.xxx): Your email address.
    - Phone number (+60 only): Your phone number, which must start with '60', as this membership is only valid for Malaysians.

    After filling in the details, click the 'Register' button to complete the registration.

    If you encounter any issues, reach out to our support team on either of these contacts below.
    
    Phone number: +601133228274
    e-mail: kinokunira@gmail.com

    Thank you for choosing KinokunIra!
    """

    messagebox.showinfo("Help", help_text)

def register_member():
    name = entry_name.get()
    dob = entry_dob.get()
    email = entry_email.get()
    phone = entry_phone.get()

    # Convert dob to date and calculate age
    try:
        dob_date = date.fromisoformat(dob)
        age = (date.today() - dob_date).days // 365
    except ValueError:
        messagebox.showerror("Error", "Invalid Date of Birth format.")
        return
    
    # Validate input
    if not name or not dob or not email or not phone:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    elif not phone.startswith("60") or not phone[2:].isdigit():
        messagebox.showerror("Invalid", "Phone number must start with '60' and contain only numeric values.")
        return
    
    else:
        # Display registration information
        registration_info = f"Name: {name}\nAge: {age}\nEmail: {email}\nPhone number: {phone}"
        messagebox.showinfo("Registration Successful", registration_info)
        print("Registration Successful!")
        print("Name:", name)
        print("Age:", age)
        print("Email:", email)
        print("Phone:", phone)

    # Establish a connection to the MySQL server
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ira_membership"
    )

    # Create a cursor object to interact with the database
    cursor = mydb.cursor()

    # Inserting data into a table
    sql = "INSERT INTO `user info` (user_name, user_dob, user_age, user_email, user_phone) VALUES (%s, %s, %s, %s, %s)"
    val = (name, dob, age, email, phone)

    try:
        cursor.execute(sql, val)
        mydb.commit()
        print("Data inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

    cursor.close()
    mydb.close()

def quit_application():
    root.destroy()

# Create the main window
root = tk.Tk()

# Set window title
root.title("Book Shop Membership Registration")

# Set the window size and position
root.geometry("800x600+400+300")

# Set background color
root.configure(bg="#F5CEF2")

# Create and configure the labels
label_title = tk.Label(root, text="Welcome to KinokunIra!", font=("Times New Roman", 50, 'bold'))
label_subtitle = tk.Label(root, text="Register for a membership card now to get a discount!", font=('Times New Roman', 25))
label_name = tk.Label(root, text="Name:", font=("Arial", 15), bg="#f0f0f0")
label_email = tk.Label(root, text="Email (xxx@xxx.xxx):", font=("Arial", 15), bg="#f0f0f0")
label_phone = tk.Label(root, text="Phone number (+60 only):", font=("Arial", 15), bg="#f0f0f0")
label_dob = tk.Label(root, text="Date of birth (YYYY-MM-DD):", font=("Arial", 15), bg="#f0f0f0")

# Create and configure the entry widgets
entry_name = tk.Entry(root, font=("Arial", 12), width=30)
entry_email = tk.Entry(root, font=("Arial", 12), width=30)
entry_phone = tk.Entry(root, font=("Arial", 12), width=30)
entry_dob = tk.Entry(root, font=("Arial", 12), width=30)

# Create and configure the register button
register_button = tk.Button(root, text="Register", command=register_member, font=("Arial", 12), bg="#84e0b3", fg="black")

# Create and configure the quit button
quit_button = tk.Button(root, text="Quit application", command=quit_application, font=("Arial", 12), bg="#d9534f", fg="white")

# Create and configure the help button
help_button = tk.Button(root, text="Help", command=show_help, font=("Arial", 12), bg="#5bc0de", fg="black")

# Place the buttons on the window
register_button.place(relx=0.8, rely=0.9)
quit_button.place(relx=0.1, rely=0.9)
help_button.place(relx=0.03, rely=0.9)

# Place the labels, entry widgets, and button on the window using pack and place
label_title.pack(pady=10)
label_subtitle.pack(pady=20)
label_name.pack(pady=10)
entry_name.pack(pady=10)
label_email.pack(pady=10)
entry_email.pack(pady=10)
label_phone.pack(pady=10)
entry_phone.pack(pady=10)
label_dob.pack(pady=10)
entry_dob.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

'''
Financial Assistant Application | ITERATION 4
George R
AUG 2024
'''

import customtkinter as ctk# replacement for tkinter - custom version provides more customization, better GUI
import json # json file imported to be able to write/read for passwords an usernames
from PIL import Image # for the use of images in my code
import os # used to restart the application when user clicks log out
from CTkSpinbox import * # custom tikinter spin box 
import sys# used to restart the application when user clicks log out
import matplotlib.pyplot as plt# imporitng for GUI graph for spending tracker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# imporitng for GUI graph for spending tracker
from datetime import datetime, timedelta# imporitng for GUI graph for spending tracker
import calendar # imporitng for GUI graph for spending tracker
import google.generativeai as genai # google gemini API used for the AI section of my app
import tkinter as tk # used for gui 
import awesometkinter # used for progress bar
import ttkbootstrap as ttkb # used for my calendar

logged_in_user = None  # keeps track of the currently logged-in user

# Load users from a json file
def load_users():
    with open("iteration 4/users.json", "r") as file:
        return json.load(file)

# save user data back into the json file
def save_users(users):
    with open("iteration 4/users.json", "w") as file:
        json.dump(users, file, indent=4)

# function to deal with user login
def login():  
    username = username_entry.get()  # get username from entry field
    password = password_entry.get()  # get password from entry field
    users = load_users()

    # Validate credentials and load the spend tracker on successful login
    if username in users and users[username]["password"] == password:
        global logged_in_user
        logged_in_user = username
        login_frame.grid_forget()  
        show_spend_tracker() 
    else:
        # show error if login fails
        error_label.configure(text="Invalid username or passwiord. Please try again.")

# display the login screen
def show_login_screen():
    login_content.grid(row=1, column=0, sticky="ns")

# show the account creation screen
def show_create_account():
    login_content.grid_forget()
    create_account_content.grid(row=1, column=0, sticky="ns")

# Handle the account creation process
def create_account():
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()
    users = load_users()

    # make sure that both username and password are provided
    if not new_username or not new_password:
        create_account_error_label.configure(text="Please enter both username and password.")
        return

    # check if the username already exists
    if new_username in users:
        create_account_error_label.configure(text="Username already exists. Please choose another.")
        return

    # Add the new user with normal settings
    users[new_username] = {"password": new_password, "spending_history": [], "saving_goal": 0, "progress": 0}
    save_users(users)

    # show the login screen after successful account creation
    create_account_content.grid_forget()
    login_content.grid(row=1, column=0, sticky="ns")
    success_label.configure(text="Account created successfully. Please log in.")

# Save the user's financial goal in the json file
def save_goal(goal_amount):
    users = load_users()
    if logged_in_user not in users:
        users[logged_in_user] = {"spending_history": [], "saving_goal": 0, "progress": 0}
    users[logged_in_user]["saving_goal"] = goal_amount
    users[logged_in_user]["progress"] = 0  # reset progress when a new goal is set
    save_users(users)

# Update saving progress in the json file and return the percentage of progress
def update_progress(saved_amount):
    users = load_users()
    goal = users[logged_in_user].get("saving_goal", 0)
    if goal > 0:
        progress = (saved_amount / goal) * 100
        users[logged_in_user]["progress"] = progress
        save_users(users)
        return progress
    return 0

# Set up the main window of the application
window = ctk.CTk()
window.title("xCel Finance | Financial Application")
window.geometry("1920x1080")
window.configure(fg_color="#F3E4F6")

# Grid configuration for window layout
window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

# image frame for displaying logo
image_frame = ctk.CTkFrame(window, fg_color="white", corner_radius=20)
image_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

# display the application logo
image = ctk.CTkImage(Image.open("iteration 4/diplogo.png"), size=(800, 342))
image_label = ctk.CTkLabel(image_frame, image=image, text="")
image_label.pack(fill="both", expand=True, padx=10, pady=10)

# Frame for the login GU Interface
login_frame = ctk.CTkFrame(window, fg_color="#d096dc", corner_radius=20)
login_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
login_frame.grid_rowconfigure(0, weight=1)
login_frame.grid_rowconfigure(6, weight=1)
login_frame.grid_columnconfigure(0, weight=1)

# content for the login form
login_content = ctk.CTkFrame(login_frame, fg_color="transparent")
login_content.grid(row=1, column=0, sticky="ns")

# title for the login section
title_label = ctk.CTkLabel(login_content, text="Ready to accelerate your\npersonal finance story?", font=("Arial", 24, "bold"), text_color="white")
title_label.pack(pady=(0, 30))

# Username and password entry
username_label = ctk.CTkLabel(login_content, text="Username:", text_color="white")
username_label.pack(pady=(0, 5))
username_entry = ctk.CTkEntry(login_content, width=200)
username_entry.pack(pady=(0, 20))

password_label = ctk.CTkLabel(login_content, text="Password:", text_color="white")
password_label.pack(pady=(0, 5))
password_entry = ctk.CTkEntry(login_content, width=200, show="*")
password_entry.pack(pady=(0, 20))

# log in and account creation buttons
login_button = ctk.CTkButton(login_content, text="Log In", text_color="#208ad6", hover_color="#CFCFCF", fg_color="white", command=login)
login_button.pack(pady=(0, 20))

create_account_button = ctk.CTkButton(login_content, text="Create Account", command=show_create_account)
create_account_button.pack()

# labels for displaying error or success messages
error_label = ctk.CTkLabel(login_content, text="", text_color="red")
error_label.pack(pady=(10, 0))

success_label = ctk.CTkLabel(login_content, text="", text_color="white")
success_label.pack(pady=(10, 0))

# content for creating a new account
create_account_content = ctk.CTkFrame(login_frame, fg_color="transparent")

# Title for the account creation section
create_account_title = ctk.CTkLabel(create_account_content, text="Create a new account", font=("Arial", 24, "bold"), text_color="white")
create_account_title.pack(pady=(0, 30))

# Username and password entry fields
new_username_label = ctk.CTkLabel(create_account_content, text="New Username:", text_color="white")
new_username_label.pack(pady=(0, 5))
new_username_entry = ctk.CTkEntry(create_account_content, width=200)
new_username_entry.pack(pady=(0, 20))

new_password_label = ctk.CTkLabel(create_account_content, text="New Password:", text_color="white")
new_password_label.pack(pady=(0, 5))
new_password_entry = ctk.CTkEntry(create_account_content, width=200, show="*")
new_password_entry.pack(pady=(0, 20))

# Button for new account
create_button = ctk.CTkButton(create_account_content, text="Create Account", command=create_account)
create_button.pack(pady=(0, 20))

# back button
back_to_login_button = ctk.CTkButton(create_account_content, text="Back to Login", command=lambda: (create_account_content.grid_forget(), login_content.grid(row=1, column=0, sticky="ns")))
back_to_login_button.pack()

# error label   
create_account_error_label = ctk.CTkLabel(create_account_content, text="", text_color="red")
create_account_error_label.pack(pady=(10, 0))

# function to restart the app
def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Log out function that destroys the window and restarts the app
def logout():
    window.destroy()
    restart_app()

# Function to quit the app
def quitapp():
    quit()

# Settings function for various options 
def settings():
    def confirm_deletion():
        users = load_users()
        if logged_in_user in users:
            del users[logged_in_user]  # remove user from the list
            save_users(users)
            delete_window.destroy()  # close the settings
            logout()  # log out after deletion

    def switch_theme():
        # toggle between light and dark mode
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    # create a pop up window for settings
    delete_window = ctk.CTkToplevel(window)
    delete_window.title("Settings")
    delete_window.geometry("300x200")

    # button to switch the theme of the application
    theme_button = ctk.CTkButton(delete_window, text="Switch Theme", command=switch_theme)
    theme_button.pack(pady=10)

    # Label and button for confirming account deletion
    ctk.CTkLabel(delete_window, text="Delete Account", wraplength=250).pack(pady=10)
    confirm_button = ctk.CTkButton(delete_window, text="Confirm Deletion", fg_color="red", text_color="white", command=confirm_deletion)
    confirm_button.pack(padx=20, pady=10)

    # Button to close
    cancel_button = ctk.CTkButton(delete_window, text="Close Settings", command=delete_window.destroy)
    cancel_button.pack(padx=20, pady=10)
# Create a top bar 
def create_top_bar(parent):
    top_bar = ctk.CTkFrame(parent, height=60, fg_color="#d096dc") 
    top_bar.pack(side="top", fill="x")  # make top bar stretch across the window
    top_bar.pack_propagate(False)  # Fix height of bar

    # fix logo to fit within the top bar
    logo = ctk.CTkImage(Image.open("iteration 4/diplogo.png"), size=(150, 64))
    logo_label = ctk.CTkLabel(top_bar, image=logo, text="")
    logo_label.pack(side="left", padx=10)  # align logo to the left side

# sidebar with navigation 
def create_sidebar(parent):
    sidebar = ctk.CTkFrame(parent, fg_color="#F3E4F6", width=150)  # sidebar with fixed width
    sidebar.pack(side="left", fill="y", pady=(0, 0))  # sidebar spans the height of the window

    button_color = "#d096dc"  # sidebar button color
    button_text_color = "white"

    # settings button with an image icon
    set_button_image = ctk.CTkImage(Image.open("iteration 4/settings.png"), size=(140, 99))
    set_button = ctk.CTkButton(master=sidebar, image=set_button_image, text="", fg_color="transparent", hover=False, command=settings)
    set_button.pack(fill="x")

    # logout and quit buttons with padding
    logout_button = ctk.CTkButton(master=sidebar, text="Log Out", command=logout, fg_color="white", text_color="black", hover_color="#d9b1e0")
    logout_button.pack(pady=(20, 10), fill="x")

    quit_button = ctk.CTkButton(master=sidebar, text="Quit", command=quitapp, fg_color="red", text_color="black", hover_color="#d9b1e0")
    quit_button.pack(pady=10, fill="x")

    # spacer between buttons
    gap = ctk.CTkLabel(master=sidebar, text="")
    gap.pack(pady=25)

    # spend tracker button
    spend_button = ctk.CTkButton(master=sidebar, text="Spend Tracker", command=show_spend_tracker, fg_color=button_color, text_color=button_text_color, hover_color="#d9b1e0")
    spend_button.pack(pady=5, fill="x")

    # finance school button
    school_button = ctk.CTkButton(master=sidebar, text="Finance School", command=show_school_frame, fg_color=button_color, text_color=button_text_color, hover_color="#d9b1e0")
    school_button.pack(pady=5, fill="x")

    # AI button
    ai_button = ctk.CTkButton(master=sidebar, text="xCel AI Assistant", command=show_ai_chat, fg_color=button_color, text_color=button_text_color, hover_color="#d9b1e0")
    ai_button.pack(pady=5, fill="x")

# show the spending tracker screen
def show_spend_tracker():
    for widget in window.winfo_children():
        widget.destroy()  # clear content from the window

    create_top_bar(window)  # add the top bar
    create_sidebar(window)  # add the sidebar

    # main content area for the spend tracker
    content_frame = ctk.CTkFrame(window)
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    spend_tracker = SpendTracker()  # create an instance of the spend tracker class
    spend_tracker.add_item(content_frame)  # add spend tracker elements to the content frame

# show the ai chat interface
def show_ai_chat():
    for widget in window.winfo_children():
        widget.destroy()  # clear window content
    create_top_bar(window)
    create_sidebar(window)

    # main content area for AI chat
    content_frame = ctk.CTkFrame(window)
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    AIChat(content_frame)  # call the class 

# show the finance school interface
def show_school_frame():
    for widget in window.winfo_children():
        widget.destroy()  # clear window content
    create_top_bar(window)
    create_sidebar(window)

    # Main content area for finance school
    content_frame = ctk.CTkFrame(window)
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    SchoolFrame(content_frame)  # finance school class

# spending tracker
class SpendTracker:
    def __init__(self):
        # list of spending categories
        self.cat_list = [
            "Food", "Technology", "Entertainment", "Groceries", "Medical",
            "Petrol", "Travel", "Clothing", "Utilities", "Education",
            "Fitness", "Subscriptions", "Gifts", "Personal Care",
            "Other (wants)", "Other (needs)"
        ]
        self.items = []  # List to store spending items

    def add_item(self, parent_frame):
        # main container for the two rectangles
        container_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        container_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # adjust grid configuration for the container to fill entire width
        container_frame.grid_columnconfigure(0, weight=3)
        container_frame.grid_columnconfigure(1, weight=1) 
        container_frame.grid_rowconfigure(0, weight=1)  # festrict the height of the content

        # left frame for item and input spending history and chart
        left_frame = ctk.CTkFrame(container_frame, fg_color="white", corner_radius=20)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        # right frame for financial goals
        right_frame = ctk.CTkFrame(container_frame, fg_color="white", corner_radius=20)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        # configure left frame rows and columns to control widget resizing
        left_frame.grid_rowconfigure(2, weight=1)  
        left_frame.grid_columnconfigure(0, weight=1)

        # left Frame Contents
        input_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.p_name = ctk.CTkEntry(input_frame, width=200)
        self.p_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Category:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.p_cat = ctk.CTkComboBox(input_frame, values=self.cat_list, width=200)
        self.p_cat.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.p_price = tk.Spinbox(input_frame, from_=0, to=100000, increment=1.0, width=10)
        self.p_price.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # second row is calendar and spending history
        display_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        display_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # date picker
        ctk.CTkLabel(display_frame, text="Select Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.p_date = ttkb.DateEntry(display_frame, bootstyle="primary", dateformat="%d/%m/%Y")
        self.p_date.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nw")

        # submit button
        self.p_submit = ctk.CTkButton(display_frame, text="Submit", command=self.submit_item)
        self.p_submit.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="nw")

        # spending history text
        ctk.CTkLabel(display_frame, text="Spending History:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.display_area = ctk.CTkTextbox(display_frame, height=150, width=300)
        self.display_area.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.display_text()

        # button to clear history
        self.clear_button = ctk.CTkButton(display_frame, text="Clear History", command=self.clear_history)
        self.clear_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # monthly spending chart
        ctk.CTkLabel(left_frame, text="Spending Chart (Last 12 Months):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.create_spending_chart(left_frame)

        #  right Frame Contents for financial goals
        ctk.CTkLabel(right_frame, text="Financial Goals", font=("Arial", 18)).pack(pady=10)

        ctk.CTkLabel(right_frame, text="Enter Saving Goal:").pack(pady=5)
        self.goal_spinbox = tk.Spinbox(right_frame, from_=0, to=1000000, increment=1, width=10)
        self.goal_spinbox.pack(pady=10)

        self.set_goal_button = ctk.CTkButton(right_frame, text="Set Saving Goal", command=self.set_goal)
        self.set_goal_button.pack(pady=10)

        ctk.CTkLabel(right_frame, text="Enter Saved Amount:").pack(pady=5)
        self.saved_amount_spinbox = tk.Spinbox(right_frame, from_=0, to=1000000, increment=1, width=10)
        self.saved_amount_spinbox.pack(pady=10)

        self.update_progress_button = ctk.CTkButton(right_frame, text="Update Progress", command=self.update_saving_progress)
        self.update_progress_button.pack(pady=10)

        self.progressbar = awesometkinter.RadialProgressbar(right_frame, fg='green', parent_bg="white", bg="white", size=(130,130))
        self.progressbar.pack(padx=20, pady=10)

        # label to display the current saving goal amount
        self.goal_label = ctk.CTkLabel(right_frame, text=f"Current Saving Goal: $0.00", text_color="black")
        self.goal_label.pack(pady=5)

        users = load_users()
        user_data = users.get(logged_in_user, {})
        saved_progress = user_data.get("progress", 0)
        saving_goal = user_data.get("saving_goal", 0)
        self.progressbar.set(saved_progress)
        self.goal_label.configure(text=f"Current Saving Goal: ${saving_goal:.2f}")

    # function to clear spending history
    def clear_history(self):
        users = load_users()
        users[logged_in_user]["spending_history"] = []  # Clear the history
        save_users(users)
        self.display_text()  # Refresh the display area
        self.create_spending_chart(self.parent_frame)  # Update the chart

    # function to set the saving goal
    def set_goal(self):
        goal_amount = float(self.goal_spinbox.get())
        save_goal(goal_amount)
        self.progressbar.set(0)
        self.goal_label.configure(text=f"Current Saving Goal: ${goal_amount:.2f}")

    # update saving progress
    def update_saving_progress(self):
        saved_amount = float(self.saved_amount_spinbox.get())
        progress = update_progress(saved_amount)
        self.progressbar.set(progress)

    # function to submit a spending item
    def submit_item(self):
        name = self.p_name.get()
        category = self.p_cat.get()
        price = float(self.p_price.get())
        date = self.p_date.entry.get()  # get selected date

        new_item = {"name": name, "category": category, "price": price, "date": date}

        users = load_users()
        users[logged_in_user]["spending_history"].append(new_item)  # save to the users spending history
        save_users(users)

        self.display_text()
        self.create_spending_chart(self.parent_frame)  # update chart

    # display spending history
    def display_text(self):
        self.display_area.delete('1.0', "end")  # clear existing text
        users = load_users()
        spending_history = users.get(logged_in_user, {}).get("spending_history", [])

        for item in spending_history:
            display_str = f"{item['name']}, {item['category']}, {item['price']}, {item['date']}\n"
            self.display_area.insert("end", display_str)

    # create spending chart
    def create_spending_chart(self, parent_frame):
        spending_data = self.read_spending_data()  # get spending data from the logged in user

        fig, ax = plt.subplots(figsize=(6, 2.5))  # smaller and less wide chart

        if spending_data:
            monthly_spending = {month: 0 for month in range(1, 13)}

            for date, amount in spending_data:
                monthly_spending[date.month] += amount

            months = list(calendar.month_abbr)[1:]  # month abbreviations e.g jan etc 
            spending_values = [monthly_spending[month] for month in range(1, 13)]

            bars = ax.bar(months, spending_values)

            ax.set_xlabel("Month")
            ax.set_ylabel("Amount Spent ($)")
            ax.set_title("Monthly Spending")

            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height, f"${height:.2f}", ha="center", va="bottom")

            plt.xticks(rotation=45)

        else:
            ax.text(0.5, 0.5, "No spending data available", horizontalalignment="center", verticalalignment="center")

        plt.tight_layout()

        # use grid for the chart canvas
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        canvas.draw()

    # read spending data from the users history
    def read_spending_data(self):
        spending_data = []  # list to store spending data
        today = datetime.now()
        start_of_year = datetime(today.year, 1, 1)

        users = load_users()
        user_spending_history = users.get(logged_in_user, {}).get("spending_history", [])

        for item in user_spending_history:
            try:
                # first try dmy
                try:
                    date = datetime.strptime(item["date"], "%d/%m/%Y")
                except ValueError:
                    # accept mdy
                    date = datetime.strptime(item["date"], "%m/%d/%y")

                price = float(item["price"])

                if date >= start_of_year:
                    spending_data.append((date, price))

            except ValueError as e: # error handilling
                print("error")
            except KeyError:
                print("error")
            except Exception as e:
                print("error")

        spending_data.sort(key=lambda x: x[0])
        return spending_data

# class for ai chat interface
class AIChat:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_ai_chat_frame()

    def create_ai_chat_frame(self):
        frame = ctk.CTkFrame(self.parent_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        os.environ["GENERATIVE_AI_KEY"] = "XXXXXXXXXXXXXXX"  # google gemini key
        genai.configure(api_key=os.getenv("GENERATIVE_AI_KEY"))

        # Configure the AI model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
        )
        self.chat_session = self.model.start_chat(history=[])  # start new chat with AI

        ctk.CTkLabel(frame, text="Enter your question:").pack(anchor="w", pady=(0, 5))
        self.question_entry = ctk.CTkEntry(frame, width=500)
        self.question_entry.pack(fill="x", pady=(0, 10), padx=(0, 10))

        submit_button = ctk.CTkButton(frame, text="Submit", command=self.send_question)
        submit_button.pack(pady=(0, 10))

        ctk.CTkLabel(frame, text="Chat History:").pack(anchor="w", pady=(0, 5))
        self.response_text = ctk.CTkTextbox(frame, height=400, width=700)
        self.response_text.pack(fill="both", expand=True, pady=(0, 10))

    def send_question(self):
        question = self.question_entry.get()
        if question:
            response = self.chat_session.send_message(question)
            self.response_text.insert("end", f"Q: {question}\n\nA: {response.text}\n\n")
            self.question_entry.delete(0, "end")


# class for managing the finance school interface
class SchoolFrame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_school_frame()

    def create_school_frame(self):
        main_frame = ctk.CTkFrame(self.parent_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=(10, 5))

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.content_text = ctk.CTkTextbox(content_frame, wrap="word", width=600, height=400)
        self.content_text.pack(fill="both", expand=True, padx=10, pady=10)

        topics = ["Learn about budgeting", "When to save/spend", "What is investing?", "How to track spending?", "Summary"]
        for topic in topics:
            ctk.CTkButton(button_frame, text=topic, command=lambda t=topic: self.show_content(t), width=180).pack(side="left", padx=5)

        self.show_content("Learn about budgeting")

    def show_content(self, topic):
        self.content_text.delete("1.0", "end")
        file_path = "iteration 4/scl1.txt"
        try:
            with open(file_path, "r") as file:
                all_content = file.read().split('\n\n\n\n')
                topic_dict = {"Learn about budgeting": 0, "When to save/spend": 1, "What is investing?": 2, "How to track spending?": 3, "Summary": 4}
                if topic in topic_dict:
                    self.content_text.insert("end", all_content[topic_dict[topic]])  # display content
                else:
                    self.content_text.insert("end", "Topic not found")
        except FileNotFoundError:
            self.content_text.insert("end", "File not found")

# Start the application 
if __name__ == "__main__":
    window.mainloop()  # Start the window loop

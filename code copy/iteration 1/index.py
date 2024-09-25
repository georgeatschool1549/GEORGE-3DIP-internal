
'''
Financial Assistant Application | ITERATION 1
George R
July 2024
'''

from easygui import * 
import openpyxl
import pandas as pd
import os

'''
All of the above imports neccassary modules to use external functions. 
E.G.: easy gui allows me to turn a text base code into a Graphical User Interface (GUI). 
'''

class SpendTracker: # Classes makes it possible for the user to enter any variable and run through the method - the user can choose a different variable and it will run throught the same methods. 
    def __init__(self): # The initiate (__init__) function asigns values to objects
        self.cat_list = [ # List of catagories
            "Food", "Technology", "Entertainment", "Groceries", "Medical",
            "Petrol", "Travel", "Clothing", "Utilities", "Education", 
            "Fitness", "Subscriptions", "Gifts", "Personal Care", 
            "Other (wants)", "Other (needs)"
        ]
        self.items = [] # Calling the items lists

    def add_item(self): # Function to add the information entered by the user into the item list. 
        while True: # While true code ensures that the user enters the information, and if they dont, thew programme breakes.
            p_name = enterbox("Name of Product") # assigns the enterybox a variable. 
            if not p_name: # If no information is entered, the programme will break.
                break

            p_cat = choicebox("Select category", "Select Category", self.cat_list) # list of choices avalible for the user to pick. 
            if not p_cat:
                break

            p_price = enterbox("Price of Product")
            if not p_price:
                break

            p_date = enterbox("Date")
            if not p_date:
                break
            
            self.items.append([p_name, p_cat, p_price, p_date]) # Appendds the items entered from the user and assigns it to the above function. 

            more = choicebox("Would you like to track another purchase?", "Select an option", ["Yes", "No"]) # Option for the user for if they want to enter another option or not.
            if more != "Yes":
                break

    def save_items(self): # Function to save entries into the Excel file. This is by using OpenPYXL (stated at the start of the code)
        workbook = openpyxl.load_workbook("iteration 1/spending.xlsx") #Opens and activates excel sheet
        sheet = workbook.active

        for item in self.items: # for the number or items in the list it will write the into the worksheet. 
            sheet.append(item)
            
        workbook.save("iteration 1/spending.xlsx")

    def display_sheet(self): # displays the excel work sheet. 
        df = pd.read_excel("iteration 1/spending.xlsx") # pd is external module and df is Data Frame - this is to call the information (in var) from the excel sheet
        msgbox(df.to_string(index=False), "Spending Tracker") #msgbox displays the info by callling the above var, setting the parameter as false, and naming the frame as spending tracker

def main(): # main function - 
    tracker = SpendTracker()
    tracker.add_item()
    tracker.save_items()
    tracker.display_sheet()

if __name__ == "__main__": # Calls the main function
    main()
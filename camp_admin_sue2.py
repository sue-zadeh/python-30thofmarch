# ============== Selwyn Campground MAIN PROGRAM ==============
# Student Name: Sue Raisianzadeh
# Student ID : 1161048
# NOTE: Make sure your two files are in the same folder
# =================================================================================

import camp_data    # camp_data.py MUST be in the SAME FOLDER as this file!
                    # camp_data.py contains the data
import datetime     # We are using date times for this assessment, and it is
                    # available in the column_output() function, so do not delete this line

# Data variables
#col variables contain the format of each data column and help display headings
#db variables contain the actual data
col_customers = camp_data.col_customers
db_customers = camp_data.db_customers
col_bookings = camp_data.col_bookings
db_bookings = camp_data.db_bookings
UNPS = camp_data.UNPS #list of unpowered sites
PS = camp_data.PS #list of powered sites


def next_id(db_data):
    #Pass in the dictionary that you want to return a new ID number for, this will return a new integer value
    # that is one higher than the current maximum in the list.
    return max(db_data.keys())+1

def column_output(db_data, cols, format_str):
    # db_data is a list of tuples.
    # cols is a dictionary with column name as the key and data type as the item.
    # format_str uses the following format, with one set of curly braces {} for each column:
    #   eg, "{: <10}" determines the width of each column, padded with spaces (10 spaces in this example)
    #   <, ^ and > determine the alignment of the text: < (left aligned), ^ (centre aligned), > (right aligned)
    #   The following example is for 3 columns of output: left-aligned 5 characters wide; centred 10 characters; right-aligned 15 characters:
    #       format_str = "{: <5}  {: ^10}  {: >15}"
    #   Make sure the column is wider than the heading text and the widest entry in that column,
    #       otherwise the columns won't align correctly.
    # You can also pad with something other than a space and put characters between the columns, 
    # eg, this pads with full stops '.' and separates the columns with the pipe character '|' :
    #       format_str = "{:.<5} | {:.^10} | {:.>15}"
    print(format_str.format(*cols))
    for row in db_data:
        row_list = list(row)
        for index, item in enumerate(row_list):
            if item is None:      # Removes any None values from the row_list, which would cause the print(*row_list) to fail
                row_list[index] = ""       # Replaces them with an empty string
            elif isinstance(item, datetime.date):    # If item is a date, convert to a string to avoid formatting issues
                row_list[index] = str(item)
        print(format_str.format(*row_list))


def list_customers():
    # List the ID, name, telephone number, and email of all customers

    # Use col_Customers for display
   
    # Convert the dictionary data into a list that displays the required data fields
    #initialise an empty list which will be used to pass data for display
    display_list = []
    #Iterate over all the customers in the dictionary
    for customer in db_customers.keys():
        #append to the display list the ID, Name, Telephone and Email
        display_list.append((customer,
                             db_customers[customer]['name'],
                             db_customers[customer]['phone'],
                             db_customers[customer]['email']))
    format_columns = "{: >4} | {: <18} | {: <15} | {: ^12}"
    print("\nCustomer LIST\n")    # display a heading for the output
    column_output(display_list, col_customers, format_columns)   # An example of how to call column_output function

    input("\nPress Enter to continue.")     # Pauses the code to allow the user to see the output



def list_campsites():
    # List the ID, name, occupancy
    print("\n=== Camp Sites ===")
    print("\nUnpowered Sites:")
    # max occupancy for unpowered sites
    print("{:<10} |{:<15}" .format("Site ID", "Max Occupancy"))
    for site in UNPS:
      print("{:<10} |{:<15}" .format(site[0], site[1])) 
    print("\nPowered Sites:") 
    # max occupancy for powered sites 
    print("{:<10} |{:<15}" .format("Site ID", "Max Occupancy"))
    for site in UNPS:
      print("{:<10} |{:<15}" .format(site[0], site[1])) 
    
    

def list_campers_by_date():  
    # List the Date, name, site, occupancy
    print("\n=== List campers by date ===")
    #date input and validate
    date_input = input("Enter a date (YYYY-MM-DD): ")
    try:
      specific_day = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
      print("Invalid date format. Please enter date as YYYY-MM-DD")
      return  
    
    # check the date is valid
    if specific_day not in db_bookings:
      print(f'No booking found for {specific_day}')
      return
    #booking for the specific day
    bookings = db_bookings[specific_day]
    unpowered_bookings = bookings[0]
    powered_bookings = bookings[1]
    
    #displying the booking information
    print(f'\nBookings for {specific_day}')
    for booking in unpowered_bookings + powered_bookings:
      site_id, customer_id, num_occupants =booking 
      customer_name = db_customers[customer_id]["name"]
      print(f"Site ID: {site_id}. Customer name: {customer_name}, Occupants: {num_occupants}")
    

def add_customer():
    # Add a customer to the db_customers database, use the next_id to get an id for the customer.
    new_id = next_id(db_customers) 
    
    print("\n=== Add New Customer ===")
    
    # Remember to add all required dictionaries.
    name = input("Enter customer's name: ")
    phone = input("Enter customer's phone number: ")
    email = input("Enter customer's email address: ")
    
    db_customers[new_id] = {'name': name, 'phone': phone, 'email': email}

    print(f"Customer added with ID: {new_id}")

def add_booking():
    
    # Add a booking
    print("\n=== Add Booking ===")
   
    # Remember to validate customer ids and sites
    customer_id = int(input("Enter customer ID: "))
    if customer_id not in db_customers:
       print("Customer ID not found.")
       return
  
   # site type and validate
    site_type = input("Enter site type (U for Unpowered, P for Powered): ").upper()
    if site_type not in ['U', 'P']:
      print("Invalid site type.")
      return
   
    # avalable site based on types
    if site_type == "U":
       sites = UNPS
    else:
      sites = PS  
      print('\nAvalable Sites:') 
    for site in sites:  
      print(f"Site ID: {site[0]}, Max Occupancy: {site[1]}")
    
    # site ID and validate
    site_id = input("Enter site ID: ") 
    if not any(site[0] == site_id for site in sites):
      print("Invalid Site ID") 
      return
    #start date and validate
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    try:
      start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    except ValueError: 
      
     print("Invalid date format")
     return
   
   #number of nights and validate
    num_nights = int(input('Enter number of nights (1-5): '))
    # between 1 and 5
    if not 1 <= num_nights <= 5:
      print('Invalid number of nights. please enter a value between 1-5')
      return
    
   # add booking for each night
    for i in range(num_nights):
     booking_date = start_date + datetime.timedelta(days=i) 
     if booking_date not in db_bookings:
       db_bookings[booking_date] =[[], []]
       booking_list_index = 0 if site_type == 'U' else 1
       db_bookings[booking_date][booking_list_index].append((site_id, customer_id, num_nights))
    print("Booking added Successfully")
      
      
# function to modify booking
def modify_booking():
  print("\n=== Modify Booking ===")
  original_date = input("Enter original booking date (YYYY-MM-DD): ")
  try:
    original_date = datetime.datetime.strptime(original_date, "%Y-%m-%d").date()
  except ValueError:
    print("Invalid date format. Please enter date as YYYY-MM-DD") 
    return
  if original_date not in db_bookings:
    print(f"No booking found for {original_date}")
    return
  
  site_id = input("Enter the original site ID:").upper()
  # to change the date and site id of the booking
  new_date_input = input("Enter new booking date (YYYY-MM-DD): ")
  try:
    new_date_input = datetime.datetime.strptime(new_date_input, "%Y-%m-%d").date()
  except ValueError:
    print("Invalid date format. Please enter date as YYYY-MM-DD")
    return
  
  new_site_id = input("Enter the new site ID:").upper()
  # check booking validation and modifying the booking
  booking_modified = False
  for bookings in db_bookings[original_date]:
    for i, booking in enumerate(bookings):
      if booking[0] == site_id:
        customer_id, occupants = booking[1], booking[2]
        bookings.pop(i)  # remove the original booking
        booking_modified = True
        break
      if booking_modified:
        break
      if not booking_modified:
        print("Original booking not found")
        return
      
      # add the new booking
if new_date not in db_bookings:
  db_bookings[new_date] = [[], []]
  new_booking_list = db_bookings[new_date][0] if new_site_id.startswith('U') else  db_bookings[new_date][1]
  new_booking_list.append((new_site_id, custom_id, occupants))
  
  print("Booking modified successfully")
    
  

# function to display the menu
def disp_menu():
    print("==== WELCOME TO SELWYN CAMPGROUND ===")
    print(" 1 - List Customers")
    print(" 2 - List Campsites")
    print(" 3 - List Campers (Specific Date")
    print(" 4 - Add Customer")
    print(" 5 - Add Booking")
    print(" 6 - Modify Booking")
    print(" X - eXit (stops the program)")


# ------------ This is the main program ------------------------

# Display menu for the first time, and ask for response
disp_menu()
response = input("Please enter menu choice: ")

# Don't change the menu numbering or function names in this menu
# Repeat this loop until the user enters an "X"
while response.upper() != "X":
    if response == "1":
        list_customers()
    elif response == "2":
        list_campsites()
    elif response == "3":
        list_campers_by_date()
    elif response == "4":
        add_customer()
    elif response == "5":
        add_booking()
    else:
        print("\n***Invalid response, please try again (enter 1-5 or X)")

    print("")
    disp_menu()
    response = input("Please select menu choice: ")

print("\n=== Thank you for using Selywn Campground Administration! ===\n")

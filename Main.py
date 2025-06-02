from class_file import *

# Creating an instance of the 'bookstore' class.
vanvitelli_bookstore = bookstore('Luigi Vanvitelli')

# Function to start the bookstore application that will immediately shift the user to 'relog' function. 
def run_bookStore():
    print("\nWelcome ! To start with you should login to your account or creat a new account.")
    relog()

#Function to handle user login or registration which is responsible to limit the user to select either between register 
#and login then continues with the related input.
def relog():
    relog_choice = input("\nInput the operation you want to use : (register or login) ").lower()
    
    if relog_choice == "register":
        user_register()
    elif relog_choice == "login":
        user_login()
    else:
        print("You should select either operation Register or Login.")
        relog()

# Function for user login and This function helps users log in. It asks for their email and password, checks if the information is correct, 
#and then guides them to the right menu, whether they're a customer or an employee.
def user_login():

    user_type_log = input("Input the type of user you want to login (Customer/Employee): ")
    while user_type_log.lower() not in ["customer", "employee"]:
        user_type_log = input("Please select and input among Customer/Employee options: ")

    email_login = input("Enter your email: ")
    if user_type_log.lower() == "customer":
        if vanvitelli_bookstore.is_registered_customer(email_login) == True:
            logger_customer = vanvitelli_bookstore.customer_finder(email_login)
            password_login = input("Enter your six digit password: ")
            
            while int(password_login) != int(logger_customer.get_password()):
                password_login = input("Wrong password. Please enter your password: ")
            
            print("Login successfull !")
            return customer_menu(logger_customer)
    
    if user_type_log.lower() == "employee":
        if vanvitelli_bookstore.is_registered_employee(email_login) == True:
            logger_employee = vanvitelli_bookstore.employee_finder(email_login)
            password_login = input("Enter your six digit password: ")
            
            while int(password_login) != int(logger_employee.get_password()):
                password_login = input("Wrong password. Please enter your password: ")
            
            print("Login successfull !")
            return employee_menu(logger_employee)

    print("There are no accounts with this email. Try to Register or Login with another email.")
    return relog()

# Function to check if a given date string is in the correct format
def is_valid_date_format(date_str):
    if len(date_str) == 10 and date_str[4] == date_str[7] == '-':
        date_parts = date_str.split('-')

        if len(date_parts) == 3:

            if date_parts[0].isdigit() and date_parts[1].isdigit() and date_parts[2].isdigit():
                year, month, day = map(int, date_parts)

                if 1890 <= year <= 2024 and 1 <= month <= 12 and 1 <= day <= 31:
                    return True

    return False

# Function to check if a given email is in a valid format
def is_valid_email(email):
    if "@" in email and "." in email:

        if email.index("@") < email.rindex("."):
            return True

    return False

#This function handles the user registration process.It asks the user for information, validates the input, 
#and registers the user as either a customer or employee.
def user_register():
    
    user_type_reg = input("Input the type of user you want to register (Customer/Employee): ")
    while user_type_reg.lower() not in ["customer", "employee"]:
        user_type_reg = input("Please select and input among Customer/Employee options: ")

    register_email = input("Input your email address: ")
    if user_type_reg.lower() == "customer":
        while not is_valid_email(register_email) or vanvitelli_bookstore.is_registered_customer(register_email):
            if not is_valid_email(register_email):
                register_email = input("Please input a valid email address: ")
            
            if vanvitelli_bookstore.is_registered_customer(register_email):
                print("There is an account already registered with this email ")
                swichToLogin = input("If you want to login input ok if not just press enter: ")

                if swichToLogin.lower() == "ok":
                    return user_login()
                
            register_email = input("Please input a valid email address: ")
    
    if user_type_reg.lower() == "employee":
        while not is_valid_email(register_email) or vanvitelli_bookstore.is_registered_employee(register_email):
            if not is_valid_email(register_email):
                register_email = input("Please input a valid email address: ")
            
            if vanvitelli_bookstore.is_registered_employee(register_email):
                print("There is an account already registered with this email ")
                swichToLogin = input("If you want to login input ok if not just press enter: ")

                if swichToLogin.lower() == "ok":
                    return user_login()
                
            register_email = input("Please input a valid email address: ")  
            
    register_name = input("Input your name (it should contain only letters): ")
    while not register_name.isalpha():
        register_name = input("Invalid input. Please enter only letters: ")
    
    register_surname = input("Input your surname (it should contain only letters): ")
    while not register_surname.isalpha():
        register_surname = input("Invalid input. Please enter only letters: ")

    register_birthDate = input("Input your date of birth (YYYY-MM-DD): ")
    while not is_valid_date_format(register_birthDate):
        register_birthDate = input("Enter your birthdate as the YYYY-MM-DD format please (Example: 2000-06-19): ")

    register_password = input("Select a six digit password: ")
    while not register_password.isdigit() or len(register_password) != 6:
        register_password = input("Please input a six digit (only numbers) password: ")

    if user_type_reg.lower() == "customer":
        vanvitelli_bookstore.register_customer(register_name, register_surname, register_birthDate, register_email, register_password)
    if user_type_reg.lower() == "employee":
        vanvitelli_bookstore.register_employee(register_name, register_surname, register_birthDate, register_email, register_password)
    
    relog()

#This function represents the menu for a logged-in customer.It provides options for loyalty card activation, purchasing books,
#checking order history, adding balance, and finding books.
def customer_menu(customerLogged):
    print(f"\n------------------------- {vanvitelli_bookstore.get_storeName()} bookstore costumer menu -------------------------")
    print(customerLogged)
    print("You can select a method to continue:")
    costumer_menu_input = input("Activate Loyality Card - Purchase Book - Order History - Add Balance - Find Book - Quite: ")
    
    while costumer_menu_input.lower() not in ["quite", "activate loyality card", "purchase book", "order history", "find book", "add balance"]:
        costumer_menu_input = input("You should select one of this methods:\nActivate Loyality Card - Purchase Book - Order History - Add Balance - Find Book - Quite: ")
    
    if costumer_menu_input.lower() == "quite":
        print("See you later !!")
        return relog()
    
    if costumer_menu_input.lower() == "activate loyality card":
        loyality_verify = input("To activate Loyality Card you should pay 10€. Do you want to continue ? (Yes/No)")
        
        while loyality_verify.lower() not in ["yes", "no"]:
            loyality_verify = input("You should select either yes or no: ")
        
        if loyality_verify.lower() == "yes":
            customerLogged.active_loyality()
            return customer_menu(customerLogged)
        
        if loyality_verify.lower() == "no":
            return customer_menu(customerLogged)
    
    if costumer_menu_input.lower() == "add balance":
        add_amount = input("Input the amount of money you want to add to your balance: ")
        
        while not add_amount.count('.') <= 1 and not add_amount.replace('.', '', 1).isdigit():
            add_amount = input("Please input a valid amount: ")
        customerLogged.add_balance(add_amount)
        return customer_menu(customerLogged)

    if costumer_menu_input.lower() == "find book":
        bookCodeToFind = input("Input the book code you want to find: ")
        vanvitelli_bookstore.find_book(bookCodeToFind)
        return customer_menu(customerLogged)
    
    if costumer_menu_input.lower() == "purchase book":
        vanvitelli_bookstore.archive_book_list()
        
        customerBookBuyCode = input("Input the book code you want buy: ")
        while not vanvitelli_bookstore.is_book_in_archive(customerBookBuyCode):
            customerBookBuyCode = input("Please input a correct book code: ")
        
        customerPurchaseQuantity = input("Input the quantity you want to buy: ")
        while not customerPurchaseQuantity.isdigit():
            customerPurchaseQuantity = input("The purchase quantity should be a number: ")
        
        vanvitelli_bookstore.buy_book(customerBookBuyCode, int(customerPurchaseQuantity), customerLogged)
        return customer_menu(customerLogged)

    if costumer_menu_input.lower() == "order history":
        customerLogged.show_order_history()
        return customer_menu(customerLogged)

#This function represents the menu for a logged-in employee.It provides options for adding, deleting, and editing books,
#viewing book lists, finding books, and checking sell history.
def employee_menu(employeeLogged):
    print(f"\n------------------------- {vanvitelli_bookstore.get_storeName()} bookstore employee menu -------------------------")
    print(employeeLogged)
    print("You can select a method to continue:")
    employee_menu_input = input("Add Book - Delete Book - Edit Book - Book List - Find Book - Sell History - Quite: ")

    while employee_menu_input.lower() not in ["quite", "add book", "delete book", "edit book", "find book", "sell history", "book list"]:
        employee_menu_input = input("You should select one of this methods:\nAdd Book - Delete Book - Edit Book - Book List - Find Book - Sell History - Quite: ")

    if employee_menu_input.lower() == "quite":
        print("See you later !!")
        return relog()
    
    if employee_menu_input.lower() == "add book":
        addBookTitle = input("Input the title of book you want to add: ")
        addBookAuthor = input("Input the author of the book you want to add: ")
        
        addBookPrice = input("Input the price of the book you want to add: ")
        while not addBookPrice.count('.') <= 1 and not addBookPrice.replace('.', '', 1).isdigit():
            addBookPrice = input("The price of the book should be a number: ")
        
        addBookQuantity = input("Input the quantity of the book you want to add: ")
        while not addBookQuantity.isdigit():
            addBookQuantity = input("The quantity of the book should be a number: ")

        vanvitelli_bookstore.add_book(addBookAuthor, addBookTitle, float(addBookPrice), int(addBookQuantity))
        return employee_menu(employeeLogged)
    
    if employee_menu_input.lower() == "delete book":
        bookCodeToDelete = input("Input the code of the book you want to delete from bookstore archive: ")
        vanvitelli_bookstore.remove_book(bookCodeToDelete)
        return employee_menu(employeeLogged)

    if employee_menu_input.lower() == "edit book":
        bookCodeToEdit = input("Input the code of the book you want to edit quantity: ")
        
        editQuantityMethod = input("Please choose whether you would like to add/remove from the quantity: ")
        while editQuantityMethod.lower() not in ["add", "remove"]:
            editQuantityMethod = input("You can add/remove the quantity: ")
        
        quantityToEdit = input(f"Please input the quantity you want to {editQuantityMethod}:")
        while not quantityToEdit.isdigit():
            quantityToEdit = input("The quantity must be a number: ")
          
        vanvitelli_bookstore.edit_book_quantity(editQuantityMethod, int(quantityToEdit), bookCodeToEdit)
        return employee_menu(employeeLogged)
    
    if employee_menu_input.lower() == "book list":
        vanvitelli_bookstore.archive_book_list()
        return employee_menu(employeeLogged)
    
    if employee_menu_input.lower() == "find book":
        bookCodeToFind = input("Input the book code you want to find: ")
        vanvitelli_bookstore.find_book(bookCodeToFind)
        return employee_menu(employeeLogged)
    
    if employee_menu_input.lower() == "sell history":
        vanvitelli_bookstore.show_sell_history()
        return employee_menu(employeeLogged)

# Starting the application
run_bookStore()
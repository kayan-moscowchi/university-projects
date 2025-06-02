#Represents some of users attributes and methods which are in common between and Customers and Employees and is a superior function
#which is inherited by the other two (Customer and Employee) classes
class person:

    def __init__(self, name, surname, birthdate, email, password):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.email = email
        self.password = password
    
    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_birthdate(self):
        return self.birthdate 

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

#Represents an Employee,completaly inheriting from the Person class.
class employee(person):
    def __init__(self, name, surname, birthdate, email, password):
        super().__init__(name, surname, birthdate, email, password)

    #Returns a string representation of the Employee object.
    def __str__(self):
        return f"Employee {self.name} {self.surname}"

#Represents a Customer, inheriting from the Person class and some other attributes which are special for the customers such as balance,
#loyality card and the order history of each customer.
class customer(person):

    def __init__(self, name, surname, birthdate, email, password):
        super().__init__(name, surname, birthdate, email, password)
        self.balance = 0
        self.loyality_card = False
        self.order_history = []

    #Returns a string representation of the Customer object.
    def __str__(self):
        if self.loyality_card == True:
            card_condition = "is active"
        else:
            card_condition = "isn't active"
        return f"Customer {self.name} {self.surname} - Balance : {self.balance} - Number of orders : {str(len(self.order_history))} - Loyality Card {card_condition}"

    #Activates the customer's loyalty card if conditions are met.
    def active_loyality(self):
        if self.loyality_card == False:
            if self.balance >= 10 :
                self.balance = self.balance - 10
                self.loyality_card = True
                print("Your Loyality card has been activated. For further purchases you will have a 10" + "%"+ " discount.")
            else:
                print("You dont have enough balance. Try to top up money to your account with 'add balance' method.")
        else:
            print("Your Loyality card is already activated !")

    #Adds balance to Customers balance.
    def add_balance(self, balance_amount):
        self.balance = self.balance + float(balance_amount)
        print("The amount of " + balance_amount + "€ added to your account balance.")

    def get_balance(self):
        return self.balance

    #Replaces new balance with the previous balance of Customer.
    def edit_balance(self, balanceAmount):
        self.balance = balanceAmount

    #Adds the new purchases of Customer to his/her order history list.
    def add_order_history(self, bookTitle, bookQuantity, spentAmount):
        self.order_history.append([bookTitle, bookQuantity, spentAmount])

    def show_order_history(self):
        if len(self.order_history) == 0:
            return print("\nYou have not ordered anything yet !")
        
        print("\nYour order history :")
        for orders in self.order_history:
            print(f"Book Title : {orders[0]} - Number purchased : {str(orders[1])} - Spent : {str(orders[2])}")

    def is_card_active(self):
        return self.loyality_card

#Represents a book with Author, Title, Price, Quantity attributes and a 4 digit code generated everytime as a unique number for each book in the bookstore.
class book:
    code_counter = 0

    def __init__(self, author, title, price, quantity):
        self.author = author
        self.title = title
        self.price = price
        self.quantity = quantity
        self.code = self.generate_code()

    #Returns a string representation of the Book object.
    def __str__(self):
        return f"Author : {self.author} - Title : {self.title} - Price : {self.price}€ - Code : {self.code} - Quantity : {self.quantity}"

    #Generates a unique 4 digit code starting from 0001 to 9999 for every book.
    def generate_code(self):
        book.code_counter += 1
        formatted_code = f"{book.code_counter:04}"
        return formatted_code

    #Replaces new price with the previous price of the book.
    def price_update(self, new_price):
        self.price = new_price

    #Replaces new quantity with the previous quantity of the book.
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_code(self):
        return self.code

class bookstore:
    def __init__(self, storeName):
        self.storeName = storeName
        self.book_archive = []
        self.customers_list = []
        self.employees_list = []
        self.sell_history = []
        self.customers_list.append(customer("kian", "mesgouchi", "2000-06-19", "kayan@gmail.com", 123456))
        self.employees_list.append(employee("kian", "mesgouchi", "2000-06-19", "kayan@gmail.com", 123456))
        self.book_archive.append(book("Chinua Achebe", "Things Fall Apart", 15.99, 20))
        self.book_archive.append(book("Khaled Hosseini", "The Kite Runner", 16.49, 30))
        self.book_archive.append(book("Jane Austen", "Pride And Prejudice", 25, 15))

    def get_storeName(self):
        return self.storeName

    #Prints all the books available in the Bookstore archive.
    def archive_book_list(self):
        print("\nThese books are available at the bookstore at the moment: ")
        for books in self.book_archive:
            print(books)

    #Adds a new Book to the Bookstore archive.
    def add_book(self, author, title, price, quantity):
        new_book = book(author, title, price, quantity)
        self.book_archive.append(new_book)
        return print(f"Book {title} written by {author} with price of {price}€ added successfully. Book Code : {new_book.get_code()} - Quantity : {quantity}")

    #Removes a Book from the Bookstore archive based on its code.
    def remove_book(self, bookCode):
        for books in self.book_archive:
            if books.get_code() == bookCode:
                print(f"Book {books.get_title()} written by {books.get_author()} with price of {books.get_price()}€ and quantity of {books.get_quantity()} removed sucessfully.")
                return self.book_archive.remove(books)
        
        return print(f"There aren't any books in bookstores archive with {bookCode} code.")

    #Edits the quantity of a book by its code in the Bookstore archive considering the method given by Employee (Add or Remove)
    def edit_book_quantity(self, method_name, edit_quantity, editBookCode):
        for books in self.book_archive:
            if books.get_code() == editBookCode:
  
                if method_name == "add":
                    new_quantity = books.get_quantity() + edit_quantity
                    books.update_quantity(new_quantity)
                    print(f"{edit_quantity} books of {books.get_title()} added successfully to the bookstore archive.")
                    return print(books)

                if method_name == "remove":
                    
                    if books.get_quantity() < edit_quantity:
                        return print(f"There are only {books.get_quantity()} of book code {editBookCode} available !")
                    
                    else:
                        new_quantity = books.get_quantity() - edit_quantity
                        books.update_quantity(new_quantity)
                        print(f"{edit_quantity} books of {books.get_title()} removed successfully from the bookstore archive.")
                        return print(books)
        
        return print(f"There aren't any books with code {editBookCode} in the bookstore archive.")

    #Finds and prints the details of a book in the Bookstore archive based on its code.
    def find_book(self, bookCodeToFind):
        for books in self.book_archive:
            if books.get_code() == bookCodeToFind:
                return print(books)
        print(f"There aren't any book available with code {bookCodeToFind} ! Try again with a correct book code later.")

    #Checks if a Book with the given code is present in the Bookstore archive.
    def is_book_in_archive(self, bookCode):
        for books in self.book_archive:
            if books.get_code() == bookCode:
                return True
        return False

    #Adds a record to the sell history.
    def add_sell_history(self, customerName, customerSurname, bookTitle, bookCode, quantityPurchased):
        self.sell_history.append([customerName, customerSurname, bookTitle, bookCode, quantityPurchased])

    #Prints out all the sold Books in the corresponding Bookstore.
    def show_sell_history(self):
        if len(self.sell_history) == 0:
            return print("Nothing sold yet !")
        
        print("\nSell history :")
        for sells in self.sell_history:
            print(f"Customer {sells[0]} {sells[1]} - Book Title : {sells[2]} - Book Code : {sells[3]} - Quantity Purchased : {sells[4]}")

    #Allows a Customer to purchase a Book if he/she mets all the conditions and considers a 10% discount for active loyality cards pushing all the
    #changed information to differents methods of Customer class and recording the sold both as sell history of the Bookstore and order history of the Customer. 
    def buy_book(self, buyCode, buyQuantity, customerLogged):
        for books in self.book_archive:
            
            if buyCode == books.get_code():
                
                if buyQuantity <= books.get_quantity():

                    if customerLogged.is_card_active() == True :
                        
                        if books.get_price() * buyQuantity * 0.9 <= customerLogged.get_balance():
                            new_balance = customerLogged.get_balance() - (books.get_price() * buyQuantity * 0.9)
                            new_quantity = books.get_quantity() - buyQuantity
                            books.update_quantity(new_quantity)
                            customerLogged.edit_balance(new_balance)
                            customerLogged.add_order_history(books.get_title(), str(buyQuantity), (books.get_price() * buyQuantity * 0.9))
                            self.add_sell_history(customerLogged.get_name(), customerLogged.get_surname(), books.get_title(), buyCode, str(buyQuantity))
                            return print(f"Purchase completed. Book name : {books.get_title()} - Quantity : {str(buyQuantity)} - Total Spent : {books.get_price() * buyQuantity * 0.9}")
                    
                        return print("You don't have enough balance to purchase. Please add balance and try again later.")
                
                    if books.get_price() * buyQuantity <= customerLogged.get_balance():
                        new_balance = customerLogged.get_balance() - (books.get_price() * buyQuantity)
                        new_quantity = books.get_quantity() - buyQuantity
                        books.update_quantity(new_quantity)
                        customerLogged.edit_balance(new_balance)
                        customerLogged.add_order_history(books.get_title(), str(buyQuantity), (books.get_price() * buyQuantity))
                        self.add_sell_history(customerLogged.get_name(), customerLogged.get_surname(), books.get_title(), buyCode, str(buyQuantity))
                        return print(f"Purchase completed. Book name : {books.get_title()} - Quantity : {str(buyQuantity)} - Total Spent : {books.get_price() * buyQuantity}")                

                    return print("You don't have enough balance to purchase. Please add balance and try again later.")
                
                return print("Insufficient quantity !")
            
        return print("Book code not found !")

    #Checks if a Customer with the given email is registered.
    def is_registered_customer(self, email):
        for customers in self.customers_list:
            
            if customers.get_email() == email:
                return True
        
        return False
    
    #Checks if a Employee with the given email is registered.
    def is_registered_employee(self, email):
        for employees in self.employees_list:
            
            if employees.get_email() == email:
                return True
        
        return False
    
    #Registers a new Customer in the Bookstore.
    def register_customer(self, name, surname, birthdate, email, password):
        self.customers_list.append(customer(name, surname, birthdate, email, password))

        return print(f"\nUser {name} {surname} registered successfully as a customer.\nNow you can login to your account.")
    
    #Registers a new Employee in the Bookstore.
    def register_employee(self, name, surname, birthdate, email, password):
        self.employees_list.append(employee(name, surname, birthdate, email, password))

        return print(f"\nUser {name} {surname} registered successfully as an employee.\nNow you can login to your account.")
    
    #Finds and returns a Customer among the registered Customers by its email address.
    def customer_finder(self, email):
        for customers in self.customers_list:
            if customers.get_email() == email:
                return customers
 
    #Finds and returns an Employee among the registered Employees by its email address.
    def employee_finder(self, email):
        for employees in self.employees_list:
            if employees.get_email() == email:
                return employees

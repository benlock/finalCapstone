#====README====
#Type 'pip install tabulate' in console before running

#This installs the tabulate library to allow creation of tables to display data
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    #This returns the cost of a given shoe object
    def get_cost(self):
        return self.cost

    #This returns the quantity of a given shoe object
    def get_quantity(self):
        return self.quantity

    #This returns a string representation of the shoe object for writing to the inventory txt file
    def __str__(self):
       return f'{self.country},{self.code},{self.product},{self.cost},{self.quantity}'

#=============Shoe list===========
shoe_list = []
#==========Functions outside the class==============
#This reads the inventory file, skips the first line and converts the  remaining lines into a format which allows them to be added to the shoe list.
def read_shoes_data():
    file = open('inventory.txt', 'r')
    contents = file.readlines()
    for line in contents:
        if contents.index(line) == 0:
            pass
        else:
            newline = line.replace('\n', '')
            newline = newline.split(',')
            #If any of the lines are not in the expected format, an error will be returned and the relevant line will not be added to the shoe list. 
            try:
                shoe_object = Shoe(newline[0], newline[1], newline[2], int(newline[3]), int(newline[4]))
                shoe_list.append(shoe_object)
            except TypeError:
                print(f'There was an error with {line}. Please check it\'s details and try again.')
            except ValueError:
                print(f'There was an error with line {contents.index(line)+1}. Please check its details and try again.')
    file.close()

#This allows new shoes to be added to the inventory. 
#A new shoe object is created, and then the string representation is added to the file.       
def capture_shoes():
    new_shoe_country = input("Enter the country: ")
    new_shoe_code = input("Enter the code: ")
    new_shoe_product = input("Enter the product: ")
    #These lines ensure that only integers can be added for the cost and quantity parameters. 
    new_shoe_cost = input("Enter the cost: ")
    while type(new_shoe_cost) != int:
        try:
            new_shoe_cost = int(new_shoe_cost)
        except ValueError:
            new_shoe_cost = input('You have entered an invalid cost. Please try again: ')
    new_shoe_quantity = input("Enter the quantity: ")
    while type(new_shoe_quantity) != int:
        try:
            new_shoe_quantity = int(new_shoe_quantity)
        except ValueError:
            new_shoe_quantity = input('You have entered an invalid quantity. Please try again: ')

    new_shoe = Shoe(new_shoe_country, new_shoe_code, new_shoe_product, new_shoe_cost, new_shoe_quantity)
    shoe_list.append(new_shoe)

    file = open('inventory.txt', 'a+')
    file.write(f'{new_shoe.__str__()}\n')
    file.close()  
    print('Details added to inventory')
    print()  

#This returns a table with all of the shoe data from the inventory file.
def view_all():
    file = open('inventory.txt', 'r')
    contents = file.readlines()
    new_list = []
    for item in contents:
        item.replace('\n', '')
        item = item.split(',')
        new_list.append(item)
    table1 = tabulate(new_list, headers='firstrow')
    print(table1)

    '''for shoes in shoe_list:
        print(shoes.__str__() + '\n')'''

#This adds all of the shoe quantities to a list, and returns the index of the lowest value. 
#That index is then found in the main shoe list, and the relevant properties of that shoe are extracted. 
#The restock quantity is added to the current quantity. 
def re_stock():
    shoe_quant_list = []
    for shoes in shoe_list:
        shoe_quant = shoes.get_quantity()
        shoe_quant_list.append(shoe_quant)
    min_quant_index = shoe_quant_list.index(min(shoe_quant_list))
    
    print(f'The item lowest in stock is {shoe_list[min_quant_index].product}, (code {shoe_list[min_quant_index].code}). There are {shoe_list[min_quant_index].quantity} in stock.')
    restock_quant = int(input('How many of this product would you like to order? '))
    updated_quant = shoe_list[min_quant_index].quantity + restock_quant
    shoe_list[min_quant_index].quantity = updated_quant
  
    #The inventory file is opened and the relevant line is updated. 
    file = open('inventory.txt', 'r')
    contents = file.readlines()
    file.close()
    for line in contents:
        if shoe_list[min_quant_index].code in line:
            target_line = line
            line = line.split(',')
            line[-1] = str(updated_quant)
            new_line = ','.join(line)
        else:
            pass
    #The inventory file is opened and close to clear the contents. 
    #The new data is then entered and the outcome is printed. 
    contents[(contents.index(target_line))] = f'{new_line}\n'
    file = open('inventory.txt', 'w+')
    file.close()
    file = open('inventory.txt', 'w+')
    for line in contents:
        file.write(line)
    file.close()  
    print(f'{restock_quant} pairs of {shoe_list[min_quant_index].product} have been ordered. There are now {updated_quant} pairs in stock')
    print()

#The list is searched and the relevant data returned. 
#An error is returned if an unknown SKU is entered. 
def search_shoe():
    print('Enter the shoe code you wish to search for, or -1 to return to the main menu')
    while True:
        search_term = input('')
        if search_term == '-1':
            print()
            break
        else:
            found = 0
            for shoes in shoe_list:
                if shoes.code == search_term:
                    print()
                    print(f'''Country: {shoes.country}
Code: {shoes.code}
Product: {shoes.product}
Cost: {shoes.cost}
Quantity: {shoes.quantity}''')
                    print()
                    found += 1  
                    break
                else:
                    pass
                
            if found == 0:
                print('There is no shoe with that code. Please enter another code, or enter -1 to return to the main menu: ')
                continue
            else:
                pass
        break

#The relevant calculation is performed, and the outcome returned as a table.
def value_per_item():
    stock_value_list = [['Product', 'Stock Value']]
    for shoes in shoe_list:
        stock_value = shoes.cost * shoes.quantity
        stock_value_list.append([shoes.product, str(stock_value)])

    table1 = tabulate(stock_value_list, headers='firstrow')
    print(table1)


#This uses the same logic as finding the minimum quantity. 
def highest_qty():
    shoe_quant_list = []
    for shoes in shoe_list:
        shoe_quant = shoes.get_quantity()
        shoe_quant_list.append(shoe_quant)
    max_quant_index = shoe_quant_list.index(max(shoe_quant_list))
    
    print(f'The item highest in stock is {shoe_list[max_quant_index].product}, (code {shoe_list[max_quant_index].code}).')
    print(f'There are {shoe_list[max_quant_index].quantity} pairs in stock')
    print()
    pass


#==========Main Menu=============
'''
Creates a menu that executes each function above.
'''

read_shoes_data()

while True:
    menu_selection = input('''Please select an option:
    c - Capture data about a shoe
    va - View all shoes
    r - Re-stock the shoe with the lowest stock
    s - Search shoes
    sv - Display the stock value for each shoe
    hq - Show which shoe has the most in stock 
    e - exit
    ''').lower()

    if menu_selection == 'c':
        capture_shoes()

    elif menu_selection == 'va':
        view_all()

    elif menu_selection == 'r':
        re_stock()

    elif menu_selection == 's':
        search_shoe()

    elif menu_selection == 'sv':
        value_per_item()

    elif menu_selection == 'hq':
        highest_qty()
    
    elif menu_selection == 'e':
        print('Thank you. Goodbye')
        break
    
    else:
        print('You have made an incorrect selection. Please try again')
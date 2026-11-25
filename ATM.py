"""
ATM

ATM.py

Author: Omar Rolon

A Python program that simulates the operation of an automatic teller
machine (ATM), modeling both the user-facing interface and the internal
logic behind it.

The system stores account numbers, PINs, balances, and the machine's
physical cash inventory. New users can register an account: the program
creates a unique 16-digit account number for them and asks them to
choose a PIN, rejecting PINs that are too easy to guess.

Users log in with their account number and PIN, which is hidden with
asterisks while it is typed. They have three attempts, and the account
is blocked if all of them fail. Once inside, a menu lets them check
their balance, withdraw cash, deposit cash, change their PIN, review
their transaction history, and see the cash available in the ATM.

Withdrawals are given with the available bills, from the highest to the
lowest, and deposits are made bill by bill, so the ATM's cash inventory
changes with every operation. All accounts are saved in a file, and
every withdrawal and deposit is recorded with its date and time in a
history file, so the information is kept even after the program closes.
"""

import random
import time
import pwinput

def welcome_menu():
    """
    Inputs: No inputs
    Outputs: The welcome menu on screen
    Process:
    -Prints the welcome message and the options: log in, register
    and exit
    """
    print("\nATM\n\nWELCOME\n\n1) Log in\n2) Register\n3) Exit\n")


def operations_options_menu():
    """
    Inputs: No inputs
    Outputs: The operations menu on screen
    Process:
    -Prints the options: consult balance, withdraw cash, deposit cash,
    PIN change, transaction history, ATM cash and exit
    """
    print("\n1)Consult Balance\n2)Withdraw Cash\n3)Deposit Cash\n4)PIN Change\n5)Transaction History\n6)Check current cash in the ATM\n7)Exit\n")


def consult_balance(data, user): 
    """
    Inputs: The account's data and the user
    Outputs: The user's balance on screen
    Process:
    -It will take the user's balance from the accounts data
    -It will print the balance
    """
    balance = data[user][2]
    print("\nYour balance is", "$"+str(balance), "pesos\n" )


def withdraw_cash(data, user, bills_denominations, bills_quantity):
    """
    Inputs: The accounts data, the user, the bills denominations, the
    bills quantity and the amount of money to be withdrawn
    Outputs: The withdrawn bills and the total on screen
    Process:
    -If the balance is less than 50, it will end the operation
    -Asks for the amount and validates that it only has digits
    -Validates that the amount is greater than 0, does not exceed the
    balance, is multiple of 50 and does not exceed the ATM cash
    -From the highest to the lowest bill, it calculates how many bills
    are needed, without using more bills than the ATM has
    -If the exact amount can't be given, it will end the operation
    -Asks for confirmation
    -Updates the bills quantity and the user's balance
    -Shows the withdrawn bills and saves the operation in the history
    """
    balance = data[user][2]
    if balance < 50:
        print("Your balance is not enough to make a withdrawal")
        return
    while True:
        withdraw = input("Amount of money to be withdrawn: $")
        withdraw_filter = withdraw.strip().replace(" ", "").replace(",", "").replace("$" , "")
        if withdraw_filter.isdigit() == False:
            print("Only digits are accepted")
        else:
            withdraw = int(withdraw_filter)
            if withdraw <= 0:
                print("Amount must be greater than 0")
            elif withdraw > balance:
                print("Amount to be withdrawn exceeds your balance")
            elif withdraw % 50 != 0:
                print("Amount needs to be multiple of 50")
            elif withdraw > atm_total_cash_sum(bills_denominations, bills_quantity):
                print("Amount exceeds the total cash available in the ATM")
            else:
                break
    total_withdrawn_bills = []
    remaining_cash = withdraw
    for i in range(len(bills_denominations)):
        bills_required = remaining_cash // bills_denominations[i]
        bills = min(bills_required, bills_quantity[i])
        total_withdrawn_bills.append(bills)
        remaining_cash = remaining_cash - bills * bills_denominations[i] 
    if remaining_cash == 0:
        message = "Are you sure you want to withdraw this quantity?: $"+str(withdraw)+" pesos"
        if keep_going(message) == True:
            new_balance = balance - withdraw
            for j in range(len(bills_denominations)):
                new_bills_quantity = bills_quantity[j] - total_withdrawn_bills[j]
                bills_quantity[j] = new_bills_quantity
            data[user][2] = new_balance
            print("You have withdrawn:")
            for k in range(len(total_withdrawn_bills)):
                if total_withdrawn_bills[k] > 0:
                    print("-", total_withdrawn_bills[k], "bills of", "$"+str(bills_denominations[k]))
            print("TOTAL:", "$"+str(withdraw), "pesos")
            save_operation(data[user][0], "WITHDRAWAL",  withdraw, new_balance)
        else:
            print("OPERATION CANCELLED")
            return
    else:
        print("The ATM cannot dispense that exact amount")
        return


def deposit_cash(data, user, bills_denominations, bills_quantity):
    """
    Inputs: The accounts data, the user, the bills denominations, the
    bills quantity and the number of bills of each type
    Outputs: The deposited bills and the total on screen
    Process:
    -Asks how many bills of each type the user is inserting and
    validates that it only has digits
    -Calculates the total money deposited
    -If no bills were inserted, it will end the operation
    -Asks for confirmation
    -Adds the bills to the bills quantity and the total to the balance
    -Shows the deposited bills and saves the operation in the history
    """
    print("\nAccepted bills:\n- $500\n- $200\n- $100\n- $50\nInsert your bills...\n\n")
    total_deposited_bills = []
    total_money_deposited = 0
    balance = data[user][2]
    for i in range(len(bills_denominations)):
        while True:
            amount_of_bills = input("How many $"+str(bills_denominations[i])+" bills: ").strip().replace(" ", "")
            if amount_of_bills.isdigit() == True:
                amount_of_bills = int(amount_of_bills)
                total_deposited_bills.append(amount_of_bills)
                total_money_deposited = total_money_deposited + amount_of_bills * bills_denominations[i]
                break
            else:
                print("Only digits are accepted")
    if total_money_deposited == 0:
        print("No bills were inserted")
        return
    else:
        message = "You are about to deposit $"+str(total_money_deposited)+" pesos\nDo you want to proceed?"
        if keep_going(message) == True:
            for j in range(len(bills_quantity)):
                new_bills_quantity = bills_quantity[j] + total_deposited_bills[j]
                bills_quantity[j] = new_bills_quantity
            new_balance = balance + total_money_deposited
            data[user][2] = new_balance
            print("You have deposited:")
            for k in range(len(total_deposited_bills)):
                if total_deposited_bills[k] > 0:
                    print("-", str(total_deposited_bills[k]), "bills of", "$"+str(bills_denominations[k]), "pesos")
            print("TOTAL DEPOSITED:", "$"+str(total_money_deposited), "pesos")
            save_operation(data[user][0], "DEPOSIT", total_money_deposited, new_balance)
        else:
            print("OPERATION CANCELLED")
            return


def save_operation(account_number, operation_type, amount, balance_after_operation):
    """
    Inputs: The account number, the operation type, the amount and the
    balance after the operation
    Outputs: A new line in the history file
    Process:
    -Gets the current date and time of the operation
    -Converts all the data into text
    -Joins the data with commas
    -Adds the line at the end of the history file
    """
    operation_date = time.strftime("%Y/%m/%d")
    operation_time = time.strftime("%H:%M")
    operation_line = [account_number, operation_type, amount, balance_after_operation, operation_date, operation_time]
    line = []
    for value in operation_line:
        line.append(str(value))
    file = open("history.txt", "a")
    file.write(",".join(line)+"\n")
    file.close()


def show_history(data, user):
    """
    Inputs: The accounts data and the user
    Outputs: The user's operations on screen
    Process:
    -Shows the user's account number with dashes
    -Reads the history file line by line
    -If the line belongs to the user, it will print the date, time,
    type, amount and balance after the operation
    -If the user has no operations, it will print a message
    """
    account_number = data[user][0]
    print("Transaction history for account", account_number_format(account_number)+":\n")
    try:
        file = open("history.txt", "r")
        found = False
        for line in file:
            line = line.strip().split(",")
            if account_number in line:
                found = True
                print(line[4], line[5]+" | "+line[1]+" | $"+line[2]+" pesos | Balance after operation: $"+line[3]+" pesos")
        file.close()
        if found == False:
            print("No operations yet")
    except FileNotFoundError:
        print("The history data does not exist")


def pin_change(data, user):
    """
    Inputs: The accounts data, the user, the current PIN, the new PIN
    and the new PIN confirmation
    Outputs: The user's PIN updated
    Process:
    -Asks for the current PIN, if it is incorrect it will end the
    operation
    -Shows the tips for PIN creation
    -Asks for the new PIN and validates that it has 4 digits, is
    different from the current PIN and is not weak
    -Asks for the confirmation, if it is the same, it will update the
    PIN
    """
    pin = pwinput.pwinput(prompt="Current PIN: ", mask="*").strip().replace(" ", "")
    if pin != data[user][1]:
        print("Incorrect PIN")
        return
    pin_creation_tips()
    print("-Avoid using your current PIN")
    while True:
        new_pin = pwinput.pwinput(prompt="New PIN: ", mask="*").strip().replace(" ", "")
        if new_pin.isdigit() == True and new_pin != pin and len(new_pin) == 4:
            if is_pin_weak(new_pin) == False:
                new_pin_confirmation = pwinput.pwinput(prompt="New PIN confirmation: ", mask="*").strip().replace(" ", "")
                if new_pin != new_pin_confirmation:
                    print("New PIN needs to be the same that the new PIN confirmation")
                else:
                    data[user][1] = new_pin
                    print("PIN changed successfully!")
                    return 
            else:
                print("Your PIN is too easy to guess, please check the tips above")
        else:
            print("\nInvalid PIN")


def atm_total_cash_sum(bills_denominations, bills_quantity):
    """
    Inputs: The bills denominations and the bills quantity
    Outputs: ATM current cash
    Process:
    -For each type of bill, it multiplies the denomination by the
    quantity and adds it to the total
    -It will return the total cash
    """
    total_cash = 0
    for i in range(len(bills_quantity)):
        total_cash = total_cash + bills_quantity[i]*bills_denominations[i]
    return total_cash


def atm_total_cash_show(bills_denominations, bills_quantity):
    """
    Inputs: The bills denominations and the bills quantity
    Outputs: The ATM cash on screen
    Process:
    -Prints how many bills of each type the ATM has
    -Prints the total cash in the ATM
    """
    print("The total cash in the ATM is:\n")
    for i in range(len(bills_quantity)):
        print("-", bills_quantity[i], "bills of", "$"+str(bills_denominations[i]), "\n")
    print("TOTAL:", "$"+str(atm_total_cash_sum(bills_denominations, bills_quantity)), "\n")


def authentication(data):
    """
    Inputs: The accounts data, the account number and the account PIN
    Outputs: The user (row of the account in the data) or -1
    Process:
    -Asks for the account number and removes spaces and dashes
    -Looks for the account number in the accounts data
    -If the account does not exist, it will ask again
    -If the account is blocked, it will return -1
    -Asks for the PIN and gives up to 3 attempts
    -Returns the user if the PIN is correct
    -Blocks the account and returns -1 if the attempts are over
    """
    print("\nHello there!!")
    print("-Remember that your account number has 16 digits\n-Do NOT use special characters other than '-' or blank spaces")
    while True:
        user = -1
        attempts = 3
        account_number = input("\nAccount number: ").strip().replace(" ", "").replace("-", "")
        for i in range(len(data)):
            if account_number  == data[i][0]:
                user = i
                break
        if user == -1:
            print("ACCOUNT NOT FOUND")
        elif data[user][3]:
            return -1
        else: 
            print("\n-Remember that your PIN is only composed of 4 digits with no special characters")
            while 1 <= attempts <= 3:
                account_pin = pwinput.pwinput(prompt="\nAccount PIN: ", mask="*").strip().replace(" ", "")
                if account_pin == data[user][1]:
                    return user
                elif attempts == 1:
                    data[user][3] = True
                    return -1
                else:
                    attempts = attempts - 1
                    print("Incorrect PIN, you have", attempts, "left")


def is_pin_weak(pin):
    """
    Inputs: The PIN
    Outputs: True if the PIN is weak, False if it is not
    Process:
    -Checks if the PIN has the same digit four times
    -Checks if the PIN is an ascending or descending sequence
    -Checks if the PIN repeats a pair of digits
    -Checks if the PIN has two pairs of repeated digits
    -If any of them is true, it will return True
    """
    numbers_ascendent = "0123456789"
    numbers_descendent = "9876543210"
    if pin.count(pin[0]) == 4: 
        return True
    elif pin in numbers_ascendent:
        return True
    elif pin in numbers_descendent:
        return True
    elif pin[0:2] == pin[2:4]:
        return True
    elif pin[0] == pin[1] and pin[2] == pin[3]:  
        return True
    else:
        return False     


def pin_creation_tips():
    """
    Inputs: No inputs
    Outputs: The tips for PIN creation on screen
    Process:
    -Prints the rules for a valid PIN
    -Prints examples of weak PINs that are not accepted
    """
    print("\nTIPS FOR PIN CREATION:")
    print("-Remember that your PIN needs to have only 4 digits")
    print("-Try to avoid typing blank spaces")
    print("-Avoid using the same digit four times, for example: 1111 or 0000")
    print("-Avoid ascending or descending sequences, for example: 6789 or 4321")
    print("-Avoid repeating a pair of digits, for example: 1212 or 6969")
    print("-Avoid using two pairs of repeated digits, for example: 1122 or 7788")


def new_account(data):
    """
    Inputs: The accounts data, the user's name, the PIN and the PIN
    confirmation
    Outputs: A new account added to the accounts data
    Process:
    -Asks for the name and validates that it only has letters
    -Creates a random 16 digit account number that does not exist yet
    -Shows the tips for PIN creation
    -Asks for the PIN and validates that it has 4 digits and is not
    weak
    -Asks for the confirmation until it is the same
    -Shows the new account number
    -Adds the new account to the accounts data
    """
    print("\nHello there!!\nLet's begin with your username\n")
    while True:
        new_username = " ".join(input("What is your name?: ").split())
        if new_username.replace(" ", "").isalpha() == True:
            break
        else:
            print("Invalid Username\n")
    while True:
        account_number_exists = False
        new_account_number = str(random.randint(0000000000000000, 9999999999999999)).zfill(16)
        for user in range(len(data)):
            if new_account_number == data[user][0]:
                account_number_exists = True
                break
        if account_number_exists == False:
            break
    new_username_show = new_username.title()
    print("\nHere we GO", new_username_show+"!", "\nLet's create your PIN!")
    pin_creation_tips()
    while True:
        new_pin = pwinput.pwinput(prompt="\nCreate your PIN: ", mask="*").strip().replace(" ", "")
        if new_pin.isdigit() == True and len(new_pin) == 4:
            if is_pin_weak(new_pin) == False:
                new_pin_confirmation = pwinput.pwinput(prompt="New PIN confirmation: ", mask="*").strip().replace(" ", "")
                if new_pin_confirmation == new_pin:
                    break
                else:
                    print("Your PIN is different from the PIN confirmation")
            else:
                print("Your PIN is too easy to guess, please check the tips above")
        else:
            print("Invalid PIN")
    print("\nYour account number is", account_number_format(new_account_number), "\nYou have registered successfully!!")
    new_user = [new_account_number, new_pin, 0, False, new_username_show, float(0)]
    data.append(new_user)


def account_number_format(account_number):
    """
    Inputs: The account number
    Outputs: The account number with dashes
    Process:
    -Splits the account number into 4 groups of 4 digits
    -Joins the groups with dashes
    -It will return the account number with dashes
    """
    account_number_display = "-".join([account_number[:4], account_number[4:8], account_number[8:12], account_number[12:]])
    return account_number_display


def keep_going(message):
    """
    Inputs: The message of the question and the user's answer
    Outputs: True if the answer is Y, False if the answer is N
    Process:
    -Shows the message and asks for Y or N
    -If the answer is not Y or N, it will ask again
    """
    while True:
        answer = input(message+" (Y/N): ").strip().replace(" ", "")
        if answer.upper() == "Y":
            return True
        elif answer.upper() == "N":
            return False
        else:
            print("Invalid Option, please type Y or N")


def save_accounts(data):
    """
    Inputs: The accounts data
    Outputs: The accounts file updated
    Process:
    -Opens the accounts file and rewrites it
    -For each account, converts all the data into text
    -Joins the data with commas and writes it as a line
    """
    file = open("accounts.txt", "w")
    for row in data:
        line = []
        for value in row:
            line.append(str(value))
        line_string = ",".join(line)
        file.write(line_string+"\n")
    file.close()


def load_accounts():
    """
    Inputs: No inputs
    Outputs: The accounts data
    Process:
    -Opens the accounts file and reads it line by line
    -Splits each line by commas into a list
    -Converts the balance into int, the blocked state into True or
    False and the block time into float
    -Adds each account to the accounts data
    -It will return the accounts data
    """
    data = []
    try:
        file = open("accounts.txt", "r")
        for line_in_file in file:
            line_in_matriz = line_in_file.strip().split(",")
            for value in range(len(line_in_matriz)):
                if value == 2:
                    line_in_matriz[value] = int(line_in_matriz[value])
                elif value == 5:
                    line_in_matriz[value] = float(line_in_matriz[value])
                elif value == 3:
                    boolean = line_in_matriz[value] == "True"
                    line_in_matriz[value] = boolean
            data.append(line_in_matriz)
        file.close()
    except FileNotFoundError:
        print("There are no accounts yet")
    return data


def main():
    """
    Inputs: The options selected by the user
    Outputs: The ATM program running
    Process:
    -Loads the accounts data from the file
    -Shows the welcome menu until the user exits
    -Option 1: logs in the user and shows the operations menu until
    the user logs out
    -Option 2: registers a new account
    -Option 3: ends the program
    -Saves the accounts data every time something changes
    """
    data = load_accounts()                                                  
    bills_denominations = [500, 200, 100, 50]
    bills_quantity = [6, 13, 27, 41]
    while True:
        welcome_menu()
        option1 = input("Choose an option: ").strip().replace(" ", "")
        match option1:
            case "1":
                user = authentication(data)
                if user != -1:
                    print("\n\nWelcome Back,", data[user][4])
                    while True:
                        operations_options_menu()
                        option2 = input("Choose an option: ").strip().replace(" ", "")
                        match option2:
                            case "1":
                                consult_balance(data, user)
                            case "2":
                                withdraw_cash(data, user, bills_denominations, bills_quantity)
                            case "3":
                                deposit_cash(data, user, bills_denominations, bills_quantity)
                            case "4":
                                pin_change(data, user)
                            case "5":
                                show_history(data, user)
                            case "6":
                                atm_total_cash_show(bills_denominations, bills_quantity)
                            case "7":
                                break
                            case _:
                                print("Invalid Option")
                        save_accounts(data)
                        message = "Would you like to do another operation?"
                        if keep_going(message) == False:
                            break
                    print("LOGGED OUT")
                else:
                    print("ACCOUNT BLOCKED")
                save_accounts(data)
            case "2":
                new_account(data)
                save_accounts(data)
            case "3":
                break
            case _:
                print("Invalid option")

                
main()

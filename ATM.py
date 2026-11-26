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
is blocked if all of them fail. They can also type E to go back to the
welcome menu. Once inside, a menu lets them check their balance,
withdraw cash, deposit cash, change their PIN, review their transaction
history, and see the cash available in the ATM.

Withdrawals are given with the available bills, from the highest to the
lowest, and deposits are made bill by bill, so the ATM's cash inventory
changes with every operation. All accounts are saved in a file, and
every withdrawal and deposit is recorded with its date and time in a
history file, so the information is kept even after the program closes.
If one of these files does not exist, the program keeps working: it
starts with no accounts or with an empty history.
"""

# Libraries
import random
import time

import pwinput

# Constants
ASCENDING_DIGITS = "0123456789"
DESCENDING_DIGITS = "9876543210"
BILLS_DENOMINATIONS = [500, 200, 100, 50]


# ========================== Menu functions ==========================


def welcome_menu():
    """
    Topics: functions, strings
    Inputs: No inputs
    Outputs: The welcome menu on screen
    Process:
    -Prints the welcome message and the options: log in, register
    and exit
    Test case:
    -welcome_menu() prints WELCOME and the options 1) Log in,
    2) Register and 3) Exit
    """
    print("\nATM\n\nWELCOME\n\n1) Log in\n2) Register\n3) Exit\n")


def operations_options_menu():
    """
    Topics: functions, strings
    Inputs: No inputs
    Outputs: The operations menu on screen
    Process:
    -Prints the options: consult balance, withdraw cash, deposit cash,
    PIN change, transaction history, ATM cash and exit
    Test case:
    -operations_options_menu() prints the 7 options, from
    1)Consult Balance to 7)Exit
    """
    print("\n1)Consult Balance\n2)Withdraw Cash\n3)Deposit Cash\n"
          "4)PIN Change\n5)Transaction History\n"
          "6)Check current cash in the ATM\n7)Exit\n")


# ===================== ATM operation functions ======================


def consult_balance(accounts, user):
    """
    Topics: functions, matrices, strings
    Inputs: The account's data and the user
    Outputs: The user's balance on screen
    Process:
    -It will take the user's balance from the accounts data
    -It will print the balance
    Test case:
    -If Pedro (user 0) has a balance of 17337, it prints
    "Your balance is $17337 pesos"
    """
    balance = accounts[user][2]
    print("\nYour balance is", "$" + str(balance), "pesos\n")


def withdraw_cash(accounts, user, bills_denominations, bills_quantity):
    """
    Topics: arithmetic operators, conditionals, loops, lists, matrices,
    strings
    Inputs: The accounts data, the user, the bills denominations, the
    bills quantity and the amount of money to be withdrawn
    Outputs: The withdrawn bills and the total on screen
    Process:
    -If the balance is less than 50, it will end the operation
    -If the ATM has no cash, it will end the operation
    -Asks for the amount, removes blank spaces, commas and the $ sign,
    and validates that it only has digits
    -Validates that the amount is greater than 0, does not exceed the
    balance, is multiple of 50 and does not exceed the ATM cash
    -From the highest to the lowest bill, it calculates how many bills
    are needed, without using more bills than the ATM has
    -If the exact amount can't be given, it will end the operation
    -Asks for confirmation
    -Updates the bills quantity and the user's balance
    -Shows the withdrawn bills and saves the operation in the history
    Test case:
    -With a balance of 17337 and the ATM bills [6, 13, 27, 41], the
    user types 750 and Y: it gives 1 bill of $500, 1 of $200 and 1 of
    $50, the balance changes to 16587 and the bills to [5, 12, 27, 40]
    """
    balance = accounts[user][2]
    if balance < 50:
        print("Your balance is not enough to make a withdrawal")
        return
    if atm_total_cash_sum(bills_denominations, bills_quantity) == 0:
        print("The ATM has no cash available right now")
        return
    while True:
        withdraw_amount = input("Amount of money to be withdrawn: $")
        withdraw_amount = withdraw_amount.strip().replace(" ", "")
        withdraw_amount = withdraw_amount.replace(",", "").replace("$", "")
        if not withdraw_amount.isdigit():
            print("Only digits are accepted")
        else:
            withdraw_amount = int(withdraw_amount)
            if withdraw_amount <= 0:
                print("Amount must be greater than 0")
            elif withdraw_amount > balance:
                print("Amount to be withdrawn exceeds your balance")
            elif withdraw_amount % 50 != 0:
                print("Amount needs to be multiple of 50")
            elif withdraw_amount > atm_total_cash_sum(bills_denominations,
                                                      bills_quantity):
                print("Amount exceeds the total cash available in the ATM")
            else:
                break
    total_withdrawn_bills = []
    remaining_cash = withdraw_amount
    for i in range(len(bills_denominations)):
        bills_required = remaining_cash // bills_denominations[i]
        bills_given = min(bills_required, bills_quantity[i])
        total_withdrawn_bills.append(bills_given)
        remaining_cash = remaining_cash - bills_given * bills_denominations[i]
    if remaining_cash == 0:
        message = ("Are you sure you want to withdraw this quantity?: $"
                   + str(withdraw_amount) + " pesos")
        if keep_going(message):
            new_balance = balance - withdraw_amount
            for j in range(len(bills_denominations)):
                bills_quantity[j] -= total_withdrawn_bills[j]
            accounts[user][2] = new_balance
            print("You have withdrawn:")
            for k in range(len(total_withdrawn_bills)):
                if total_withdrawn_bills[k] > 0:
                    print("-", total_withdrawn_bills[k], "bills of",
                          "$" + str(bills_denominations[k]))
            print("TOTAL:", "$" + str(withdraw_amount), "pesos")
            save_operation(accounts[user][0], "WITHDRAWAL",
                           withdraw_amount, new_balance)
        else:
            print("OPERATION CANCELLED")
    else:
        print("The ATM cannot dispense that exact amount")


def deposit_cash(accounts, user, bills_denominations, bills_quantity):
    """
    Topics: arithmetic operators, conditionals, nested loops, lists,
    matrices, strings
    Inputs: The accounts data, the user, the bills denominations, the
    bills quantity and the number of bills of each type
    Outputs: The deposited bills and the total on screen
    Process:
    -Shows the accepted bills, taken from the bills denominations
    -Asks how many bills of each type the user is inserting and
    validates that it only has digits
    -Calculates the total money deposited
    -If no bills were inserted, it will end the operation
    -Asks for confirmation
    -Adds the bills to the bills quantity and the total to the balance
    -Shows the deposited bills and saves the operation in the history
    Test case:
    -With a balance of 1000, the user inserts 2 bills of $500, 1 of
    $200, 0 of $100 and 3 of $50 and types Y: it deposits $1350, the
    balance changes to 2350 and the bills to [8, 14, 27, 44]
    """
    print("\nAccepted bills:")
    for denomination in bills_denominations:
        print("- $" + str(denomination))
    print("Insert your bills...\n\n")
    total_deposited_bills = []
    total_money_deposited = 0
    balance = accounts[user][2]
    for i in range(len(bills_denominations)):
        while True:
            amount_of_bills = input("How many $" + str(bills_denominations[i])
                                    + " bills: ")
            amount_of_bills = amount_of_bills.strip().replace(" ", "")
            if amount_of_bills.isdigit():
                amount_of_bills = int(amount_of_bills)
                total_deposited_bills.append(amount_of_bills)
                total_money_deposited += (amount_of_bills
                                          * bills_denominations[i])
                break
            else:
                print("Only digits are accepted")
    if total_money_deposited == 0:
        print("No bills were inserted")
    else:
        message = ("You are about to deposit $" + str(total_money_deposited)
                   + " pesos\nDo you want to proceed?")
        if keep_going(message):
            for j in range(len(bills_quantity)):
                bills_quantity[j] += total_deposited_bills[j]
            new_balance = balance + total_money_deposited
            accounts[user][2] = new_balance
            print("You have deposited:")
            for k in range(len(total_deposited_bills)):
                if total_deposited_bills[k] > 0:
                    print("-", total_deposited_bills[k], "bills of",
                          "$" + str(bills_denominations[k]), "pesos")
            print("TOTAL DEPOSITED:",
                  "$" + str(total_money_deposited), "pesos")
            save_operation(accounts[user][0], "DEPOSIT",
                           total_money_deposited, new_balance)
        else:
            print("OPERATION CANCELLED")


def pin_change(accounts, user):
    """
    Topics: functions, conditionals, matrices
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
    Test case:
    -If Pedro's PIN is 3784 and he types 3784, then 5829 and the
    confirmation 5829, his PIN changes to 5829 and it prints
    "PIN changed successfully"
    -If he types a wrong current PIN, it prints "Incorrect PIN"
    """
    current_pin = read_pin("Current PIN: ")
    if current_pin != accounts[user][1]:
        print("Incorrect PIN")
        return
    pin_creation_tips()
    print("-Avoid using your current PIN")
    accounts[user][1] = ask_new_pin(current_pin)
    print("PIN changed successfully")


def atm_total_cash_sum(bills_denominations, bills_quantity):
    """
    Topics: arithmetic operators, loops, lists, return values
    Inputs: The bills denominations and the bills quantity
    Outputs: ATM current cash
    Process:
    -For each type of bill, it multiplies the denomination by the
    quantity and adds it to the total
    -It will return the total cash
    Test case:
    -atm_total_cash_sum([500, 200, 100, 50], [6, 13, 27, 41]) returns
    10350
    """
    total_cash = 0
    for i in range(len(bills_quantity)):
        total_cash = total_cash + bills_quantity[i] * bills_denominations[i]
    return total_cash


def atm_total_cash_show(bills_denominations, bills_quantity):
    """
    Topics: loops, lists, strings
    Inputs: The bills denominations and the bills quantity
    Outputs: The ATM cash on screen
    Process:
    -Prints how many bills of each type the ATM has
    -Prints the total cash in the ATM
    Test case:
    -atm_total_cash_show([500, 200, 100, 50], [6, 13, 27, 41]) prints
    "- 6 bills of $500" (and the other 3 types) and "TOTAL: $10350"
    """
    print("The total cash in the ATM is:\n")
    for i in range(len(bills_quantity)):
        print("-", bills_quantity[i], "bills of",
              "$" + str(bills_denominations[i]), "\n")
    total_cash = atm_total_cash_sum(bills_denominations, bills_quantity)
    print("TOTAL:", "$" + str(total_cash), "\n")


# ===================== Login and PIN functions ======================


def find_account(accounts, account_number):
    """
    Topics: loops, conditionals, matrices, return values
    Inputs: The accounts data and the account number
    Outputs: The user (row of the account in the accounts data) or -1
    Process:
    -Looks for the account number in the accounts data, row by row
    -If it finds it, it will return the row of the account
    -If no account has that number, it will return -1
    Test case:
    -If the accounts data has Pedro (row 0) and Alberto (row 1),
    find_account(accounts, "6742907529582104") returns 1 and
    find_account(accounts, "1234") returns -1
    """
    for i in range(len(accounts)):
        if accounts[i][0] == account_number:
            return i
    return -1


def authentication(accounts):
    """
    Topics: nested loops, conditionals, matrices, strings
    Inputs: The accounts data, the account number and the account PIN
    Outputs: The user (row of the account in the accounts data), -1 if
    the account is blocked or -2 if the user wants to go back
    Process:
    -Asks for the account number and removes spaces and dashes
    -If the user types E or e, it will return -2 to go back to the
    welcome menu
    -Looks for the account number in the accounts data
    -If the account does not exist, it will ask again
    -If the account is blocked, it will return -1
    -Asks for the PIN and gives up to 3 attempts
    -Returns the user if the PIN is correct
    -Blocks the account and returns -1 if the attempts are over
    Test case:
    -Typing 8649-0724-9072-4758 and the PIN 3784 returns 0 (Pedro)
    -Typing E returns -2
    -Typing Pedro's account and 3 wrong PINs blocks the account and
    returns -1
    """
    print("\nHello there!!")
    print("-Remember that your account number has 16 digits")
    print("-Do NOT use special characters other than '-' or blank spaces")
    print("You can write 'E' to go back")
    while True:
        attempts = 3
        account_number = input("\nAccount number: ").strip()
        account_number = account_number.replace(" ", "").replace("-", "")
        if account_number.upper() == "E":
            return -2
        user = find_account(accounts, account_number)
        if user == -1:
            print("ACCOUNT NOT FOUND")
        elif accounts[user][3]:
            return -1
        else:
            print("\n-Remember that your PIN is only composed of 4 digits "
                  "with no special characters")
            while True:
                account_pin = read_pin("\nAccount PIN: ")
                if account_pin == accounts[user][1]:
                    return user
                elif attempts == 1:
                    accounts[user][3] = True
                    return -1
                else:
                    attempts = attempts - 1
                    print("Incorrect PIN, you have", attempts, "left")


def read_pin(message):
    """
    Topics: external libraries, strings
    Inputs: The message to show and the PIN typed by the user
    Outputs: The PIN without blank spaces
    Process:
    -Shows the message and asks for the PIN, hiding it with asterisks
    -Removes the blank spaces from the PIN
    -It will return the PIN
    Test case:
    -If the user types 3784, the screen shows **** and it returns
    "3784"
    -If the user types 37 84, it returns "3784"
    """
    pin = pwinput.pwinput(message, mask="*").strip().replace(" ", "")
    return pin


def is_pin_weak(pin):
    """
    Topics: conditionals, strings
    Inputs: The PIN
    Outputs: True if the PIN is weak, False if it is not
    Process:
    -Checks if the PIN has the same digit four times
    -Checks if the PIN is an ascending or descending sequence
    -Checks if the PIN repeats a pair of digits
    -Checks if the PIN has two pairs of repeated digits
    -If any of them is true, it will return True
    Test case:
    -is_pin_weak("1111"), is_pin_weak("6789"), is_pin_weak("1212") and
    is_pin_weak("1122") return True
    -is_pin_weak("5829") returns False
    """
    if pin.count(pin[0]) == 4:
        return True
    elif pin in ASCENDING_DIGITS:
        return True
    elif pin in DESCENDING_DIGITS:
        return True
    elif pin[0:2] == pin[2:4]:
        return True
    elif pin[0] == pin[1] and pin[2] == pin[3]:
        return True
    else:
        return False


def pin_creation_tips():
    """
    Topics: functions, strings
    Inputs: No inputs
    Outputs: The tips for PIN creation on screen
    Process:
    -Prints the rules for a valid PIN
    -Prints examples of weak PINs that are not accepted
    Test case:
    -pin_creation_tips() prints the 6 tips, for example:
    "-Avoid repeating a pair of digits, e.g. 1212 or 6969"
    """
    print("\nTIPS FOR PIN CREATION:")
    print("-Remember that your PIN needs to have only 4 digits")
    print("-Try to avoid typing blank spaces")
    print("-Avoid using the same digit four times, e.g. 1111 or 0000")
    print("-Avoid ascending or descending sequences, e.g. 6789 or 4321")
    print("-Avoid repeating a pair of digits, e.g. 1212 or 6969")
    print("-Avoid using two pairs of repeated digits, e.g. 1122 or 7788")


def ask_new_pin(current_pin):
    """
    Topics: loops, nested conditionals, strings
    Inputs: The current PIN, the new PIN and the new PIN confirmation
    Outputs: The new PIN
    Process:
    -Asks for the new PIN and validates that it has 4 digits, is
    different from the current PIN and is not weak
    -Asks for the confirmation of the new PIN
    -If something is wrong, it will print a message and ask again
    -It will return the new PIN when everything is correct
    -For new accounts, the current PIN is an empty text, so that
    validation never blocks a valid PIN
    Test case:
    -ask_new_pin("3784"): if the user types 1111 (weak), then 3784
    (the same as the current PIN), then 5829 and the confirmation
    5829, it returns "5829"
    """
    while True:
        new_pin = read_pin("Create your new PIN: ")
        if new_pin.isdigit() and new_pin != current_pin and len(new_pin) == 4:
            if not is_pin_weak(new_pin):
                new_pin_confirmation = read_pin("New PIN confirmation: ")
                if new_pin != new_pin_confirmation:
                    print("Your PIN is different from the PIN confirmation")
                else:
                    return new_pin
            else:
                print("Your PIN is too easy to guess, check the tips above")
        else:
            print("\nInvalid PIN")


# ================ Registration and helper functions =================


def new_account(accounts):
    """
    Topics: loops, conditionals, strings, matrices, libraries
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
    Test case:
    -If the user types "  ana   lopez " and the PIN 5821 two times, it
    adds [new account number, "5821", 0, False, "Ana Lopez"] to the
    accounts data and shows the new account number with dashes
    """
    print("\nHello there!!\nLet's begin with your username\n")
    while True:
        new_username = " ".join(input("What is your name?: ").split())
        if new_username.replace(" ", "").isalpha():
            break
        else:
            print("Invalid Username\n")
    while True:
        new_account_number = str(random.randint(0, 9999999999999999)).zfill(16)
        if find_account(accounts, new_account_number) == -1:
            break
    formatted_username = new_username.title()
    print("\nHere we GO", formatted_username + "!", "\nLet's create your PIN!")
    pin_creation_tips()
    new_pin = ask_new_pin("")
    print("\nYour account number is",
          account_number_format(new_account_number),
          "\nYou have registered successfully!!")
    new_user = [new_account_number, new_pin, 0, False, formatted_username]
    accounts.append(new_user)


def account_number_format(account_number):
    """
    Topics: strings, return values
    Inputs: The account number
    Outputs: The account number with dashes
    Process:
    -Splits the account number into 4 groups of 4 digits
    -Joins the groups with dashes
    -It will return the account number with dashes
    Test case:
    -account_number_format("8649072490724758") returns
    "8649-0724-9072-4758"
    """
    return "-".join([account_number[:4], account_number[4:8],
                    account_number[8:12], account_number[12:]])


def keep_going(message):
    """
    Topics: loops, conditionals, strings
    Inputs: The message of the question and the user's answer
    Outputs: True if the answer is Y, False if the answer is N
    Process:
    -Shows the message and asks for Y or N
    -If the answer is not Y or N, it will ask again
    Test case:
    -If the user types x, it asks again, and if the user then types y,
    it returns True
    -If the user types N, it returns False
    """
    while True:
        answer = input(message + " (Y/N): ").strip().replace(" ", "")
        if answer.upper() == "Y":
            return True
        elif answer.upper() == "N":
            return False
        else:
            print("Invalid Option, please type Y or N")


# ========================== File functions ==========================


def save_operation(account_number, operation_type, amount,
                   balance_after_operation):
    """
    Topics: files, libraries, lists, loops, strings
    Inputs: The account number, the operation type, the amount and the
    balance after the operation
    Outputs: A new line in the history file
    Process:
    -Gets the current date and time of the operation
    -Converts all the data into text
    -Joins the data with commas
    -Adds the line at the end of the history file
    Test case:
    -save_operation("8649072490724758", "WITHDRAWAL", 750, 16587)
    adds this line at the end of history.txt (with the current date
    and time): 8649072490724758,WITHDRAWAL,750,16587,2026/11/26,13:40
    """
    operation_date = time.strftime("%Y/%m/%d")
    operation_time = time.strftime("%H:%M")
    operation_line = [account_number, operation_type, amount,
                      balance_after_operation, operation_date, operation_time]
    line = []
    for value in operation_line:
        line.append(str(value))
    file = open("history.txt", "a")
    file.write(",".join(line) + "\n")
    file.close()


def show_history(accounts, user):
    """
    Topics: files, error handling, loops, conditionals, strings
    Inputs: The accounts data and the user
    Outputs: The user's operations on screen
    Process:
    -Shows the user's account number with dashes
    -Reads the history file line by line
    -If the line belongs to the user, it will print the date, time,
    type, amount and balance after the operation
    -If the user has no operations, it will print a message
    -If the history file does not exist (FileNotFoundError), it means
    that no operations have been made yet, so it will print the same
    message
    Test case:
    -If history.txt has the line from the save_operation test case,
    for Pedro it prints: 2026/11/26 13:40 | WITHDRAWAL | $750 pesos |
    Balance after operation: $16587 pesos
    -If history.txt does not exist, it prints "No operations yet"
    """
    account_number = accounts[user][0]
    print("Transaction history for account",
          account_number_format(account_number) + ":\n")
    try:
        file = open("history.txt", "r")
        found = False
        for line in file:
            line = line.strip().split(",")
            if account_number in line:
                found = True
                print(line[4], line[5] + " | " + line[1] + " | $" + line[2]
                      + " pesos | Balance after operation: $" + line[3]
                      + " pesos")
        file.close()
        if not found:
            print("No operations yet")
    except FileNotFoundError:
        print("No operations yet")


def save_accounts(accounts):
    """
    Topics: files, nested loops, matrices, strings
    Inputs: The accounts data
    Outputs: The accounts file updated
    Process:
    -Opens the accounts file and rewrites it
    -For each account, converts all the data into text
    -Joins the data with commas and writes it as a line
    Test case:
    -If the accounts data is [["8649072490724758", "3784", 17337,
    False, "Pedro"]], accounts.txt is rewritten with only this line:
    8649072490724758,3784,17337,False,Pedro
    """
    file = open("accounts.txt", "w")
    for row in accounts:
        line = []
        for value in row:
            line.append(str(value))
        line_string = ",".join(line)
        file.write(line_string + "\n")
    file.close()


def load_accounts():
    """
    Topics: files, error handling, nested loops, conditionals,
    matrices, strings
    Inputs: No inputs
    Outputs: The accounts data (empty if the accounts file does not
    exist)
    Process:
    -Opens the accounts file and reads it line by line
    -Skips the empty lines of the file
    -Splits each line by commas into a list
    -Converts the balance into int and the blocked state into True or
    False
    -Adds each account to the accounts data
    -If the accounts file does not exist (FileNotFoundError), it will
    print a message and the accounts data will stay empty
    -It will return the accounts data
    Test case:
    -If accounts.txt only has the line
    8649072490724758,3784,17337,False,Pedro, it returns
    [["8649072490724758", "3784", 17337, False, "Pedro"]]
    -If accounts.txt does not exist, it prints a message and returns
    an empty list
    """
    accounts = []
    try:
        file = open("accounts.txt", "r")
        for line_in_file in file:
            if line_in_file.strip() != "":
                account_row = line_in_file.strip().split(",")
                for column in range(len(account_row)):
                    if column == 2:
                        account_row[column] = int(account_row[column])
                    elif column == 3:
                        account_row[column] = account_row[column] == "True"
                accounts.append(account_row)
        file.close()
    except FileNotFoundError:
        print("There are no accounts yet, please register first")
    return accounts


# =========================== Main program ===========================


def main():
    """
    Topics: loops, conditionals, match, functions, lists
    Inputs: The options selected by the user
    Outputs: The ATM program running
    Process:
    -Loads the accounts data from the file
    -Sets the bills quantity of the ATM, bills denominations are
    constant
    -Shows the welcome menu until the user exits
    -Option 1: logs in the user. If the login is correct, it shows the
    operations menu until the user logs out. If the account is
    blocked, it prints a message, and if the user typed E, it goes
    back to the welcome menu
    -Option 2: registers a new account
    -Option 3: ends the program
    -Saves the accounts data every time something changes
    Test case:
    -Choosing 1, typing Pedro's account and PIN, then 1 and N shows
    his balance and LOGGED OUT; then choosing 3 ends the program
    """
    accounts = load_accounts()
    bills_quantity = [6, 13, 27, 41]
    while True:
        welcome_menu()
        welcome_option = input("Choose an option: ").strip().replace(" ", "")
        match welcome_option:
            case "1":
                user = authentication(accounts)
                if user >= 0:
                    print("\n\nWelcome Back,", accounts[user][4])
                    while True:
                        operations_options_menu()
                        operation_option = input("Choose an option: ")
                        operation_option = operation_option.strip()
                        operation_option = operation_option.replace(" ", "")
                        match operation_option:
                            case "1":
                                consult_balance(accounts, user)
                            case "2":
                                withdraw_cash(accounts, user,
                                              BILLS_DENOMINATIONS,
                                              bills_quantity)
                            case "3":
                                deposit_cash(accounts, user,
                                             BILLS_DENOMINATIONS,
                                             bills_quantity)
                            case "4":
                                pin_change(accounts, user)
                            case "5":
                                show_history(accounts, user)
                            case "6":
                                atm_total_cash_show(BILLS_DENOMINATIONS,
                                                    bills_quantity)
                            case "7":
                                break
                            case _:
                                print("INVALID OPTION")
                        save_accounts(accounts)
                        message = "Would you like to do another operation?"
                        if not keep_going(message):
                            break
                    print("LOGGED OUT")
                elif user == -1:
                    print("ACCOUNT BLOCKED")
                else:
                    print("Returning to main menu...")
                save_accounts(accounts)
            case "2":
                new_account(accounts)
                save_accounts(accounts)
            case "3":
                break
            case _:
                print("INVALID OPTION")


main()

"""
ATM

ATM.py

Author: Omar Rolon

A Python program that simulates the operation of an automatic teller machine (ATM), modeling
both the user-facing interface and the internal logic behind it.

The system stores account numbers, PINs, balances, and the machine’s physical cash inventory.
Users authenticate with an account number and PIN, protected by a three-attempt limit that blocks
the account on failure. Once inside, a menu lets them check their balance, deposit cash, withdraw
cash, change their PIN, and review their transaction history.
"""

def menu():
    print("\n1)Consult Balance\n2)Withdraw Cash\n3)Deposit Cash\n4)PIN Change\n5)Transaction History\n6)Check current cash in the ATM\n7)Exit\n")

def consult_balance(data, access):
    """
    Inputs: The accounts data and the user
    Outputs: The user´s balance
    Process:
    -It will look for the user in the accounts data
    -It will return the balance of that user
    """
    return data[access][2]

def atm_total_cash(bills_denominations, bills_quantity):
    """
    Inputs: List of the bills denominations (500, 200, 100, 50 and 20) and list of the quantity of each bill
    Outputs: ATM current cash
    Process:
    -The current cash starts in 0
    -For each bill, current cash = current cash + denomination of the bill * quantity of the bill
    -It will return the current Cash
    """
    current_cash = 0
    for i in range(len(bills_denominations)):
        current_cash = current_cash + bills_denominations[i] * bills_quantity[i]
    return current_cash

def authentication(data):
    """
    Inputs: The accounts data, account number, account PIN
    Outputs: The user (position of the account in the data) or -1
    Process:
    -Asks the user for an account number
    -Validates if the account number only has digits
    -Validates if the account exists and if it is not blocked
    -Asks for the account PIN and gives up to 3 attempts
    -Returns the corresponding user if the PIN is correct
    -Blocks the account and returns -1 if the attempts are 0
    """
    while True:
        account_number = input("Account number: ")
        pin = -1
        user = -1
        attempts = 3
        if account_number.isdigit() == False:
            print("Invalid account number\n")
        else:
            account_number = int(account_number)
            while True:
                for i in range(len(data)):
                    if account_number == data[i][0]:
                        user = i
                        break
                if user == -1:
                    print("Account number does not exist in data\n")
                    break
                if data[user][3] == True:
                    print("Account Blocked\n")
                    break
                while 1<= attempts <= 3 and data[user][3] == False:
                    account_pin = input("\nAccount PIN: ")
                    for j in range(1):
                        if account_pin.isdigit() and int(account_pin) == data[user][1]:
                            return user
                    if pin == -1:
                        attempts = attempts - 1
                        if attempts == 0:
                            data[user][3] = True
                            return -1
                        print("Incorrect PIN, you have", attempts, "left")
                        break

def main():
    data = [
        #Account Number, PIN, Balance, Blocked, Name
        [86547234, 1234, 18337, False, "PEDRO"],
        [92341234, 4321, 14356, False, "ALBERTO"]
    ]
    bills_denominations = [500, 200, 100, 50, 20]
    bills_quantity = [6, 13, 27, 41, 20]
    while True:
        print("ATM\n\nWELCOME\n")
        access = authentication(data)
        if access != -1:
            print("\nWelcome Back,", data[access][4])
            menu()
            while True:
                option = input("Choose an option: ")
                if option.isdigit():
                    option = int(option)
                match option:
                    case 1:
                        print("Your balance is:", consult_balance(data, access), "pesos")
                    case 2:
                        print("Withdraw Cash")
                    case 3:
                        print("Deposit Cash")
                    case 4:
                        print("PIN Change")
                    case 5:
                        print("Transaction History")
                    case 6:
                        print("The total cash is:", atm_total_cash(bills_denominations, bills_quantity))
                    case 7:
                        break
                    case _:
                        print("Invalid Option")
        elif access == -1:
            print("Account Blocked\n")

main()

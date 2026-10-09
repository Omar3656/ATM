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

def consult_balance(access):
    """
    Inputs: The user
    Outputs: The user´s balance
    Process:
    -If the user is Pedro, it will return Pedro´s balance
    -If the user is Alberto, it will return Alberto´s balance
    """
    if access == user_1:
        return balance_1
    else:
        return balance_2
    
def atm_total_cash(cash_500, cash_200, cash_100, cash_50, cash_20):
    """
    Inputs: Total bills of 500, 200, 100, 50 and 20
    Outputs: ATM current cash
    Process:
    -The current cash = bills of 500 * 500 + bills of 200 * 200 + bills of 100 * 100 + bills of 50 * 50 + bills of 20 * 20
    -It will return the current Cash
    """
    current_cash = cash_500 * 500 + cash_200 * 200 + cash_100 * 100 + cash_50 * 50 + cash_20 * 20
    return current_cash
    
def authentication(account_number_1, account_number_2, account_pin_1, account_pin_2, blocked_1, blocked_2):
    """
    Inputs: account_pin_1, account_pin_2, blocked_1, blocked_2, account number, account PIN
    Outputs: user_1, user_2, or False
    Process:
    -Asks the user for an account number
    -Validates if the account exists and if it is not blocked
    -Asks for the account PIN and gives up to 3 attempts
    -Returns the corresponding user if the PIN is correct
    -Blocks the account and returns False if attempts reach 0
    """
    attempts = 3
    while True:
        account_number = int(input("Account number: "))
        while True:
            if account_number == account_number_1:
                while 1<= attempts <= 3 and blocked_1 == False:
                    account_pin = int(input("Account PIN: "))
                    if account_pin == account_pin_1:
                        return user_1
                    else:
                        attempts = attempts - 1
                        if attempts == 0:
                            blocked_1 = True
                            return False
                        else:
                            print("INCORRECT PIN, you have", attempts, " left")
                            break
            elif account_number == account_number_2:
                while 1<= attempts <= 3 and blocked_2 == False:
                    account_pin = int(input("Account PIN: "))
                    if account_pin == account_pin_2:
                        return user_2
                    else:
                        attempts = attempts - 1
                        if attempts == 0:
                            blocked_2 = True
                            return False
                        else:
                            print("INCORRECT PIN, you have", attempts, " left")
                            break
            else:
                print("Account number does not exist in data")
                break
            
def main():
    print("ATM\n\nWELCOME\n")
    while True:
        access = authentication(account_number_1, account_number_2, account_pin_1, account_pin_2, blocked_1, blocked_2)
        if access == user_1:
            print("\nWelcome Back,", user_1)
            menu()
            while True:
                option = int(input("Choose an option: "))
                match option:
                    case 1:
                        print("Your balance is:", consult_balance(access), "pesos")
                    case 2:
                        print("Withdraw Cash")
                    case 3:
                        print("Deposit Cash")
                    case 4:
                        print("PIN Change")
                    case 5:
                        print("Transaction History")
                    case 6:
                        print("The total cash is:", atm_total_cash(cash_500, cash_200, cash_100, cash_50, cash_20))
                    case 7:
                        break
                    case _:
                        print("Invalid Option")
        elif access == user_2:
            print("\nWelcome Back,", user_2)
            menu()
            while True:
                option = int(input("Choose an option: "))
                match option:
                    case 1:
                        print("Your balance is:", consult_balance(access), "pesos")
                    case 2:
                        print("Withdraw Cash")
                    case 3:
                        print("Deposit Cash")
                    case 4:
                        print("PIN Change")
                    case 5:
                        print("Transaction History")
                    case 6:
                        print("The total cash is:", atm_total_cash(cash_500, cash_200, cash_100, cash_50, cash_20))
                    case 7:
                        break
                    case _:
                        print("Invalid Option")
        else:
            print("Session Ended")
        
#User 1 information 
account_number_1 = 86547234
account_pin_1 = 1234
balance_1 = 7337
attempts_1 = 3
blocked_1=False
user_1 = "PEDRO"

#User 2 information
account_number_2 = 92341234
account_pin_2 = 4321
balance_2 = 14356
attempts_2 = 3
blocked_2=False
user_2 = "ALBERTO"

    #Current cash in the ATM
cash_500 = 6
cash_200 = 13
cash_100 = 27
cash_50 = 41
cash_20 = 20

main()

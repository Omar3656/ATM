"""
PROGRAMMING FUNDAMENTALS PROJECT

"""
#User 1 information
account_number_1=8492758294718255
account_pin_1=1234
balance_1=7337
blocked_1=False #Este lo usare luego maestra para cuando añade los 3 intentos con bucles, luego de los 3 intentos, este se cambiara a True
user_1="Pedro"

#Current cash in the ATM
cash_500 = 6
cash_200 = 13
cash_100 = 27
cash_50 = 41

def deposit_1(depositedmoney, blocked_1):
    if (user_1=="Pedro" and blocked_1==False and depositedmoney>0):
        newbalance=depositedmoney+balance_1
        return newbalance
    else:
        print("Error")
        return balance_1
        
def atm_total_cash(cash_500, cash_200, cash_100, cash_50):
    current_cash=cash_500*500+cash_200*200+cash_100*100+cash_50*50
    return current_cash
    
def menu():
    print("\n1)Consult Balance\n2)Withdraw Cash\n3)Deposit Cash\n4)PIN Change\n5)Transaction History\n6)Check current cash in the ATM\n7)Exit\n")
    
def authentication():
    user_account=int(input("Write 1 if you want to exit\n\nAccount Number: "))
    if (user_account==account_number_1):
        user_pin=int(input("Account PIN: "))
        if (user_pin==account_pin_1):
            return "User1"
        else:
            print("Incorrect PIN")
            return authentication()
    elif (user_account==1):
        return 1  
    else:
        print("USER ACCOUNT WAS NOT FOUND IN OUR SYSTEM\n")
        return authentication()
    
def main():
    print("ATM\n\nWELCOME\n")
    validation = authentication()
    if (validation=="User1"):
        print("Welcome back, ", user_1)
        menu()
        option=int(input("What operation would you like to do?: "))
        if option == 3:
            deposited_money=float(input("Money to be deposited: "))
            newbalance_1=deposit_1(deposited_money, blocked_1)
            print("Your new balance is ", newbalance_1)
        elif option==6:
            current_cash=atm_total_cash(cash_500, cash_200, cash_100, cash_50)
            print("The current cash in the ATM is in total: ", current_cash, "\n500 Bills:", cash_500,"\n200 Bills: ", cash_200, "\n100 Bills: ", cash_100, "\n50 Bills: ", cash_50)
        elif option==7:
            print("Session closed successfully")
        else:
            print("Error")
    else:
        print("You´ve finished your session")
main()
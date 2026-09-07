ATM

CONTEXT:

Automatic Teller Machines (ATMs) are essential components of modern financial infrastructure, used daily for many bank operations such as balance inquiries, deposit & withdrawals of cash, and transactions. Despite their frequent use, the operations and processes behind these machines are not often wondered by people.

The objective of this project is to develop a functional ATM UI simulation that models both user-facing operations and its internal operation logic. Some of the features I want to include are: user authentication, transaction logging (history), real-time cash inventory, optimal bank-note dispensation algorithm (handling $50, $100, $200, and $500 denominations based on available physical stock), and an operation to change your current PIN to a new one.

ALGORITHM:

The internal ATM digital system will already include the correct information such as the determined account number, the correct NIP for each account number, the available cash that the user has and the current storage of cash that the ATM has. Also, it´ll include a security system of PIN attempts and a timer will start at the beggining of a new account session, if the user does not interact with the UI the session will end

Inputs:
-User Account Number
-Account Number PIN
-Selected option from the main menu
-Amount of cash to withdraw 
-Amount of cash to deposit
-New PIN for PIN change operations
-Confirmation/Cancel/Return option
-New PIN confirmation

Process:

User´s authentication:
-Ask for the account Number
-Ask for the NIP
-Compare if account number exists in the ATM digital system
-Verify the PIN for the given account number
-Go to Menu if both are correct
-Display error message if one is incorrect (3 total attempts)
-If 3 attempts are used, block the account number and the session ends

Main Navigation Menu:
-Display the available options (Withdraw cash, Deposit Cash, Consult balance, PIN change, Transaction history, Exit)
-Ask for the operation to do
-Redirect the user to the process to be performed (User can decide whether cancel or keep going with the operation)

Main ATM processes:
Balance inquiry: Display the current balance --> Go to Menu
Withdrawal: Ask for the money to be withdrawn -> Validate if quantity is positive, multiple of $50, does not exceeds the balance and if ATM has the cash needed (If the conditionals are correct, keep going, otherwise, error message & go back to menu) -> Ask for confirmation -> Calculate the optimus combination of cash to be withdrawn (from higher to smaller denomination) -> Upgrade the ATM cash storage -> Upgrade user´s balance -> Register the transaction -> Display withdrawn money   -> Go to menu
Deposit: Ask for the money to be deposited -> Validate if its positive(If its positive, keep going, otherwise, error message & go back to menu) -> Ask for confirmation -> Update user´s balance -> Register the transaction -> Display deposited money -> Show remaining balance --> Go to menu
PIN change: Ask for the current PIN -> Ask for the new PIN -> Ask for the confirmation (If its correct, keep going, otherwise, error message & go back to menu) -> Upgrade PIN -> Go to Menu
Transactions History: Display the transaction history
Exit: Ends the session 

Outputs:
-Current user´s balance
-Messages of the operations for the user (Error messages, Operation messages, Confirmation messages)
-Transaction history
-Withdrawn/Deposited cash.

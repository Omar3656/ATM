# ATM
**Author:** Omar Rolon

## Context:

Automatic Teller Machines (ATMs) are essential components of modern financial infrastructure, used daily for many bank operations such as balance inquiries, deposits and withdrawals of cash, and transactions. Despite their frequent use, people rarely think about the operations and processes behind these machines.

The objective of this project is to develop a functional ATM simulation that models both the user-facing operations and the internal logic behind them. The program includes:

- User authentication with a PIN that is hidden with asterisks, 3 attempts and account blocking
- Registration of new accounts, with a unique 16-digit account number and a PIN that is not easy to guess
- Balance inquiry
- Cash withdrawals with a bill dispensing algorithm that uses $500, $200, $100 and $50 bills, from the highest to the lowest, based on the bills available in the ATM
- Cash deposits, where the user says how many bills of each type they insert
- PIN change
- Transaction history with the date and time of each operation
- Real-time cash inventory of the ATM
- Files to save the accounts and the history, so the information is kept after the program closes

## Solution:

To solve this, I made a Python program, `ATM.py`, that runs in the terminal. It has two menus: the welcome menu (Log in, Register and Exit) and the operations menu, with 7 options. This is how it solves each part of the problem:

- **Only the owner can use an account:** the program asks for the account number and the PIN. The PIN is hidden with asterisks while it is typed, using the library pwinput. After 3 wrong PINs the account is blocked, and it stays blocked because this is saved in `accounts.txt`.
- **The amounts must be correct:** before a withdrawal, the program checks that the amount only has digits, is greater than 0, is a multiple of $50, and is not more than the balance or the cash in the ATM. If something is wrong, it shows a message and asks again.
- **The ATM has a limited number of bills:** the program knows how many $500, $200, $100 and $50 bills the ATM has. To give the money, it starts with the biggest bill, uses as many as it can, and then goes to the next one. If it cannot give the exact amount, nothing changes. When the user makes a deposit, the bills are added to the ATM.
- **The information must not be lost:** the accounts are saved in `accounts.txt` after every operation, and every withdrawal and deposit is saved in `history.txt` with its date and time. When the program starts again, it reads the accounts from the file.
- **New users:** anyone can register with their name. The program creates a random 16-digit account number that no one else has, and it does not accept PINs that are easy to guess.
- **Typing mistakes:** the program accepts account numbers with dashes or spaces, amounts with commas or the `$` sign, and Y, N or E in lowercase. If the user types something wrong, it shows a message and asks again, so the program never stops because of a mistake. If one of the files is missing, it shows a message and keeps working.

## Requirements:

- Python 3.10 or newer, because the program uses `match` and `case`
- The external library **pwinput**, used to hide the PIN with asterisks while it is typed. Documentation: https://pypi.org/project/pwinput/
- The libraries `random` and `time` are also used, but they come with Python, so they do not need to be installed.
- The files `ATM.py`, `accounts.txt` and `history.txt` from this repository

## How to run:

These steps assume that Python 3.10 or newer is already installed. Everything is done from a terminal:

- **Windows:** use the Command Prompt. Press the Windows key, type `cmd` and press Enter.
- **macOS and Linux:** use the Terminal app.

**NOTE:** On Windows the command is `python` (or `py`). On macOS and Linux it is usually `python3`. Use the one that works on your computer in all the steps.

1. Check your Python version. It must be 3.10 or newer:

   ```
   python --version
   ```

2. Download the project and go into its folder. With Git:

   ```
   git clone https://github.com/Omar3656/atm.git
   cd atm
   ```

   If you do not have Git, you can download the 3 files with curl, which already comes with Windows 10 or newer and macOS:

   ```
   mkdir atm
   cd atm
   curl -O https://raw.githubusercontent.com/Omar3656/atm/main/ATM.py
   curl -O https://raw.githubusercontent.com/Omar3656/atm/main/accounts.txt
   curl -O https://raw.githubusercontent.com/Omar3656/atm/main/history.txt
   ```

3. Install the pwinput library:

   ```
   python -m pip install pwinput
   ```

4. Run the program from that same folder:

   ```
   python ATM.py
   ```

5. To close the program, choose option 3 (Exit) in the welcome menu.

**NOTE:** The program reads and writes `accounts.txt` and `history.txt` in the folder where the terminal is, so always run it from the project folder. If one of these files does not exist, the program still runs: it starts with no accounts or with an empty history, and it creates the file again when it needs it.

### Test accounts included in `accounts.txt`:

| Name | Account number | PIN |
|---|---|---|
| Pedro | 8649-0724-9072-4758 | 3784 |
| Alberto | 6742-9075-2958-2104 | 4873 |

**NOTE:** If an account gets blocked during the tests, open `accounts.txt` and change `True` to `False` in its line to unblock it.

## Algorithm:

The program keeps all the accounts in a matrix called `accounts`. Each row is one account with this order:

```
[account number, PIN, balance, blocked, name]
```

**Example:** `["8649072490724758", "3784", 17337, False, "Pedro"]`

So `accounts[user][2]` is the balance of the user. The cash of the ATM is stored in two lists: `BILLS_DENOMINATIONS = [500, 200, 100, 50]` and `bills_quantity = [6, 13, 27, 41]`, so the ATM starts with $10350. The accounts are saved in `accounts.txt`, and every withdrawal and deposit is saved in `history.txt`. The cash of the ATM is not saved in a file, so every time the program starts, the ATM has $10350 again.

### Inputs:
- Option of the welcome menu (from 1 to 3)
- Account number or `E` to go back
- PIN
- Option of the operations menu (from 1 to 7)
- Amount of money to withdraw
- Number of bills of each type to deposit
- Current PIN, new PIN and new PIN confirmation
- Name of the new user
- Confirmations with Y or N
- The files `accounts.txt` and `history.txt`

### Process:

**1. Start of the program**

- Loads the accounts from `accounts.txt`: each line is split by commas, the balance is converted into an integer and the blocked state into True or False. Empty lines are skipped.
- If `accounts.txt` does not exist, shows a message and starts with no accounts.
- Sets the bills of the ATM.
- Shows the welcome menu until the user chooses Exit.

**2. Log in**

- Asks for the account number and removes the spaces and dashes.
- If the user types `E`, it goes back to the welcome menu.
- Looks for the account number in the accounts matrix. If it does not exist, shows `ACCOUNT NOT FOUND` and asks again.
- If the account is blocked, shows `ACCOUNT BLOCKED` and goes back to the welcome menu.
- Asks for the PIN, hidden with asterisks. The user has 3 attempts.
- If the PIN is correct, shows the operations menu.
- If the 3 attempts fail, blocks the account and saves it in `accounts.txt`, so it stays blocked.

**3. Register**

- Asks for the name. It can only have letters and spaces. Extra spaces are removed and the first letter of each word is written in capitals.
- Creates a random 16-digit account number, repeating it until it does not belong to another account.
- Shows the tips to create a PIN.
- Asks for the PIN and its confirmation. The PIN must have 4 digits and must not be weak. A PIN is weak if:
  - It has the same digit four times (1111)
  - It is an ascending or descending sequence (6789 or 4321)
  - It repeats a pair of digits (1212)
  - It has two pairs of repeated digits (1122)
- Shows the new account number with dashes, adds the account to the matrix and saves it in `accounts.txt`.

**4. Operations menu**

After every operation (except Exit), the accounts are saved in `accounts.txt` and the program asks if the user wants to do another operation.

- **Consult balance:** shows the balance of the user.
- **Withdraw cash:**
  1. If the balance is less than $50 or the ATM has no cash, ends the operation.
  2. Asks for the amount and removes spaces, commas and the `$` sign.
  3. Checks that the amount only has digits, is greater than 0, does not exceed the balance, is a multiple of 50 and does not exceed the cash of the ATM. If something is wrong, shows a message and asks again.
  4. Calculates the bills from the highest to the lowest. For each type of bill:
     - `bills_required = remaining_cash // bill`
     - `bills_given = min(bills_required, bills available in the ATM)`
     - `remaining_cash = remaining_cash - bills_given * bill`
  5. If the remaining cash is not 0, shows `The ATM cannot dispense that exact amount` and ends the operation.
  6. Asks for confirmation. If the user types N, shows `OPERATION CANCELLED`.
  7. Subtracts the bills from the ATM and the amount from the balance.
  8. Shows the bills given and the total, and saves the operation in `history.txt` with its date and time.
- **Deposit cash:**
  1. Shows the accepted bills.
  2. Asks how many bills of each type the user is inserting. Only digits are accepted.
  3. Calculates the total: the number of bills of each type multiplied by its value.
  4. If the total is 0, shows `No bills were inserted` and ends the operation.
  5. Asks for confirmation. If the user types N, shows `OPERATION CANCELLED`.
  6. Adds the bills to the ATM and the total to the balance.
  7. Shows the bills deposited and the total, and saves the operation in `history.txt`.
- **PIN change:**
  1. Asks for the current PIN. If it is wrong, shows `Incorrect PIN` and ends the operation.
  2. Shows the tips to create a PIN.
  3. Asks for the new PIN, with the same rules as in the registration. It must also be different from the current PIN.
  4. Asks for the confirmation, updates the PIN and shows `PIN changed successfully`.
- **Transaction history:** reads `history.txt` line by line and shows the operations of the user (date, time, type, amount and balance after the operation). If there are none, or the file does not exist, shows `No operations yet`.
- **Check current cash in the ATM:** shows how many bills of each type the ATM has and the total.
- **Exit:** logs out and goes back to the welcome menu.

**5. End of the program**

- When the user chooses Exit in the welcome menu, the program ends.

### Outputs:
- Balance of the user
- Messages for the user, such as error messages, confirmation messages and operation messages
- Bills withdrawn or deposited, and the total of the operation
- Transaction history of the user
- Cash available in the ATM
- Account number of new users, with dashes
- Updated files: `accounts.txt` and `history.txt`

## Tests:

Each test starts with the original `accounts.txt` and `history.txt` of this repository. The tests change these files, so to repeat them, restore the files with `git checkout accounts.txt history.txt`, or download them again with the curl commands of step 2.

| # | What to do | Expected result |
|---|---|---|
| 1 | Log in with Pedro and choose 1 | `Your balance is $17337 pesos` |
| 2 | Log in with Pedro, choose 2, type 750 and then Y | Gives 1 bill of $500, 1 bill of $200 and 1 bill of $50 (`TOTAL: $750 pesos`). Pedro's balance is now $16587 |
| 3 | Log in with Pedro, choose 2 and type 125, then 20000, then 10400 | `Amount needs to be multiple of 50`, then `Amount to be withdrawn exceeds your balance`, then `Amount exceeds the total cash available in the ATM` |
| 4 | Log in with Alberto, choose 3, type 2, 1, 0 and 3 bills, and then Y | `TOTAL DEPOSITED: $1350 pesos`. Alberto's balance is now $22506 |
| 5 | Log in with Pedro and choose 6 | The bills of the ATM, from `- 6 bills of $500` to `- 41 bills of $50`, and `TOTAL: $10350` |
| 6 | Do test 2, answer Y to do another operation and choose 5 | The withdrawal with its date and time: `WITHDRAWAL \| $750 pesos \| Balance after operation: $16587 pesos` |
| 7 | Choose 1 and type the account 1234-5678-1234-5678 | `ACCOUNT NOT FOUND` |
| 8 | Log in with Pedro's account and type 3 wrong PINs | `Incorrect PIN, you have 2 left`, then `1 left`, and then `ACCOUNT BLOCKED` |
| 9 | Choose 2 (Register), type the name `ana   lopez` (in lowercase and with extra spaces), the PIN 1111, and then 5821 two times | `Your PIN is too easy to guess, check the tips above`, then the new account number with dashes. The account is saved as Ana Lopez |
| 10 | Choose 9 in the welcome menu | `INVALID OPTION` |

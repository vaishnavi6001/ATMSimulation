# current data in accounts.csv:
# Account Number   PIN  Balance
# 1               1234     1000
# 2               1111     2000
# 3               1010     3000
# 4               4444     4000
# 5               2222     5000
# 6               2021     6000
# 7               1478     7000
# 8               2589     2000
# 9               2345     3000
# 20              1000     1000
# 100             1234      100

import pandas as pd
from constants import *  # constants file
num = 0
try:
    data = pd.read_csv('accounts.csv')
except FileNotFoundError:
    print("Update file path. ")
    exit()
data.set_index('Account Number', inplace=True)


class Account:
    def __init__(self, pin, current_balance, account_number):
        self.pin = pin
        self.current_balance = current_balance
        self.account_number = account_number

    def send_money(self, recipient, amount):
        self.current_balance -= amount
        recipient.current_balance += amount
        data.loc[self.account_number, 'Balance'] = self.current_balance
        data.loc[recipient.account_number, 'Balance'] = recipient.current_balance

    def deposit_money(self, amount):
        self.current_balance += amount
        data.loc[self.account_number, 'Balance'] = self.current_balance

    def withdraw_money(self, amount):
        self.current_balance -= amount
        data.loc[self.account_number, 'Balance'] = self.current_balance

    def display_balance(self):
        print("Your current balance is", self.current_balance)


# own exception classes-
class NegativeNumberError(Exception):
    """Raised when number entered is negative when it should be positive."""
    pass


class NotInRangeError(Exception):
    """Raised when number entered does not lie within permissible range."""
    pass


class AmountExceedsBalanceError(Exception):
    """Raised when amount entered for sending/withdrawal is greater than balance."""
    pass


class WrongPinError(Exception):
    """Raised when PIN entered is wrong."""
    pass


def exit_or_try_again():
    print("Press 1 to exit. Press any other key to try again.")
    if input() == 1:
        exit()
    else:
        print("Enter a valid input this time: ")
        return True


def find_account(account_no1):
    pin0 = 0
    balance0 = 0
    if account_no1 in data.index:
        pin0 = data.PIN[account_no1]
        balance0 = data.Balance[account_no1]
    return Account(pin0, balance0, account_no1)


def input_acc_num():
    while check_acc:
        try:
            acc_num = int(input())
            if acc_num < 0:
                raise NegativeNumberError
        except NegativeNumberError:
            print("Account number cannot be negative. Please try again.")
            if exit_or_try_again():
                continue
        except ValueError:
            print("Enter a valid account number. Your account number consists only of numbers.")
            if exit_or_try_again():
                continue
        return acc_num


def input_amount_sw():
    while check_amount:
        try:
            amt = int(input())
            if amt < 0:
                raise NegativeNumberError
            if amt > p1.current_balance:
                raise AmountExceedsBalanceError
        except NegativeNumberError:
            print("Amount cannot be negative. Please try again.")
            if exit_or_try_again():
                continue
        except AmountExceedsBalanceError:
            print("The amount you have entered is greater than your current balance. ")
            if exit_or_try_again():
                continue
        except ValueError:
            print("Amount can consist only numbers. Please try again.")
            if exit_or_try_again():
                continue
        return amt


def input_amount_dep():
    while check_amount:
        try:
            amt4 = int(input("Enter amount to be deposited: "))
            if amt4 < 0:
                raise NegativeNumberError
        except ValueError:
            print("Invalid amount. Please enter a number.")
            if exit_or_try_again():
                continue
        except NegativeNumberError:
            print("Amount cannot be negative. Please enter a positive number.")
            if exit_or_try_again():
                continue
        return amt4


def input_pin():
    while check_pin:
        try:
            pin = int(input("Enter PIN (it is a number):\n"))
            if pin < 0:
                raise NegativeNumberError
        except NegativeNumberError:
            print("PIN cannot be negative.")
            if exit_or_try_again():
                continue
        except ValueError:
            print("PIN is a number. Please enter a number.")
            if exit_or_try_again():
                continue
        return pin


def new_acc_no(new_no):
    num2 = new_no
    while num2 in data.index:
        print("Account number already exists. Please enter another number.")
        num2 = input_acc_num()
    return num2


while True:
    data.sort_index(inplace=True)
    data.to_csv('accounts.csv')
    try:
        num = int(input('''
Press 1 to send money
Press 2 to create a new account
Press 3 to display your balance
Press 4 to deposit money
Press 5 to withdraw money
Press 6 to exit \n'''))
        if num < 0 or num > 6:
            raise NotInRangeError
    except ValueError:
        print("Invalid input.")
    except NotInRangeError:
        print("Enter a number in range.")
        continue
    if num == CREATE_ACC:
        print("Enter an account number which does not already exist: ")
        new_account = input_acc_num()
        new_account_no = new_acc_no(new_account)
        new_pin = input_pin()
        new_amount = input_amount_dep()
        data.loc[int(new_account_no)] = [new_pin, new_amount]
        print("Your account number is", new_account_no, "and your current balance is ₹", new_amount)

    elif 0 < num < 6 and num != CREATE_ACC:
        while True:
            print("Enter your account number: ")
            account_no = input_acc_num()
            p1 = find_account(account_no)
            if p1.pin == 0 & p1.current_balance == 0:
                print("Enter a valid account number.")
                continue
            break
        while True:
            pin1 = input_pin()
            try:
                if pin1 == p1.pin:
                    if num == SEND_MONEY:
                        while True:
                            print("Enter recipient's account number: ")
                            acc_rec = input_acc_num()
                            rec = find_account(acc_rec)
                            if rec.pin == 0 & rec.current_balance == 0:
                                print("Enter a valid account number.")
                                continue
                            if rec.account_number == p1.account_number:
                                print("You cannot send money to yourself. Enter another existing account number.")
                                continue
                            break
                        p1.display_balance()
                        print("Enter amount to be sent: ")
                        amount1 = input_amount_sw()
                        p1.send_money(rec, amount1)
                        p1.display_balance()

                    if num == DISPLAY_BALANCE:
                        p1.display_balance()

                    if num == DEPOSIT_MONEY:
                        amount4 = input_amount_dep()
                        p1.deposit_money(amount4)
                        p1.display_balance()

                    if num == WITHDRAW_MONEY:
                        print("Enter amount to be withdrawn: ")
                        amount5 = input_amount_sw()
                        p1.withdraw_money(amount5)
                        p1.display_balance()
                    break
                else:
                    raise WrongPinError
            except WrongPinError:
                print("The pin you have entered is wrong. Please enter the right key in the next try.")
                continue
    elif num == EXIT:
        print("Thank you for visiting our ATM.")
        exit()
    data.to_csv('accounts.csv')

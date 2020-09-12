# Write your code here
# Write your code here
from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()
c.execute('DELETE FROM card')
conn.commit()
def data_entry(card_number, card_pin):
    c.execute('INSERT INTO card(number, pin) VALUES({number}, {pin})'.format(number=card_number, pin=card_pin))
    conn.commit()

class Account():
    card_numbers = [""]
    card_pins = []
    def __init__(self):
        self.acc_number = None
        self.acc_pin = None
        self.balance = 0

    def log_in_acc(self):
        print("Enter your card number:")
        trial_acc_num = input()
        print("Enter your PIN")
        trial_acc_pin = input()
        found = False
        for i in Account.card_numbers:
            for x in Account.card_pins:
                if str(i) == str(trial_acc_num) and str(x) == str(trial_acc_pin):
                    print("\nYou have successfully logged in!\n")
                    found = True
                    self.acc_number = i
                    self.acc_pin = x
                    return self.print_acc_screen()
        if not found:
            print("\nWrong card number or PIN!\n")
            return self.print_home_screen()


    def creat_acc_num(self):
        acc_num = [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(acc_num)):
            if i > 5:
                acc_num[i] = randint(0, 9)
        return acc_num

    def digitSum(self):
        number = self.creat_acc_num()
        oddSum = 0
        evenSum = 0
        total = 0
        for i in number[1::2]:
            oddSum += i
        for i in number[0::2]:
            temp_i = 0
            temp_i = i * 2
            if temp_i > 9:
                temp_i -= 9
            evenSum += temp_i
        total = evenSum + oddSum
        if total % 10 == 0:
            self.create_acc(number)
        else:
            self.digitSum()
    def check_account_number(self):
        print("Transfer\nEnter card number: ")
        acc_number = input()
        if acc_number == self.acc_number:
            print("You can't transfer to the same account!")
            self.print_acc_screen()
        else:
            oddSum = 0
            evenSum = 0
            total = 0
            for i in acc_number[1::2]:
                oddSum += int(i)
            for i in acc_number[0::2]:
                temp_i = 0
                temp_i = int(i) * 2
                if temp_i > 9:
                    temp_i -= 9
                evenSum += temp_i
            total = evenSum + oddSum
            if total % 10 == 0 and acc_number in Account.card_numbers:
                self.transfer_money(acc_number)
            elif acc_number not in Account.card_numbers and total % 10 == 0:
                print("Such a card does not exist.")
                self.print_acc_screen()
            else:
                print("Probably you made a mistake in the card number. Please try again!")
                self.print_acc_screen()

    def create_acc(self, acc_number):
        self.acc_number = acc_number
        self.acc_number = [str(i) for i in self.acc_number]
        self.acc_number = ''.join(self.acc_number)
        self.acc_pin = randint(1000, 9999)
        print("\nYour card has been created")
        print(f"Your card number: \n{self.acc_number}")
        print(f"Your card PIN: \n{self.acc_pin}\n")
        Account.card_numbers.append(self.acc_number)
        Account.card_pins.append(self.acc_pin)
        data_entry(self.acc_number, self.acc_pin)
        self.print_home_screen()

    def print_balance(self):
        print(c.execute('SELECT balance FROM card WHERE number = {acc_number}'.format(acc_number = self.acc_number)).fetchone())
        self.print_acc_screen()

    def close_account(self, account_number):
        c.execute('DELETE FROM card WHERE number = {account_number}'.format(account_number = self.acc_number))
        conn.commit()
        for i in Account.card_numbers:
            for x in Account.card_pins:
                if i == self.acc_number:
                    Account.card_numbers.remove(i)
                    Account.card_pins.remove(x)

    def add_income(self):
        print("\nEnter income: ")
        user_money = int(input())
        c.execute('UPDATE card SET balance = balance + {amount_to_add} WHERE number = {user_acc_number}'.format(amount_to_add = user_money, user_acc_number = self.acc_number))
        conn.commit()
        self.balance += user_money
        print("Income was added!\n")

    def transfer_money(self,account_being_transferred_to):
        print("Enter how much money you want to transfer: ")
        transfer_amount = int(input())
        if transfer_amount > self.balance:
            print("Not enough money!\n")
            self.print_acc_screen()
        else:
            print("Success!\n")
            self.balance -= transfer_amount
            c.execute('UPDATE card SET balance = balance + {transfer_money} WHERE number = {account_to_be_transferred_to}'.format(transfer_money = transfer_amount, account_to_be_transferred_to = account_being_transferred_to))
            conn.commit()
            c.execute('UPDATE card SET balance = balance - {transfer_money} WHERE number = {account_being_transferred_from}'.format(transfer_money = transfer_amount, account_being_transferred_from = self.acc_number))
            conn.commit()
            self.print_acc_screen()

    def print_acc_screen(self):
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")

        user_input = int(input())
        if user_input == 0:
            print("Bye!")
            return None
        elif user_input == 1:
            print(self.print_balance())

        elif user_input == 2:
            self.add_income()
            self.print_acc_screen()

        elif user_input == 3:
            self.check_account_number()

        elif user_input == 4:
            self.close_account(self.acc_number)
            print("The account has been closed!")
            self.print_home_screen()
        else:
            print("You have successfully logged out!")
            self.print_home_screen()

    def print_home_screen(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        user_choice = int(input())
        if user_choice == 0:
            print(" \nBye!")
            return None
        elif user_choice == 2:
            self.log_in_acc()
        else:
            self.digitSum()

trial_user = Account()
trial_user.print_home_screen()

from typing import List


class Transaction:
    def __init__(self, amount: float, type: str):
        """Create a new Transaction object with the given amount and type

        Args:
            amount (float): Dollar (or other currency) amount of the Transaction
            type (str): Type of Transaction ("Deposit" or "Withdrawl")
        """
        self.amount = amount
        self.type = type


class BankAccount:
    def __init__(self, number: str, owner: str, balance: float):
        """Create a new BankAccount object with the given account number, owner and starting balance, as well as empty list of Transactions

        Args:
            number (str): Account number for BankAccount
            owner (str): Name of Customer that owns BankAccount
            balance (float): Current currency balance in BankAccount
        """
        self.number = number
        self.owner = owner
        self.balance = balance
        self.transactions: List[Transaction] = []

    def deposit(self, amount: float):
        """Deposit an amount into BankAccount by creating a new "Deposit" type Transaction with given amount

        Args:
            amount (float): Currency amount to deposit
        """
        self.balance += amount
        self.transactions.append(Transaction(amount, "Deposit"))

    def withdraw(self, amount: float):
        """Withdraw a given amount from BankAccount by creating a new "Withdrawal" type Transaction with given amount after checking that BankAccount contains at least that amount

        Args:
            amount (float): Currency amount to attempt to withdraw

        Returns:
            None or str: None if withdrawal successful or "Insufficient funds" string if BankAccount does not contain at least given amount "amount"
        """
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(Transaction(amount, "Withdrawal"))
        else:
            return "Insufficient funds"


class Customer:
    def __init__(self, name: str, account: BankAccount):
        """Create a new Customer object with the given name and owned BankAccount

        Args:
            name (str): Customer's name
            account (BankAccount): BankAccount owned by Customer
        """
        self.name = name
        self.account = account


class Bank:
    def __init__(self):
        """Create a new Bank object with an empty list of Customers"""
        self.customers: List[Customer] = []

    def add_customer(self, customer: Customer):
        """Add a Customer to Bank's list of Customers

        Args:
            customer (Customer): Customer to add to Bank's list of Customers
        """
        self.customers.append(customer)

    def remove_customer(self, customer: Customer):
        """Remove a Customer from Bank's list of Customers

        Args:
            customer (Customer): Customer to remove
        """
        self.customers.remove(customer)


##### TESTS BELOW #####


import unittest

# imports commented out for testing in same file
# import Transaction
# import BankAccount
# import Customer
# import Bank


class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()

    def test_add_customer(self):
        customer = Customer("John Doe", BankAccount(12345, "John Doe", 1000))
        self.bank.add_customer(customer)
        self.assertEqual(len(self.bank.customers), 1)

    def test_remove_customer(self):
        customer = Customer("John Doe", BankAccount(12345, "John Doe", 1000))
        self.bank.add_customer(customer)
        self.bank.remove_customer(customer)
        self.assertEqual(len(self.bank.customers), 0)


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer_account = BankAccount(12345, "John Doe", 1000)
        self.customer = Customer("John Doe", self.customer_account)

    def test_name(self):
        self.assertEqual(self.customer.name, "John Doe")

    def test_account(self):
        self.assertEqual(self.customer.account.balance, 1000)


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount(12345, "John Doe", 1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw(self):
        self.account.withdraw(500)
        self.assertEqual(self.account.balance, 500)

    def test_insufficient_funds(self):
        msg = self.account.withdraw(2000)
        self.assertEqual("Insufficient funds", msg)
        self.assertEqual(self.account.balance, 1000)

    def test_transaction_history(self):
        self.assertEqual(len(self.account.transactions), 0)
        self.account.deposit(500)
        self.account.withdraw(500)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[0].type, "Deposit")
        self.assertEqual(self.account.transactions[1].type, "Withdrawal")


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction(500, "Deposit")

    def test_amount(self):
        self.assertEqual(self.transaction.amount, 500)

    def test_type(self):
        self.assertEqual(self.transaction.type, "Deposit")


if __name__ == "__main__":
    unittest.main()

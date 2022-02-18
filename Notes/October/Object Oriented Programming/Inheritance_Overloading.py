"""]
Created on Tue Oct 26 13:52:17 2021

@author: asianinvasion
"""

class Account:
    
    """ Account Class for our ebank website """
    
    def __init__(self, name, opening_balance = 0.0):
        """ Initialize a user account """
        self.name = name
        self.balance = opening_balance
        self.transactions = [('Starting', opening_balance, opening_balance)]
        
    def deposit(self, amount):
        """ Despoit funds into the account """
        self.balance += amount
        self.transactions.append(("Deposit", amount, self.balance))
        
    def withdraw(self, amount):
        """ Withdraw funds from the account """
        if amount > self.balance:
            raise ValueError("Account Balance Exceeded")
        
        self.balance -= amount
        self.transactions.append(("Withdraw", -amount, self.balance))
        
    def get_balance(self):
        """ Accessor method: get the balance amount """
        return self.balance
    
    def print_transactions(self):
        """ Print all historical transactions """
        print("\n", self)
        for type_trans, amt, bal in self.transactions:
            print(f'{type_trans:10} {amt:9.2f} {bal:9.2f}')
            
class Bank:
    
    def __init__(self):
        """ Constructor """
        self.accounts = {}
    
    def open_account(self, acct, starting_balance = 0.0):
        """ Open a new account with an optional starting balance """
        a =  Account(acct, starting_balance)
        self.accounts[acct] = a
        # Create a new account, add it to self.accounts under key 'act'
        # This usage of other classes is called COMPOSITION 
    
    def deposit(self, acct, amt):
        """ Deposit funds to a named account """
        self.accounts[acct].deposit(amt)
    
    def withdraw(self, acct, amt):
        """ Withdraw funds to a named account """
        self.accounts[acct].withdraw(amt)
        
    def transfer(self, from_acct, to_acct, amt):
        """ Transfer funds between accounts """
        self.withdraw(from_acct, amt)
        self.deposit(to_acct, amt)
        
    def print_statement(self):
        """ Print statement """
        for acct in self.accounts:
            self.accounts[acct].print_transactions()


#%% Oeprator Overloading

class Vector:
    
    def __init__(self, *components):
        """ vector constructor """
        self._components = list(components)
        
    def mag(self):
        """ Magnitude of the vector """
        return sum([c**2 for c in self._components]) ** .5
    
    def dim(self):
        """ Dimensions of the vector"""
        return len(self._components)
    
    def __getitem__(self, i):
        """ Use indexing to fetch the ith vector component """
        return self._components[i]
    
    def __add__(self, other):
        """ Add two vectors. Accomodate different dimensions """
        copy = self[:]
        for i in range(other.dim()):
            if i < len(copy):
                copy[i] += other[i]
            else:
                copy.append(other[i])
    
    def __mul__(self, other):
        """ Dot or scalar product of two vectors. Must determine if 
            Other is a vector object or just a scalar. """
        if type(other) == Vector:
            mindim = min(self.dim(), other.dim())
            return 
        elif type(other) == int or type(other) == float:
            return
    
def main():
    """ Test Methods """
    
    
    
    
    
    
    
    
    
    
        
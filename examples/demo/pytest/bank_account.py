class BankAccount:
    def __init__(self, balance: float = 0.0):
        if balance < 0:
            raise ValueError("initial balance cannot be negative")
        self.balance = balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("withdraw amount must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        return self.balance


def transfer(source: BankAccount, target: BankAccount, amount: float) -> tuple[float, float]:
    if source is target:
        raise ValueError("cannot transfer to same account")
    source.withdraw(amount)
    target.deposit(amount)
    return source.balance, target.balance

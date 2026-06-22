public class BankAccount {
    private String accountNumber;
    private double balance;
    private boolean isActive;

    public BankAccount(String accountNumber, double initialBalance) {
        if (accountNumber == null || accountNumber.trim().isEmpty()) {
            throw new IllegalArgumentException("Account number cannot be empty");
        }
        if (initialBalance < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative");
        }
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.isActive = true;
    }

    public void deposit(double amount) {
        checkActive();
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive");
        }
        this.balance += amount;
    }

    public void withdraw(double amount) {
        checkActive();
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdraw amount must be positive");
        }
        if (this.balance < amount) {
            throw new IllegalStateException("Insufficient funds");
        }
        this.balance -= amount;
    }

    public void transfer(BankAccount targetAccount, double amount) {
        checkActive();
        if (targetAccount == null) {
            throw new IllegalArgumentException("Target account cannot be null");
        }
        if (!targetAccount.isActive()) {
            throw new IllegalStateException("Target account is inactive");
        }
        
        this.withdraw(amount);
        targetAccount.deposit(amount);
    }

    public void deactivate() {
        if (this.balance > 0) {
            throw new IllegalStateException("Cannot deactivate account with non-zero balance");
        }
        this.isActive = false;
    }

    public double getBalance() {
        return this.balance;
    }

    public String getAccountNumber() {
        return this.accountNumber;
    }

    public boolean isActive() {
        return this.isActive;
    }

    private void checkActive() {
        if (!this.isActive) {
            throw new IllegalStateException("Account is inactive");
        }
    }
}

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    private static final double DELTA = 0.001;

    // TC-001: Create active account with valid data
    @Test
    void testCreateActiveAccount_TC001() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals("ACC123", account.getAccountNumber());
        assertEquals(1000.0, account.getBalance(), DELTA);
        assertTrue(account.isActive());
    }

    // TC-002: Constructor throws when account number is empty
    @Test
    void testConstructorEmptyAccountNumber_TC002() {
        assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("   ", 100.0);
        });
    }

    // TC-003: Constructor throws when initial balance is negative
    @Test
    void testConstructorNegativeBalance_TC003() {
        assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("ACC001", -50.0);
        });
    }

    // TC-004: getAccountNumber returns the value set at construction
    @Test
    void testGetAccountNumber_TC004() {
        BankAccount account = new BankAccount("ACC999", 0.0);
        assertEquals("ACC999", account.getAccountNumber());
    }

    // TC-005: getBalance returns the value set at construction
    @Test
    void testGetBalance_TC005() {
        BankAccount account = new BankAccount("ACC100", 250.75);
        assertEquals(250.75, account.getBalance(), DELTA);
    }

    // TC-006: isActive reflects active flag set at construction
    @Test
    void testIsActiveFlag_TC006() {
        BankAccount account = new BankAccount("ACC200", 0.0);
        assertTrue(account.isActive());
    }

    // TC-007: Deposit positive amount updates balance
    @Test
    void testDepositPositiveAmount_TC007() {
        BankAccount account = new BankAccount("ACC300", 500.0);
        account.deposit(200.0);
        assertEquals(700.0, account.getBalance(), DELTA);
    }

    // TC-008: Deposit zero or negative amount throws IllegalArgumentException
    @Test
    void testDepositNonPositiveAmount_TC008() {
        BankAccount account = new BankAccount("ACC400", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0));
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-10.0));
    }

    // TC-009: Withdraw amount less than balance succeeds
    @Test
    void testWithdrawWithinBalance_TC009() {
        BankAccount account = new BankAccount("ACC500", 400.0);
        account.withdraw(150.0);
        assertEquals(250.0, account.getBalance(), DELTA);
    }

    // TC-010: Withdraw amount greater than balance throws IllegalStateException
    @Test
    void testWithdrawExceedBalance_TC010() {
        BankAccount account = new BankAccount("ACC600", 100.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> account.withdraw(150.0));
        assertEquals("Insufficient funds", ex.getMessage());
    }

    // TC-011: Withdraw zero or negative amount throws IllegalArgumentException
    @Test
    void testWithdrawNonPositiveAmount_TC011() {
        BankAccount account = new BankAccount("ACC700", 200.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(0));
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-20.0));
    }

    // TC-012: Transfer to active target account succeeds
    @Test
    void testTransferSuccess_TC012() {
        BankAccount source = new BankAccount("SRC001", 300.0);
        BankAccount target = new BankAccount("TGT001", 100.0);
        source.transfer(target, 150.0);
        assertEquals(150.0, source.getBalance(), DELTA);
        assertEquals(250.0, target.getBalance(), DELTA);
    }

    // TC-013: Transfer with null target throws IllegalArgumentException
    @Test
    void testTransferNullTarget_TC013() {
        BankAccount source = new BankAccount("SRC002", 200.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> source.transfer(null, 50.0));
        assertEquals("Target account cannot be null", ex.getMessage());
    }

    // TC-014: Transfer to inactive target throws IllegalStateException
    @Test
    void testTransferToInactiveTarget_TC014() {
        BankAccount source = new BankAccount("SRC003", 300.0);
        BankAccount target = new BankAccount("TGT002", 0.0); // zero balance to allow deactivation
        target.deactivate();
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> source.transfer(target, 30.0));
        assertEquals("Target account is inactive", ex.getMessage());
    }

    // TC-015: Operation on inactive account throws IllegalStateException via checkActive
    @Test
    void testOperationOnInactiveAccount_TC015() {
        BankAccount account = new BankAccount("ACC_INACTIVE", 0.0);
        account.deactivate();
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> account.deposit(100.0));
        assertEquals("Account is inactive", ex.getMessage());
    }

    // TC-016: deactivate() throws IllegalStateException when balance > 0
    @Test
    void testDeactivateWithNonZeroBalance_TC016() {
        BankAccount account = new BankAccount("ACC_DEACT", 10.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                account::deactivate);
        assertEquals("Cannot deactivate account with non-zero balance", ex.getMessage());
    }

    // TC-017: deactivate() succeeds when balance is zero and subsequent operations fail
    @Test
    void testDeactivateAndSubsequentInactiveOperation_TC017() {
        BankAccount account = new BankAccount("ACC_ZERO", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> account.withdraw(10.0));
        assertEquals("Account is inactive", ex.getMessage());
    }
}
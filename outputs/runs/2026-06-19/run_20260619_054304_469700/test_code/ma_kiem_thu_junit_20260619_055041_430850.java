import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.*;

class GeneratedTest {

    // TC-001: Create BankAccount with valid account number and positive initial balance
    @Test
    void testCreateAccountValid_TC_001() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        assertEquals("ACC123", account.getAccountNumber());
        assertEquals(100.0, account.getBalance(), 0.001);
        assertTrue(account.isActive());
    }

    // TC-002: Create BankAccount with null account number
    @Test
    void testCreateAccountNullNumber_TC_002() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 50.0));
    }

    // TC-003: Create BankAccount with empty account number string
    @Test
    void testCreateAccountEmptyNumber_TC_003() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 50.0));
    }

    // TC-004: Create BankAccount with negative initial balance
    @Test
    void testCreateAccountNegativeBalance_TC_004() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC124", -10.0));
    }

    // TC-005: Deposit a positive amount
    @Test
    void testDepositPositiveAmount_TC_005() {
        BankAccount account = new BankAccount("ACC125", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001);
    }

    // TC-006: Deposit zero amount
    @Test
    void testDepositZeroAmount_TC_006() {
        BankAccount account = new BankAccount("ACC126", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
    }

    // TC-007: Deposit negative amount
    @Test
    void testDepositNegativeAmount_TC_007() {
        BankAccount account = new BankAccount("ACC127", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-20.0));
    }

    // TC-008: Withdraw a valid amount less than balance
    @Test
    void testWithdrawValidAmount_TC_008() {
        BankAccount account = new BankAccount("ACC128", 200.0);
        account.withdraw(80.0);
        assertEquals(120.0, account.getBalance(), 0.001);
    }

    // TC-009: Withdraw amount greater than balance
    @Test
    void testWithdrawInsufficientFunds_TC_009() {
        BankAccount account = new BankAccount("ACC129", 50.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(75.0));
    }

    // TC-010: Withdraw zero amount
    @Test
    void testWithdrawZeroAmount_TC_010() {
        BankAccount account = new BankAccount("ACC130", 50.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(0.0));
    }

    // TC-011: Withdraw negative amount
    @Test
    void testWithdrawNegativeAmount_TC_011() {
        BankAccount account = new BankAccount("ACC131", 50.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-10.0));
    }

    // TC-012: Transfer amount to an active target account
    @Test
    void testTransferToActiveAccount_TC_012() {
        BankAccount source = new BankAccount("SRC001", 200.0);
        BankAccount target = new BankAccount("TGT001", 100.0);
        source.transfer(target, 50.0);
        assertEquals(150.0, source.getBalance(), 0.001);
        assertEquals(150.0, target.getBalance(), 0.001);
    }

    // TC-013: Transfer to null target account
    @Test
    void testTransferToNullTarget_TC_013() {
        BankAccount source = new BankAccount("SRC002", 200.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 30.0));
    }

    // TC-014: Transfer to inactive target account
    @Test
    void testTransferToInactiveTarget_TC_014() {
        BankAccount source = new BankAccount("SRC003", 200.0);
        BankAccount target = new BankAccount("TGT002", 100.0);
        // deactivate target (balance must be zero to allow deactivation)
        target.withdraw(100.0);
        target.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 30.0));
    }

    // TC-015: Transfer amount greater than source balance
    @Test
    void testTransferAmountExceedsSourceBalance_TC_015() {
        BankAccount source = new BankAccount("SRC004", 40.0);
        BankAccount target = new BankAccount("TGT003", 10.0);
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
    }

    // TC-016: Deactivate account with zero balance
    @Test
    void testDeactivateZeroBalance_TC_016() {
        BankAccount account = new BankAccount("ACC132", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    // TC-017: checkActive does not throw when account is active
    @Test
    void testCheckActiveDoesNotThrowWhenActive_TC_017() throws Exception {
        BankAccount account = new BankAccount("ACC133", 10.0);
        Method checkActive = BankAccount.class.getDeclaredMethod("checkActive");
        checkActive.setAccessible(true);
        Executable exec = () -> checkActive.invoke(account);
        assertDoesNotThrow(exec);
    }

    // TC-018: checkActive throws IllegalStateException with correct message when inactive
    @Test
    void testCheckActiveThrowsWithMessageWhenInactive_TC_018() throws Exception {
        BankAccount account = new BankAccount("ACC134", 0.0);
        // deactivate the account
        account.deactivate();
        Method checkActive = BankAccount.class.getDeclaredMethod("checkActive");
        checkActive.setAccessible(true);
        InvocationTargetException ex = assertThrows(InvocationTargetException.class,
                () -> checkActive.invoke(account));
        Throwable cause = ex.getCause();
        assertTrue(cause instanceof IllegalStateException);
        assertEquals("Account is inactive", cause.getMessage());
    }
}
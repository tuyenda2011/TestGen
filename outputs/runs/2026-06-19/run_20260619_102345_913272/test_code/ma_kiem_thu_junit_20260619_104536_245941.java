// Plan: TC-001, TC-002, TC-003, TC-004, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    // TC-001: Xác minh getAccountNumber() trả về số tài khoản đã khởi tạo
    @Test
    @DisplayName("TC-001: Verify getAccountNumber() returns the initialized account number")
    void test_getAccountNumber_returns_initialized_value() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals("ACC123", account.getAccountNumber());
    }

    // TC-002: Xác minh getBalance() trả về số dư đã khởi tạo
    @Test
    @DisplayName("TC-002: Verify getBalance() returns the initialized balance")
    void test_getBalance_returns_initialized_value() {
        BankAccount account = new BankAccount("ACC456", 2500.75);
        assertEquals(2500.75, account.getBalance(), 0.001);
    }

    // TC-003: Xác minh isActive() trả về true cho tài khoản mới được tạo
    @Test
    @DisplayName("TC-003: Verify isActive() returns true for newly created active account")
    void test_isActive_returns_true_for_new_account() {
        BankAccount account = new BankAccount("ACC789", 500.0);
        assertTrue(account.isActive());
    }

    // TC-004: checkActive() ném IllegalStateException khi tài khoản không active
    @Test
    @DisplayName("TC-004: checkActive() throws IllegalStateException when account is inactive")
    void test_checkActive_throws_when_inactive() {
        BankAccount account = new BankAccount("ACC001", 0.0);
        account.deactivate();
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> account.deposit(100.0));
        assertEquals("Account is inactive", ex.getMessage());
    }

    // TC-012: checkActive() ném IllegalStateException khi isActive là false qua withdraw
    @Test
    @DisplayName("TC-012: checkActive() throws IllegalStateException when isActive flag is false via withdraw")
    void test_checkActive_throws_when_isActive_false_via_withdraw() {
        BankAccount account = new BankAccount("ACC002", 0.0);
        account.deactivate();
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> account.withdraw(50.0));
        assertEquals("Account is inactive", ex.getMessage());
    }

    // TC-013: Constructor ném IllegalArgumentException cho account number rỗng
    @Test
    @DisplayName("TC-013: Constructor throws IllegalArgumentException for empty account number")
    void test_constructor_throws_for_empty_account_number() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 100.0));
        assertEquals("Account number cannot be empty", ex.getMessage());
    }

    // TC-014: Constructor ném IllegalArgumentException cho số dư âm
    @Test
    @DisplayName("TC-014: Constructor throws IllegalArgumentException for negative initial balance")
    void test_constructor_throws_for_negative_balance() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC003", -10.0));
        assertEquals("Initial balance cannot be negative", ex.getMessage());
    }

    // TC-015: deposit() cập nhật số dư thành công
    @Test
    @DisplayName("TC-015: deposit() successfully updates balance")
    void test_deposit_updates_balance() {
        BankAccount account = new BankAccount("ACC004", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001);
    }

    // TC-016: deposit() ném IllegalArgumentException cho số tiền bằng 0
    @Test
    @DisplayName("TC-016: deposit() throws IllegalArgumentException for zero amount")
    void test_deposit_throws_for_zero_amount() {
        BankAccount account = new BankAccount("ACC005", 100.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
        assertEquals("Deposit amount must be positive", ex.getMessage());
    }

    // TC-017: deposit() ném IllegalArgumentException cho số tiền âm
    @Test
    @DisplayName("TC-017: deposit() throws IllegalArgumentException for negative amount")
    void test_deposit_throws_for_negative_amount() {
        BankAccount account = new BankAccount("ACC006", 100.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> account.deposit(-50.0));
        assertEquals("Deposit amount must be positive", ex.getMessage());
    }

    // TC-018: withdraw() cập nhật số dư thành công
    @Test
    @DisplayName("TC-018: withdraw() successfully updates balance")
    void test_withdraw_updates_balance() {
        BankAccount account = new BankAccount("ACC007", 200.0);
        account.withdraw(75.0);
        assertEquals(125.0, account.getBalance(), 0.001);
    }

    // TC-019: withdraw() ném IllegalStateException cho số dư không đủ
    @Test
    @DisplayName("TC-019: withdraw() throws IllegalStateException for insufficient funds")
    void test_withdraw_throws_for_insufficient_funds() {
        BankAccount account = new BankAccount("ACC008", 50.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> account.withdraw(100.0));
        assertEquals("Insufficient funds", ex.getMessage());
    }

    // TC-020: transfer() ném IllegalStateException khi tài khoản nguồn không active
    @Test
    @DisplayName("TC-020: transfer() throws IllegalStateException when source account is inactive")
    void test_transfer_throws_when_source_inactive() {
        BankAccount source = new BankAccount("SRC", 0.0);
        source.deactivate();
        BankAccount target = new BankAccount("TGT", 0.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
        assertEquals("Account is inactive", ex.getMessage());
    }


    // ===== Targeted retry tests =====

// TC-021: Constructor ném IllegalArgumentException cho account number null
    @Test
    @DisplayName("TC-021: Constructor throws IllegalArgumentException for null account number")
    void test_constructor_throws_for_null_account_number() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 100.0));
        assertEquals("Account number cannot be empty", ex.getMessage());
    }

    // TC-022: transfer() ném IllegalArgumentException khi target account là null
    @Test
    @DisplayName("TC-022: transfer() throws IllegalArgumentException when target account is null")
    void test_transfer_throws_for_null_target() {
        BankAccount source = new BankAccount("SRC", 100.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 50.0));
        assertEquals("Target account cannot be null", ex.getMessage());
    }

    // TC-023: transfer() ném IllegalStateException khi target account không active
    @Test
    @DisplayName("TC-023: transfer() throws IllegalStateException when target account is inactive")
    void test_transfer_throws_when_target_inactive() {
        BankAccount source = new BankAccount("SRC", 100.0);
        BankAccount target = new BankAccount("TGT", 0.0);
        target.deactivate();
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
        assertEquals("Target account is inactive", ex.getMessage());
    }

    // TC-024: transfer() chuyển tiền thành công giữa hai tài khoản
    @Test
    @DisplayName("TC-024: transfer() successfully transfers money between accounts")
    void test_transfer_successful() {
        BankAccount source = new BankAccount("SRC", 200.0);
        BankAccount target = new BankAccount("TGT", 100.0);
        source.transfer(target, 75.0);
        assertEquals(125.0, source.getBalance(), 0.001);
        assertEquals(175.0, target.getBalance(), 0.001);
    }

    // TC-025: deactivate() ném IllegalStateException khi số dư > 0
    @Test
    @DisplayName("TC-025: deactivate() throws IllegalStateException when balance is positive")
    void test_deactivate_throws_for_positive_balance() {
        BankAccount account = new BankAccount("ACC", 100.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> account.deactivate());
        assertEquals("Cannot deactivate account with non-zero balance", ex.getMessage());
    }

    // TC-026: deactivate() đặt isActive thành false khi số dư bằng 0
    @Test
    @DisplayName("TC-026: deactivate() sets isActive to false when balance is zero")
    void test_deactivate_successful() {
        BankAccount account = new BankAccount("ACC", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    // TC-027: withdraw() ném IllegalArgumentException cho số tiền bằng 0
    @Test
    @DisplayName("TC-027: withdraw() throws IllegalArgumentException for zero amount")
    void test_withdraw_throws_for_zero_amount() {
        BankAccount account = new BankAccount("ACC", 100.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> account.withdraw(0.0));
        assertEquals("Withdraw amount must be positive", ex.getMessage());
    }

    // TC-028: withdraw() ném IllegalArgumentException cho số tiền âm
    @Test
    @DisplayName("TC-028: withdraw() throws IllegalArgumentException for negative amount")
    void test_withdraw_throws_for_negative_amount() {
        BankAccount account = new BankAccount("ACC", 100.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> account.withdraw(-50.0));
        assertEquals("Withdraw amount must be positive", ex.getMessage());
    }

    // TC-029: transfer() ném IllegalArgumentException khi amount bằng 0
    @Test
    @DisplayName("TC-029: transfer() throws IllegalArgumentException for zero transfer amount")
    void test_transfer_throws_for_zero_amount() {
        BankAccount source = new BankAccount("SRC", 100.0);
        BankAccount target = new BankAccount("TGT", 50.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> source.transfer(target, 0.0));
        assertEquals("Withdraw amount must be positive", ex.getMessage());
    }

    // TC-030: transfer() ném IllegalArgumentException khi amount âm
    @Test
    @DisplayName("TC-030: transfer() throws IllegalArgumentException for negative transfer amount")
    void test_transfer_throws_for_negative_amount() {
        BankAccount source = new BankAccount("SRC", 100.0);
        BankAccount target = new BankAccount("TGT", 50.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> source.transfer(target, -25.0));
        assertEquals("Withdraw amount must be positive", ex.getMessage());
    }

    // TC-031: transfer() ném IllegalStateException khi source không đủ tiền
    @Test
    @DisplayName("TC-031: transfer() throws IllegalStateException when source has insufficient funds")
    void test_transfer_throws_for_insufficient_funds() {
        BankAccount source = new BankAccount("SRC", 50.0);
        BankAccount target = new BankAccount("TGT", 100.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> source.transfer(target, 100.0));
        assertEquals("Insufficient funds", ex.getMessage());
    }
}
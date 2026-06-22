// Plan: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    // TC-001: Kiểm tra tạo BankAccount hợp lệ và các getter trả về giá trị đúng
    @Test
    void test_TC_001_createValidAccount() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        assertEquals("ACC123", account.getAccountNumber(), "Số tài khoản phải khớp");
        assertEquals(100.0, account.getBalance(), 0.0001, "Số dư phải khớp");
        assertTrue(account.isActive(), "Tài khoản phải ở trạng thái active");
    }

    // TC-002: Kiểm tra constructor ném IllegalArgumentException khi accountNumber null
    @Test
    void test_TC_002_constructorNullAccountNumber() {
        assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount(null, 50.0);
        }, "Phải ném IllegalArgumentException khi accountNumber null");
    }

    // TC-003: Kiểm tra constructor ném IllegalArgumentException khi initialBalance âm
    @Test
    void test_TC_003_constructorNegativeBalance() {
        assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("ACC124", -10.0);
        }, "Phải ném IllegalArgumentException khi số dư ban đầu âm");
    }

    // TC-004: Kiểm tra deposit tăng balance đúng
    @Test
    void test_TC_004_depositPositiveAmount() {
        BankAccount account = new BankAccount("ACC125", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.0001, "Balance phải tăng sau deposit");
    }

    // TC-005: Kiểm tra deposit ném IllegalArgumentException khi amount không dương
    @Test
    void test_TC_005_depositNonPositiveAmount() {
        BankAccount account = new BankAccount("ACC126", 100.0);
        assertThrows(IllegalArgumentException.class, () -> {
            account.deposit(0.0);
        }, "Phải ném IllegalArgumentException khi deposit amount không dương");
    }

    // TC-006: Kiểm tra withdraw thành công khi amount < balance
    @Test
    void test_TC_006_withdrawValidAmount() {
        BankAccount account = new BankAccount("ACC127", 200.0);
        account.withdraw(80.0);
        assertEquals(120.0, account.getBalance(), 0.0001, "Balance phải giảm sau withdraw");
    }

    // TC-007: Kiểm tra withdraw ném IllegalArgumentException khi amount không dương
    @Test
    void test_TC_007_withdrawNonPositiveAmount() {
        BankAccount account = new BankAccount("ACC128", 200.0);
        assertThrows(IllegalArgumentException.class, () -> {
            account.withdraw(-5.0);
        }, "Phải ném IllegalArgumentException khi withdraw amount không dương");
    }

    // TC-008: Kiểm tra withdraw ném IllegalStateException khi amount vượt quá balance
    @Test
    void test_TC_008_withdrawExceedsBalance() {
        BankAccount account = new BankAccount("ACC129", 30.0);
        assertThrows(IllegalStateException.class, () -> {
            account.withdraw(50.0);
        }, "Phải ném IllegalStateException khi số tiền rút vượt quá số dư");
    }

    // TC-009: Kiểm tra transfer thành công khi target active và đủ tiền
    @Test
    void test_TC_009_transferSuccess() {
        BankAccount source = new BankAccount("SRC001", 150.0);
        BankAccount target = new BankAccount("TGT001", 20.0);
        source.transfer(target, 50.0);
        assertEquals(100.0, source.getBalance(), 0.0001, "Số dư source giảm sau transfer");
        assertEquals(70.0, target.getBalance(), 0.0001, "Số dư target tăng sau transfer");
    }

    // TC-010: Kiểm tra transfer ném IllegalArgumentException khi target null
    @Test
    void test_TC_010_transferNullTarget() {
        BankAccount source = new BankAccount("SRC002", 100.0);
        assertThrows(IllegalArgumentException.class, () -> {
            source.transfer(null, 20.0);
        }, "Phải ném IllegalArgumentException khi targetAccount null");
    }

    // TC-011: Kiểm tra transfer ném IllegalStateException khi target inactive
    @Test
    void test_TC_011_transferToInactiveTarget() {
        BankAccount source = new BankAccount("SRC003", 100.0);
        BankAccount target = new BankAccount("TGT002", 0.0);
        // Deactivate target để tạo trạng thái inactive
        target.deactivate();
        assertThrows(IllegalStateException.class, () -> {
            source.transfer(target, 10.0);
        }, "Phải ném IllegalStateException khi target account inactive");
    }

    // TC-012: Kiểm tra deactivate ném IllegalStateException khi balance > 0
    @Test
    void test_TC_012_deactivateWithNonZeroBalance() {
        BankAccount account = new BankAccount("ACC130", 10.0);
        assertThrows(IllegalStateException.class, () -> {
            account.deactivate();
        }, "Phải ném IllegalStateException khi deactivate với balance khác 0");
    }

    // TC-013: Kiểm tra deactivate thành công khi balance = 0
    @Test
    void test_TC_013_deactivateSuccess() {
        BankAccount account = new BankAccount("ACC131", 0.0);
        account.deactivate();
        assertFalse(account.isActive(), "Tài khoản phải ở trạng thái inactive sau deactivate");
    }
}
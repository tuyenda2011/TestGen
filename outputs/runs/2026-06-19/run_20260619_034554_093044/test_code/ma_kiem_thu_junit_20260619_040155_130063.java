import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GeneratedTest {

    // TC-001: Kiểm tra tạo tài khoản hợp lệ và các getter trả về giá trị đúng
    @Test
    void testCreateAccountValid_TC_001() {
        BankAccount account = new BankAccount("ACC12345", 1000.0);
        assertEquals("ACC12345", account.getAccountNumber());
        assertEquals(1000.0, account.getBalance(), 0.001);
        assertTrue(account.isActive());
    }

    // TC-002: Kiểm tra tạo tài khoản với accountNumber null ném IllegalArgumentException
    @Test
    void testCreateAccountNullNumber_TC_002() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 500.0));
    }

    // TC-003: Kiểm tra tạo tài khoản với accountNumber rỗng ném IllegalArgumentException
    @Test
    void testCreateAccountEmptyNumber_TC_003() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 500.0));
    }

    // TC-004: Kiểm tra tạo tài khoản với số dư âm ném IllegalArgumentException
    @Test
    void testCreateAccountNegativeBalance_TC_004() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC98765", -10.0));
    }

    // TC-005: Nạp tiền vào tài khoản đang hoạt động, số dư tăng đúng
    @Test
    void testDepositPositiveAmount_TC_005() {
        BankAccount account = new BankAccount("ACC001", 200.0);
        account.deposit(150.0);
        assertEquals(350.0, account.getBalance(), 0.001);
    }

    // TC-006: Nạp tiền số 0 ném IllegalArgumentException
    @Test
    void testDepositZeroAmount_TC_006() {
        BankAccount account = new BankAccount("ACC002", 200.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
    }

    // TC-007: Nạp tiền số âm ném IllegalArgumentException
    @Test
    void testDepositNegativeAmount_TC_007() {
        BankAccount account = new BankAccount("ACC003", 200.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-50.0));
    }

    // TC-008: Rút tiền hợp lệ, số dư giảm đúng
    @Test
    void testWithdrawValidAmount_TC_008() {
        BankAccount account = new BankAccount("ACC004", 500.0);
        account.withdraw(200.0);
        assertEquals(300.0, account.getBalance(), 0.001);
    }

    // TC-009: Rút tiền số 0 ném IllegalArgumentException
    @Test
    void testWithdrawZeroAmount_TC_009() {
        BankAccount account = new BankAccount("ACC005", 500.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(0.0));
    }

    // TC-010: Rút tiền số âm ném IllegalArgumentException
    @Test
    void testWithdrawNegativeAmount_TC_010() {
        BankAccount account = new BankAccount("ACC006", 500.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-100.0));
    }

    // TC-011: Rút tiền vượt quá số dư ném IllegalStateException
    @Test
    void testWithdrawInsufficientFunds_TC_011() {
        BankAccount account = new BankAccount("ACC007", 300.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(400.0));
    }

    // TC-012: Chuyển tiền hợp lệ giữa hai tài khoản hoạt động
    @Test
    void testTransferValid_TC_012() {
        BankAccount source = new BankAccount("SRC001", 800.0);
        BankAccount target = new BankAccount("TGT001", 200.0);
        source.transfer(target, 300.0);
        assertEquals(500.0, source.getBalance(), 0.001);
        assertEquals(500.0, target.getBalance(), 0.001);
    }

    // TC-013: Chuyển tiền sang tài khoản null ném IllegalArgumentException
    @Test
    void testTransferToNullTarget_TC_013() {
        BankAccount source = new BankAccount("SRC002", 800.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 100.0));
    }

    // TC-014: Chuyển tiền sang tài khoản không hoạt động ném IllegalStateException
    @Test
    void testTransferToInactiveTarget_TC_014() {
        BankAccount source = new BankAccount("SRC003", 800.0);
        BankAccount target = new BankAccount("TGT002", 200.0);
        // Deactivate target by withdrawing all funds then calling deactivate
        target.withdraw(200.0);
        target.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 100.0));
    }

    // TC-015: Gọi deposit trên tài khoản không hoạt động ném IllegalStateException
    @Test
    void testDepositOnInactiveAccount_TC_015() {
        BankAccount account = new BankAccount("ACC008", 100.0);
        account.withdraw(100.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.deposit(50.0));
    }

    // TC-016: Gọi withdraw trên tài khoản không hoạt động ném IllegalStateException
    @Test
    void testWithdrawOnInactiveAccount_TC_016() {
        BankAccount account = new BankAccount("ACC009", 100.0);
        account.withdraw(100.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.withdraw(10.0));
    }

    // TC-017: Gọi transfer từ tài khoản không hoạt động ném IllegalStateException
    @Test
    void testTransferFromInactiveAccount_TC_017() {
        BankAccount source = new BankAccount("SRC004", 500.0);
        BankAccount target = new BankAccount("TGT003", 100.0);
        source.withdraw(500.0);
        source.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
    }
}
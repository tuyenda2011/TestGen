import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GeneratedTest {

    // TC-001: Kiểm tra tạo tài khoản hợp lệ và các getter trả về giá trị đúng
    @Test
    void testCreateAccountValid_TC_001() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals("ACC123", account.getAccountNumber(), "Số tài khoản không khớp");
        assertEquals(1000.0, account.getBalance(), 0.001, "Số dư không khớp");
        assertTrue(account.isActive(), "Tài khoản phải ở trạng thái hoạt động");
    }

    // TC-002: Kiểm tra constructor ném IllegalArgumentException khi accountNumber null
    @Test
    void testConstructorNullAccountNumber_TC_002() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount(null, 500.0));
        assertEquals("Account number cannot be empty", ex.getMessage());
    }

    // TC-003: Kiểm tra constructor ném IllegalArgumentException khi accountNumber rỗng
    @Test
    void testConstructorEmptyAccountNumber_TC_003() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount("   ", 500.0));
        assertEquals("Account number cannot be empty", ex.getMessage());
    }

    // TC-004: Kiểm tra constructor ném IllegalArgumentException khi initialBalance âm
    @Test
    void testConstructorNegativeBalance_TC_004() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount("ACC124", -10.0));
        assertEquals("Initial balance cannot be negative", ex.getMessage());
    }

    // TC-005: Kiểm tra deposit số tiền dương cập nhật balance đúng
    @Test
    void testDepositPositiveAmount_TC_005() {
        BankAccount account = new BankAccount("ACC200", 200.0);
        account.deposit(150.0);
        assertEquals(350.0, account.getBalance(), 0.001);
    }

    // TC-006: Kiểm tra deposit số 0 ném IllegalArgumentException
    @Test
    void testDepositZeroAmount_TC_006() {
        BankAccount account = new BankAccount("ACC201", 200.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> account.deposit(0.0));
        assertEquals("Deposit amount must be positive", ex.getMessage());
    }

    // TC-007: Kiểm tra deposit số âm ném IllegalArgumentException
    @Test
    void testDepositNegativeAmount_TC_007() {
        BankAccount account = new BankAccount("ACC202", 200.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> account.deposit(-50.0));
        assertEquals("Deposit amount must be positive", ex.getMessage());
    }

    // TC-008: Kiểm tra withdraw số tiền nhỏ hơn balance thành công
    @Test
    void testWithdrawWithinBalance_TC_008() {
        BankAccount account = new BankAccount("ACC300", 500.0);
        account.withdraw(200.0);
        assertEquals(300.0, account.getBalance(), 0.001);
    }

    // TC-009: Kiểm tra withdraw số tiền lớn hơn balance ném IllegalStateException
    @Test
    void testWithdrawExceedBalance_TC_009() {
        BankAccount account = new BankAccount("ACC301", 300.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> account.withdraw(400.0));
        assertEquals("Insufficient funds", ex.getMessage());
    }

    // TC-010: Kiểm tra withdraw số 0 hoặc âm ném IllegalArgumentException
    @Test
    void testWithdrawZeroOrNegativeAmount_TC_010() {
        BankAccount account = new BankAccount("ACC302", 300.0);
        IllegalArgumentException ex1 = assertThrows(IllegalArgumentException.class,
                () -> account.withdraw(0.0));
        assertEquals("Withdraw amount must be positive", ex1.getMessage());

        IllegalArgumentException ex2 = assertThrows(IllegalArgumentException.class,
                () -> account.withdraw(-10.0));
        assertEquals("Withdraw amount must be positive", ex2.getMessage());
    }

    // TC-011: Kiểm tra transfer thành công khi target account hoạt động và đủ tiền
    @Test
    void testTransferSuccessful_TC_011() {
        BankAccount source = new BankAccount("SRC001", 500.0);
        BankAccount target = new BankAccount("TGT001", 200.0);
        source.transfer(target, 150.0);
        assertEquals(350.0, source.getBalance(), 0.001);
        assertEquals(350.0, target.getBalance(), 0.001);
    }

    // TC-012: Kiểm tra transfer ném IllegalArgumentException khi targetAccount null
    @Test
    void testTransferNullTarget_TC_012() {
        BankAccount source = new BankAccount("SRC002", 500.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> source.transfer(null, 100.0));
        assertEquals("Target account cannot be null", ex.getMessage());
    }

    // TC-013: Kiểm tra transfer ném IllegalStateException khi targetAccount không hoạt động
    @Test
    void testTransferToInactiveTarget_TC_013() {
        BankAccount source = new BankAccount("SRC003", 500.0);
        BankAccount inactiveTarget = new BankAccount("TGT002", 0.0);
        inactiveTarget.deactivate(); // làm cho tài khoản mục tiêu không hoạt động
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> source.transfer(inactiveTarget, 100.0));
        assertEquals("Target account is inactive", ex.getMessage());
    }

    // TC-014: Kiểm tra deactivate ném IllegalStateException khi balance không bằng 0
    @Test
    void testDeactivateWithNonZeroBalance_TC_014() {
        BankAccount account = new BankAccount("ACC400", 50.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                account::deactivate);
        assertEquals("Cannot deactivate account with non-zero balance", ex.getMessage());
    }

    // TC-015: Kiểm tra deactivate thành công khi balance = 0
    @Test
    void testDeactivateWhenZeroBalance_TC_015() {
        BankAccount account = new BankAccount("ACC401", 0.0);
        account.deactivate();
        assertFalse(account.isActive(), "Tài khoản phải ở trạng thái không hoạt động sau khi deactivate");
    }

    // TC-016: Kiểm tra rằng mọi thao tác (deposit, withdraw, transfer) trên tài khoản không hoạt động ném IllegalStateException với thông điệp đúng
    @Test
    void testOperationsOnInactiveAccountThrow_TC_016() {
        BankAccount inactive = new BankAccount("ACC500", 0.0);
        inactive.deactivate();

        IllegalStateException exDeposit = assertThrows(IllegalStateException.class,
                () -> inactive.deposit(10.0));
        assertEquals("Account is inactive", exDeposit.getMessage());

        IllegalStateException exWithdraw = assertThrows(IllegalStateException.class,
                () -> inactive.withdraw(10.0));
        assertEquals("Account is inactive", exWithdraw.getMessage());

        BankAccount target = new BankAccount("ACC501", 0.0);
        IllegalStateException exTransfer = assertThrows(IllegalStateException.class,
                () -> inactive.transfer(target, 5.0));
        assertEquals("Account is inactive", exTransfer.getMessage());
    }
}
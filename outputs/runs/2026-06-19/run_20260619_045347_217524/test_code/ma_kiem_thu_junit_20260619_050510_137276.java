import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    /**
     * TC-006: Kiểm tra rằng phương thức checkActive (được gọi nội bộ) ném IllegalStateException
     * khi tài khoản không hoạt động. Ta tạo tài khoản, deactivate nó (với số dư 0) rồi gọi withdraw
     * để kích hoạt kiểm tra trạng thái.
     */
    @Test
    void testCheckActiveThrowsWhenInactive_TC_006() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        // Deactivate khi balance = 0
        account.deactivate();
        // withdraw sẽ gọi checkActive trước khi kiểm tra số tiền
        assertThrows(IllegalStateException.class, () -> account.withdraw(10.0));
    }

    /**
     * TC-007: Xác nhận các getter trả về giá trị đúng cho một tài khoản hợp lệ.
     */
    @Test
    void testGettersReturnCorrectValues_TC_007() {
        String expectedNumber = "12345";
        double expectedBalance = 2500.75;
        boolean expectedActive = true;

        BankAccount account = new BankAccount(expectedNumber, expectedBalance);

        assertEquals(expectedNumber, account.getAccountNumber(), "Số tài khoản không khớp");
        assertEquals(expectedBalance, account.getBalance(), 0.0001, "Số dư không khớp");
        assertTrue(account.isActive(), "Trạng thái hoạt động không đúng");
    }

    // ===== Targeted retry tests =====

    /**
     * Kiểm tra constructor ném IllegalArgumentException khi số tài khoản null.
     */
    @Test
    void COV_retry_2_constructor_nullAccountNumber() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 100.0));
    }

    /**
     * Kiểm tra constructor ném IllegalArgumentException khi số tài khoản rỗng.
     */
    @Test
    void COV_retry_2_constructor_emptyAccountNumber() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 100.0));
    }

    /**
     * Kiểm tra constructor ném IllegalArgumentException khi số dư ban đầu âm.
     */
    @Test
    void COV_retry_2_constructor_negativeInitialBalance() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC001", -50.0));
    }

    /**
     * Kiểm tra deposit thành công với số tiền dương.
     */
    @Test
    void COV_retry_2_deposit_positiveAmount() {
        BankAccount account = new BankAccount("ACC002", 200.0);
        account.deposit(150.0);
        assertEquals(350.0, account.getBalance(), 0.0001);
    }

    /**
     * Kiểm tra deposit ném IllegalArgumentException khi số tiền không dương.
     */
    @Test
    void COV_retry_2_deposit_nonPositiveAmount() {
        BankAccount account = new BankAccount("ACC003", 200.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-10.0));
    }

    /**
     * Kiểm tra withdraw thành công khi số dư đủ và số tiền dương.
     */
    @Test
    void COV_retry_2_withdraw_success() {
        BankAccount account = new BankAccount("ACC004", 500.0);
        account.withdraw(200.0);
        assertEquals(300.0, account.getBalance(), 0.0001);
    }

    /**
     * Kiểm tra withdraw ném IllegalArgumentException khi số tiền không dương.
     */
    @Test
    void COV_retry_2_withdraw_nonPositiveAmount() {
        BankAccount account = new BankAccount("ACC005", 500.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(0.0));
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-20.0));
    }

    /**
     * Kiểm tra withdraw ném IllegalStateException khi số dư không đủ.
     */
    @Test
    void COV_retry_2_withdraw_insufficientFunds() {
        BankAccount account = new BankAccount("ACC006", 100.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(150.0));
    }

    /**
     * Kiểm tra transfer thành công giữa hai tài khoản hoạt động.
     */
    @Test
    void COV_retry_2_transfer_success() {
        BankAccount source = new BankAccount("SRC001", 400.0);
        BankAccount target = new BankAccount("TGT001", 100.0);
        source.transfer(target, 150.0);
        assertEquals(250.0, source.getBalance(), 0.0001);
        assertEquals(250.0, target.getBalance(), 0.0001);
    }

    /**
     * Kiểm tra transfer ném IllegalArgumentException khi target null.
     */
    @Test
    void COV_retry_2_transfer_nullTarget() {
        BankAccount source = new BankAccount("SRC002", 300.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 50.0));
    }

    /**
     * Kiểm tra transfer ném IllegalStateException khi target không hoạt động.
     */
    @Test
    void COV_retry_2_transfer_inactiveTarget() {
        BankAccount source = new BankAccount("SRC003", 300.0);
        BankAccount target = new BankAccount("TGT002", 0.0);
        // Deactivate target (balance = 0)
        target.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
    }

    /**
     * Kiểm tra deactivate thành công khi số dư bằng 0.
     */
    @Test
    void COV_retry_2_deactivate_success() {
        BankAccount account = new BankAccount("ACC007", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    /**
     * Kiểm tra deactivate ném IllegalStateException khi số dư > 0.
     */
    @Test
    void COV_retry_2_deactivate_nonZeroBalance() {
        BankAccount account = new BankAccount("ACC008", 10.0);
        assertThrows(IllegalStateException.class, () -> account.deactivate());
    }

    /**
     * Kiểm tra checkActive được gọi gián tiếp qua deposit khi tài khoản không hoạt động.
     */
    @Test
    void COV_retry_2_deposit_inactiveAccount() {
        BankAccount account = new BankAccount("ACC009", 0.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.deposit(50.0));
    }

    /**
     * Kiểm tra checkActive được gọi gián tiếp qua transfer khi tài khoản nguồn không hoạt động.
     */
    @Test
    void COV_retry_2_transfer_inactiveSource() {
        BankAccount source = new BankAccount("SRC004", 0.0);
        BankAccount target = new BankAccount("TGT003", 100.0);
        source.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
    }
}
// Plan: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.io.TempDir;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.api.function.Executable;
import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.Path;
import java.nio.file.Files;
import java.io.IOException;

public class BankAccountTest {

    // TC-001: Tạo tài khoản với số tài khoản hợp lệ và số dư ban đầu dương
    @Test
    void TC_001_createBankAccountWithValidAccountNumberAndPositiveInitialBalance() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        assertEquals("ACC123", account.getAccountNumber(), "Số tài khoản phải trả về ACC123");
        assertEquals(100.0, account.getBalance(), 0.001, "Số dư ban đầu phải là 100.0");
        assertTrue(account.isActive(), "Tài khoản mới tạo phải active");
    }

    // TC-002: Constructor ném ngoại lệ khi số tài khoản là null
    @Test
    void TC_002_constructorThrowsWhenAccountNumberIsNull() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount(null, 50.0);
        }, "Phải ném IllegalArgumentException khi accountNumber null");
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-003: Constructor ném ngoại lệ khi số dư ban đầu âm
    @Test
    void TC_003_constructorThrowsWhenInitialBalanceIsNegative() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("ACC124", -10.0);
        }, "Phải ném IllegalArgumentException khi initialBalance âm");
        assertEquals("Initial balance cannot be negative", exception.getMessage());
    }

    // TC-004: Nạp tiền dương cập nhật số dư
    @Test
    void TC_004_depositPositiveAmountUpdatesBalance() {
        BankAccount account = new BankAccount("ACC125", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001, "Số dư sau deposit phải là 150.0");
    }

    // TC-005: Deposit ném ngoại lệ khi số tiền là 0 hoặc âm
    @Test
    void TC_005_depositThrowsWhenAmountIsZeroOrNegative() {
        BankAccount account = new BankAccount("ACC126", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            account.deposit(0.0);
        }, "Phải ném IllegalArgumentException khi deposit amount <= 0");
        assertEquals("Deposit amount must be positive", exception.getMessage());
    }

    // TC-006: Rút tiền nhỏ hơn số dư thành công
    @Test
    void TC_006_withdrawAmountLessThanBalanceSucceeds() {
        BankAccount account = new BankAccount("ACC127", 200.0);
        account.withdraw(80.0);
        assertEquals(120.0, account.getBalance(), 0.001, "Số dư sau withdraw phải là 120.0");
    }

    // TC-007: Withdraw ném ngoại lệ khi số tiền là 0 hoặc âm
    @Test
    void TC_007_withdrawThrowsWhenAmountIsZeroOrNegative() {
        BankAccount account = new BankAccount("ACC128", 200.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            account.withdraw(-5.0);
        }, "Phải ném IllegalArgumentException khi withdraw amount <= 0");
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    // TC-008: Withdraw ném ngoại lệ khi không đủ số dư
    @Test
    void TC_008_withdrawThrowsWhenInsufficientFunds() {
        BankAccount account = new BankAccount("ACC129", 50.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.withdraw(100.0);
        }, "Phải ném IllegalStateException khi không đủ số dư");
        assertEquals("Insufficient funds", exception.getMessage());
    }

    // TC-009: Chuyển tiền tới tài khoản đích active thành công
    @Test
    void TC_009_transferToActiveTargetAccountSucceeds() {
        BankAccount sourceAccount = new BankAccount("ACC130", 150.0);
        BankAccount targetAccount = new BankAccount("ACC131", 30.0);
        sourceAccount.transfer(targetAccount, 50.0);
        assertEquals(100.0, sourceAccount.getBalance(), 0.001, "Số dư nguồn sau transfer phải là 100.0");
        assertEquals(80.0, targetAccount.getBalance(), 0.001, "Số dư đích sau transfer phải là 80.0");
    }

    // TC-010: Transfer ném ngoại lệ khi tài khoản đích là null
    @Test
    void TC_010_transferThrowsWhenTargetAccountIsNull() {
        BankAccount sourceAccount = new BankAccount("ACC132", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            sourceAccount.transfer(null, 20.0);
        }, "Phải ném IllegalArgumentException khi target account null");
        assertEquals("Target account cannot be null", exception.getMessage());
    }

    // TC-011: Transfer ném ngoại lệ khi tài khoản đích không active
    @Test
    void TC_011_transferThrowsWhenTargetAccountIsInactive() {
        BankAccount sourceAccount = new BankAccount("ACC133", 100.0);
        BankAccount targetAccount = new BankAccount("ACC134", 0.0);
        targetAccount.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            sourceAccount.transfer(targetAccount, 10.0);
        }, "Phải ném IllegalStateException khi target account không active");
        assertEquals("Target account is inactive", exception.getMessage());
    }

    // TC-012: Deactivate tài khoản active có số dư 0 thành công
    @Test
    void TC_012_deactivateActiveAccountWithZeroBalanceSucceeds() {
        BankAccount account = new BankAccount("ACC135", 0.0);
        account.deactivate();
        assertFalse(account.isActive(), "Tài khoản phải không active sau deactivate");
    }

    // TC-013: Deactivate ném ngoại lệ khi số dư lớn hơn 0
    @Test
    void TC_013_deactivateThrowsWhenBalanceIsGreaterThanZero() {
        BankAccount account = new BankAccount("ACC136", 10.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.deactivate();
        }, "Phải ném IllegalStateException khi balance > 0");
        assertEquals("Cannot deactivate account with non-zero balance", exception.getMessage());
    }

    // TC-014: Các phương thức getter trả về đúng giá trị trường
    @Test
    void TC_014_getterMethodsReturnCorrectFieldValues() {
        BankAccount account = new BankAccount("ACC999", 250.0);
        assertEquals("ACC999", account.getAccountNumber(), "getAccountNumber() phải trả về ACC999");
        assertEquals(250.0, account.getBalance(), 0.001, "getBalance() phải trả về 250.0");
        assertTrue(account.isActive(), "isActive() phải trả về true");
    }

    // TC-015: Kiểm tra hành vi checkActive() thông qua phương thức public gọi nó (deposit)
    @Test
    void TC_015_checkActiveBehaviorVerifiedViaDepositOnInactiveAccount() {
        BankAccount account = new BankAccount("ACC137", 0.0);
        account.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.deposit(10.0);
        }, "Phải ném IllegalStateException khi account không active");
        assertEquals("Account is inactive", exception.getMessage());
    }

    // TC-016: Kiểm tra thao tác file tạm với @TempDir
    @Test
    void TC_016_writeAndReadTempFile(@TempDir Path tempDir) throws IOException {
        Path file = tempDir.resolve("data.txt");
        Files.writeString(file, "a,b,c");
        String content = Files.readString(file);
        assertEquals("a,b,c", content, "Nội dung file tạm phải là a,b,c");
    }

    // TC-017: Parameterized test cho getAccountNumber với các giá trị khác nhau
    @ParameterizedTest
    @ValueSource(strings = {"ACC001", "ACC002", "ACC003"})
    void TC_017_getAccountNumber_returnsProvidedValue(String acc) {
        BankAccount account = new BankAccount(acc, 0.0);
        assertEquals(acc, account.getAccountNumber(), "getAccountNumber() phải trả về giá trị đầu vào");
    }

    // TC-018: Parameterized test cho isActive với các trường hợp khác nhau
    @ParameterizedTest
    @ValueSource(doubles = {0.0, 100.0, 500.5})
    void TC_018_isActive_returnsTrueForNewAccounts(double balance) {
        BankAccount account = new BankAccount("ACC138", balance);
        assertTrue(account.isActive(), "Tài khoản mới tạo phải luôn active");
    }
}
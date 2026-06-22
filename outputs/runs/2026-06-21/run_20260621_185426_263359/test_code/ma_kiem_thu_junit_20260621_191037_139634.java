import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BankAccountTest {

    private BankAccount defaultAccount;

    @BeforeEach
    void setUp() {
        // Khởi tạo một tài khoản mặc định để các test không phụ thuộc vào trạng thái chung
        defaultAccount = new BankAccount("DEFAULT", 0.0);
    }

    // -------------------- Constructor Tests --------------------
    @Nested
    @DisplayName("Constructor Validation")
    class ConstructorTests {

        @Test
        @DisplayName("Constructor throws IllegalArgumentException khi accountNumber null, rỗng hoặc chỉ khoảng trắng")
        void testConstructorInvalidAccountNumber() {
            String[] invalids = {null, "", "   "};
            for (String invalidAccountNumber : invalids) {
                IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                        () -> new BankAccount(invalidAccountNumber, 0.0));
                assertTrue(ex.getMessage().contains("Account number cannot be empty"));
            }
        }

        @Test
        @DisplayName("Constructor throws IllegalArgumentException khi initialBalance âm")
        void testConstructorNegativeInitialBalance() {
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                    () -> new BankAccount("ACC001", -10.0));
            assertTrue(ex.getMessage().contains("Initial balance cannot be negative"));
        }

        @Test
        @DisplayName("Tạo tài khoản hợp lệ với số dư 0 và kiểm tra trạng thái active")
        void testConstructorValidZeroBalance() {
            BankAccount account = new BankAccount("ACC123", 0.0);
            assertEquals("ACC123", account.getAccountNumber());
            assertEquals(0.0, account.getBalance(), 0.001);
            assertTrue(account.isActive());
        }

        @Test
        @DisplayName("Tạo tài khoản hợp lệ với số dư dương và kiểm tra trạng thái active")
        void testConstructorValidPositiveBalance() {
            BankAccount account = new BankAccount("ACC456", 100.50);
            assertEquals("ACC456", account.getAccountNumber());
            assertEquals(100.50, account.getBalance(), 0.001);
            assertTrue(account.isActive());
        }
    }

    // -------------------- Getter Tests --------------------
    @Nested
    @DisplayName("Getter Methods")
    class GetterTests {

        @Test
        @DisplayName("Lấy accountNumber trả về giá trị đã truyền vào constructor")
        void testGetAccountNumber() {
            BankAccount account = new BankAccount("ACC001", 50.0);
            assertEquals("ACC001", account.getAccountNumber());
        }

        @Test
        @DisplayName("Kiểm tra isActive trả về true sau khi tạo tài khoản")
        void testIsActiveAfterConstruction() {
            BankAccount account = new BankAccount("ANY", 10.0);
            assertTrue(account.isActive());
        }
    }

    // -------------------- Deposit Tests --------------------
    @Nested
    @DisplayName("Deposit Operations")
    class DepositTests {

        @Test
        @DisplayName("Deposit amount zero ném IllegalArgumentException")
        void testDepositZeroThrows() {
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                    () -> defaultAccount.deposit(0.0));
            assertTrue(ex.getMessage().contains("Deposit amount must be positive"));
        }

        @Test
        @DisplayName("Deposit amount âm ném IllegalArgumentException")
        void testDepositNegativeThrows() {
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                    () -> defaultAccount.deposit(-5.0));
            assertTrue(ex.getMessage().contains("Deposit amount must be positive"));
        }

        @Test
        @DisplayName("Deposit thành công cập nhật số dư")
        void testDepositSuccessful() {
            BankAccount account = new BankAccount("ACC001", 20.0);
            account.deposit(30.0);
            assertEquals(50.0, account.getBalance(), 0.001);
        }

        @Test
        @DisplayName("Deposit trên tài khoản không active ném IllegalStateException")
        void testDepositOnInactiveAccountThrows() {
            BankAccount account = new BankAccount("ACC001", 0.0);
            account.deactivate();
            IllegalStateException ex = assertThrows(IllegalStateException.class,
                    () -> account.deposit(10.0));
            assertTrue(ex.getMessage().contains("Account is inactive"));
        }
    }

    // -------------------- Withdraw Tests --------------------
    @Nested
    @DisplayName("Withdraw Operations")
    class WithdrawTests {

        @Test
        @DisplayName("Withdraw amount zero ném IllegalArgumentException")
        void testWithdrawZeroThrows() {
            BankAccount account = new BankAccount("ACC001", 100.0);
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                    () -> account.withdraw(0.0));
            assertTrue(ex.getMessage().contains("Withdraw amount must be positive"));
        }

        @Test
        @DisplayName("Withdraw amount âm ném IllegalArgumentException")
        void testWithdrawNegativeThrows() {
            BankAccount account = new BankAccount("ACC001", 100.0);
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                    () -> account.withdraw(-20.0));
            assertTrue(ex.getMessage().contains("Withdraw amount must be positive"));
        }

        @Test
        @DisplayName("Withdraw vượt quá số dư ném IllegalStateException")
        void testWithdrawExceedsBalanceThrows() {
            BankAccount account = new BankAccount("ACC001", 50.0);
            IllegalStateException ex = assertThrows(IllegalStateException.class,
                    () -> account.withdraw(75.0));
            assertTrue(ex.getMessage().contains("Insufficient funds"));
        }

        @Test
        @DisplayName("Withdraw thành công giảm số dư")
        void testWithdrawSuccessful() {
            BankAccount account = new BankAccount("ACC001", 80.0);
            account.withdraw(30.0);
            assertEquals(50.0, account.getBalance(), 0.001);
        }

        @Test
        @DisplayName("Withdraw trên tài khoản không active ném IllegalStateException")
        void testWithdrawOnInactiveAccountThrows() {
            BankAccount account = new BankAccount("ACC001", 0.0);
            account.deactivate();
            IllegalStateException ex = assertThrows(IllegalStateException.class,
                    () -> account.withdraw(5.0));
            assertTrue(ex.getMessage().contains("Account is inactive"));
        }
    }

    // -------------------- Transfer Tests --------------------
    @Nested
    @DisplayName("Transfer Operations")
    class TransferTests {

        @Test
        @DisplayName("Transfer tới tài khoản null ném IllegalArgumentException")
        void testTransferNullTargetThrows() {
            BankAccount source = new BankAccount("SRC", 100.0);
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                    () -> source.transfer(null, 20.0));
            assertTrue(ex.getMessage().contains("Target account cannot be null"));
        }

        @Test
        @DisplayName("Transfer tới tài khoản không active ném IllegalStateException")
        void testTransferToInactiveTargetThrows() {
            BankAccount source = new BankAccount("SRC", 100.0);
            BankAccount target = new BankAccount("TGT", 0.0);
            target.deactivate();
            IllegalStateException ex = assertThrows(IllegalStateException.class,
                    () -> source.transfer(target, 20.0));
            assertTrue(ex.getMessage().contains("Target account is inactive"));
        }

        @Test
        @DisplayName("Transfer thành công chuyển tiền giữa các tài khoản active")
        void testTransferSuccessful() {
            BankAccount source = new BankAccount("SRC", 150.0);
            BankAccount target = new BankAccount("TGT", 50.0);
            source.transfer(target, 40.0);
            assertEquals(110.0, source.getBalance(), 0.001);
            assertEquals(90.0, target.getBalance(), 0.001);
        }

        @Test
        @DisplayName("Transfer trên tài khoản không active ném IllegalStateException")
        void testTransferFromInactiveAccountThrows() {
            BankAccount source = new BankAccount("SRC", 0.0);
            source.deactivate();
            BankAccount target = new BankAccount("TGT", 0.0);
            IllegalStateException ex = assertThrows(IllegalStateException.class,
                    () -> source.transfer(target, 10.0));
            assertTrue(ex.getMessage().contains("Account is inactive"));
        }
    }

    // -------------------- Deactivate Tests --------------------
    @Nested
    @DisplayName("Deactivate Operations")
    class DeactivateTests {

        @Test
        @DisplayName("Deactivate khi số dư > 0 ném IllegalStateException")
        void testDeactivateWithPositiveBalanceThrows() {
            BankAccount account = new BankAccount("ACC001", 10.0);
            IllegalStateException ex = assertThrows(IllegalStateException.class,
                    account::deactivate);
            assertTrue(ex.getMessage().contains("Cannot deactivate account with non-zero balance"));
        }

        @Test
        @DisplayName("Deactivate thành công khi số dư = 0")
        void testDeactivateSuccessful() {
            BankAccount account = new BankAccount("ACC001", 0.0);
            account.deactivate();
            assertFalse(account.isActive());
        }

        @Test
        @DisplayName("Sau khi deactivate, mọi thao tác khác ném IllegalStateException")
        void testOperationsAfterDeactivationThrow() {
            BankAccount account = new BankAccount("ACC001", 0.0);
            account.deactivate();

            IllegalStateException exDeposit = assertThrows(IllegalStateException.class,
                    () -> account.deposit(10.0));
            assertTrue(exDeposit.getMessage().contains("Account is inactive"));

            IllegalStateException exWithdraw = assertThrows(IllegalStateException.class,
                    () -> account.withdraw(5.0));
            assertTrue(exWithdraw.getMessage().contains("Account is inactive"));

            IllegalStateException exTransfer = assertThrows(IllegalStateException.class,
                    () -> account.transfer(new BankAccount("TGT", 0.0), 5.0));
            assertTrue(exTransfer.getMessage().contains("Account is inactive"));
        }
    }
}
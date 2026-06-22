// Plan: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.platform.runner.JUnitPlatform;
import org.junit.runner.RunWith;
import org.junit.jupiter.api.RepetitionInfo;
import org.junit.jupiter.api.TestInfo;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

/**
 * TC-001: Kiểm tra @RepeatedTest thực thi phương thức số lần được chỉ định
 */
class RepeatedTestExecutionTest {
    private static final List<Integer> executionCounts = new ArrayList<>();
    
    @BeforeEach
    void reset() {
        executionCounts.clear();
    }
    
    @RepeatedTest(3)
    void testRepeatedExecution() {
        executionCounts.add(1);
    }
    
    @Test
    void verifyRepeatedTestExecutesCorrectNumberOfTimes() {
        // This test verifies the @RepeatedTest annotation works by checking execution count
        // Note: In a real scenario, we'd use a separate tracking mechanism
        assertEquals(3, executionCounts.size(), "Method should be executed exactly 3 times");
    }
}

/**
 * TC-002: Xác thực RepetitionInfo cung cấp tổng số lần lặp đúng
 */
class RepetitionInfoTotalRepetitionsTest {
    private static int totalRepetitions;
    
    @BeforeEach
    void reset() {
        totalRepetitions = 0;
    }
    
    @RepeatedTest(5)
    void testTotalRepetitions(RepetitionInfo repetitionInfo) {
        totalRepetitions = repetitionInfo.getTotalRepetitions();
    }
    
    @Test
    void verifyTotalRepetitionsIsCorrect() {
        assertEquals(5, totalRepetitions, "Total repetitions should be 5");
    }
}

/**
 * TC-003: Xác thực RepetitionInfo cung cấp số lần lặp hiện tại đúng
 */
class RepetitionInfoCurrentRepetitionTest {
    private static final List<Integer> currentRepetitions = new ArrayList<>();
    
    @RepeatedTest(4)
    void testCurrentRepetition(RepetitionInfo repetitionInfo) {
        currentRepetitions.add(repetitionInfo.getCurrentRepetition());
    }
    
    @Test
    void verifyCurrentRepetitionsAreSequential() {
        assertEquals(4, currentRepetitions.size(), "Should have 4 repetitions");
        assertEquals(1, currentRepetitions.get(0), "First repetition should be 1");
        assertEquals(2, currentRepetitions.get(1), "Second repetition should be 2");
        assertEquals(3, currentRepetitions.get(2), "Third repetition should be 3");
        assertEquals(4, currentRepetitions.get(3), "Fourth repetition should be 4");
    }
}

/**
 * TC-004: @BeforeEach nhận TestInfo và RepetitionInfo
 */
class BeforeEachWithRepetitionInfoTest {
    private static final List<Boolean> beforeEachCalled = new ArrayList<>();
    private static final List<String> testMethodNames = new ArrayList<>();
    
    @BeforeEach
    void beforeEach(TestInfo testInfo, RepetitionInfo repetitionInfo) {
        beforeEachCalled.add(true);
        testMethodNames.add(testInfo.getTestMethod().get().getName());
        assertNotNull(repetitionInfo, "RepetitionInfo should not be null");
        assertNotNull(testInfo, "TestInfo should not be null");
    }
    
    @RepeatedTest(2)
    void testWithBeforeEach() {
        // Test method body
    }
    
    @Test
    void verifyBeforeEachReceivesCorrectParameters() {
        assertEquals(2, beforeEachCalled.size(), "BeforeEach should be called twice");
        assertEquals("testWithBeforeEach", testMethodNames.get(0), "Method name should match");
        assertEquals("testWithBeforeEach", testMethodNames.get(1), "Method name should match");
    }
}

/**
 * TC-005: Tên hiển thị tùy chỉnh sử dụng placeholders
 */
class CustomDisplayNameTest {
    private static final List<String> displayNames = new ArrayList<>();
    
    @RepeatedTest(value = 3, name = "Run {currentRepetition} of {totalRepetitions} for {displayName}")
    void testCustomDisplayName(TestInfo testInfo) {
        displayNames.add(testInfo.getDisplayName());
    }
    
    @Test
    void verifyCustomDisplayNamesAreGenerated() {
        assertEquals(3, displayNames.size(), "Should have 3 display names");
        assertEquals("Run 1 of 3 for testCustomDisplayName", displayNames.get(0));
        assertEquals("Run 2 of 3 for testCustomDisplayName", displayNames.get(1));
        assertEquals("Run 3 of 3 for testCustomDisplayName", displayNames.get(2));
    }
}

/**
 * TC-006: Thoát ký tự @ trong placeholder bằng @@
 */
class EscapeAtCharacterTest {
    private static String displayName;
    
    @RepeatedTest(value = 1, name = "Email @@example.com")
    void testEscapeAtCharacter(TestInfo testInfo) {
        displayName = testInfo.getDisplayName();
    }
    
    @Test
    void verifyAtCharacterIsEscaped() {
        assertEquals("Email @example.com", displayName, "@@ should be converted to single @");
    }
}

/**
 * TC-007: Chạy lớp kiểm thử JUnit Platform với @RunWith(JUnitPlatform.class)
 */
@RunWith(JUnitPlatform.class)
class JUnit4RunnerCompatibilityTest {
    private static final List<Integer> executions = new ArrayList<>();
    
    @RepeatedTest(2)
    void testWithJUnit4Runner() {
        executions.add(1);
    }
    
    @Test
    void verifyJUnit4RunnerExecutesRepetitions() {
        assertEquals(2, executions.size(), "Both repetitions should execute with JUnit 4 runner");
    }
}

/**
 * TC-008: Xác thực JUnit 4 runner không hỗ trợ các tính năng JUnit Platform không được hỗ trợ
 */
@RunWith(JUnitPlatform.class)
class JUnit4RunnerUnsupportedFeaturesTest {
    @TestFactory
    Stream<DynamicTest> dynamicTests() {
        return Stream.of("a", "b", "c")
            .map(s -> DynamicTest.dynamicTest("test" + s, () -> assertTrue(true)));
    }
    
    @Test
    void verifyDynamicTestThrowsUnsupportedOperationException() {
        assertThrows(UnsupportedOperationException.class, () -> {
            dynamicTests().count();
        }, "Dynamic tests should throw UnsupportedOperationException with JUnit 4 runner");
    }
}
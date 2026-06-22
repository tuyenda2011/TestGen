# TÀI LIỆU CỐT LÕI (Rút gọn từ junit5_user_guide_official.pdf)

> **Tổng quan**: Giữ lại 142 trang, lọc bỏ 1 trang dư thừa (changelog, index, license...).

1. Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  5
1.1. What is JUnit 5? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  5
1.2. Supported Java Versions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  5
1.3. Getting Help . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  5
1.4. Getting Started. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  5
1.4.1. Downloading JUnit Artifacts. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  5
1.4.2. JUnit 5 Features . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  6
1.4.3. Example Projects. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  6
2. Writing Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  6
2.1. Annotations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  7
2.1.1. Meta-Annotations and Composed Annotations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  9
2.2. Test Classes and Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  10
2.3. Display Names. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  12
2.3.1. Display Name Generators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  12
2.3.2. Setting the Default Display Name Generator . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  14
2.4. Assertions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  15
2.4.1. Kotlin Assertion Support. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  18
2.4.2. Third-party Assertion Libraries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  20
2.5. Assumptions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  21
2.6. Disabling Tests. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  22
2.7. Conditional Test Execution. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  23
2.7.1. Operating System Conditions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  23
2.7.2. Java Runtime Environment Conditions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  24
2.7.3. System Property Conditions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  25
2.7.4. Environment Variable Conditions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  25
2.7.5. Script-based Conditions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  26
Script Bindings. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  27
2.8. Tagging and Filtering. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  28
2.8.1. Syntax Rules for Tags. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  28
2.9. Test Execution Order . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  29
2.10. Test Instance Lifecycle . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  30
2.10.1. Changing the Default Test Instance Lifecycle . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  31
2.11. Nested Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  31
2.12. Dependency Injection for Constructors and Methods. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  33
2.13. Test Interfaces and Default Methods. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  36
2.14. Repeated Tests. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  41

2.14.1. Repeated Test Examples . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  41
2.15. Parameterized Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  44
2.15.1. Required Setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  45
2.15.2. Consuming Arguments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  45
2.15.3. Sources of Arguments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  45
@ValueSource . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  45
Null and Empty Sources . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  46
@EnumSource . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  47
@MethodSource . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  48
@CsvSource . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  50
@CsvFileSource . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  51
@ArgumentsSource . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  51
2.15.4. Argument Conversion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  52
Widening Conversion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  52
Implicit Conversion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  52
Explicit Conversion. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  55
2.15.5. Argument Aggregation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  56
Custom Aggregators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  57
2.15.6. Customizing Display Names. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  58
2.15.7. Lifecycle and Interoperability . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  59
2.16. Test Templates . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  60
2.17. Dynamic Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  60
2.17.1. Dynamic Test Examples . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  61
2.17.2. URI Test Sources for Dynamic Tests. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  64
2.18. Timeouts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  65
2.18.1. Using @Timeout for Polling Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  67
2.19. Parallel Execution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  67
2.19.1. Configuration. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  71
2.19.2. Synchronization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  71
2.20. Built-in Extensions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  73
2.20.1. The TempDirectory Extension. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  73
3. Migrating from JUnit 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  74
3.1. Running JUnit 4 Tests on the JUnit Platform . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  74
3.1.1. Categories Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  75
3.2. Migration Tips . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  75
3.3. Limited JUnit 4 Rule Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  75
3.4. JUnit 4 @Ignore Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  76
4. Running Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  77
4.1. IDE Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  77
4.1.1. IntelliJ IDEA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  77
4.1.2. Eclipse . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  78

4.1.3. NetBeans . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  78
4.1.4. Visual Studio Code . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  78
4.1.5. Other IDEs. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  79
4.2. Build Support. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  79
4.2.1. Gradle . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  79
Configuration Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  79
Configuring Test Engines . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  80
Configuring Logging (optional) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  80
4.2.2. Maven . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  81
Configuring Test Engines . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  81
Filtering by Test Class Names . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  83
Filtering by Tags . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  84
Configuration Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  84
4.2.3. Ant . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  85
Basic Usage . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  85
4.3. Console Launcher. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  86
4.3.1. Options . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  87
4.3.2. Argument Files (@-files) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  90
4.4. Using JUnit 4 to run the JUnit Platform . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  90
4.4.1. Setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  90
Explicit Dependencies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  91
Transitive Dependencies. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  91
4.4.2. Display Names vs. Technical Names . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  91
4.4.3. Single Test Class. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  91
4.4.4. Test Suite. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  92
4.5. Configuration Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  93
4.6. Tag Expressions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  93
4.7. Capturing Standard Output/Error . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  94
5. Extension Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  94
5.1. Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  94
5.2. Registering Extensions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  95
5.2.1. Declarative Extension Registration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  95
5.2.2. Programmatic Extension Registration. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  96
Static Fields. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  96
Static Fields in Kotlin . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  97
Instance Fields . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  98
5.2.3. Automatic Extension Registration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  98
Enabling Automatic Extension Detection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  98
5.2.4. Extension Inheritance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  99
5.3. Conditional Test Execution. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  99
5.3.1. Deactivating Conditions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  99

Pattern Matching Syntax. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  100
5.4. Test Instance Factories . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  100
5.5. Test Instance Post-processing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  100
5.6. Parameter Resolution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  101
5.7. Test Result Processing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  101
5.8. Test Lifecycle Callbacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  102
5.8.1. Before and After Test Execution Callbacks. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  102
5.9. Exception Handling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  104
5.10. Intercepting Invocations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  107
5.11. Providing Invocation Contexts for Test Templates . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  108
5.12. Keeping State in Extensions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  109
5.13. Supported Utilities in Extensions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  110
5.13.1. Annotation Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  110
5.13.2. Class Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  110
5.13.3. Reflection Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  110
5.13.4. Modifier Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  110
5.14. Relative Execution Order of User Code and Extensions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  110
5.14.1. User and Extension Code . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  110
5.14.2. Wrapping Behavior of Callbacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  114
6. Advanced Topics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  123
6.1. JUnit Platform Launcher API. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  123
6.1.1. Discovering Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  123
6.1.2. Executing Tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  124
6.1.3. Plugging in your own Test Engine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  125
6.1.4. Plugging in your own Test Execution Listener . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  126
6.1.5. JUnit Platform Reporting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  126
6.1.6. Configuring the Launcher . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  126
6.2. JUnit Platform Test Kit. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  127
6.2.1. Engine Test Kit. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  127
6.2.2. Asserting Statistics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  129
6.2.3. Asserting Events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  130
7. API Evolution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  135
7.1. API Version and Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  136
7.2. Experimental APIs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  136
7.3. Deprecated APIs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  140
7.4. @API Tooling Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  140
8. Contributors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  141
9. Release Notes. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  141
10. Appendix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  141
10.1. Dependency Metadata . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  141
10.1.1. JUnit Platform . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  141

1. Overview
The goal of this document is to provide comprehensive reference documentation for programmers
writing tests, extension authors, and engine authors as well as build tool and IDE vendors.
1.1. What is JUnit 5?
Unlike previous versions of JUnit, JUnit 5 is composed of several different modules from three
different sub-projects.
JUnit 5 = JUnit Platform + JUnit Jupiter + JUnit Vintage
The JUnit Platform  serves as a foundation for launching testing frameworks  on the JVM. It also
defines the TestEngine API for developing a testing framework that runs on the platform.
Furthermore, the platform provides a Console Launcher to launch the platform from the command
line and a JUnit 4 based Runner  for running any TestEngine on the platform in a JUnit 4 based
environment. First-class support for the JUnit Platform also exists in popular IDEs (see IntelliJ IDEA,
Eclipse, NetBeans, and Visual Studio Code) and build tools (see Gradle, Maven, and Ant).
JUnit Jupiter is the combination of the new programming model and extension model for writing
tests and extensions in JUnit 5. The Jupiter sub-project provides a TestEngine for running Jupiter
based tests on the platform.
JUnit Vintage provides a TestEngine for running JUnit 3 and JUnit 4 based tests on the platform.
1.2. Supported Java Versions
JUnit 5 requires Java 8 (or higher) at runtime. However, you can still test code that has been
compiled with previous versions of the JDK.
1.3. Getting Help
Ask JUnit 5 related questions on Stack Overflow or chat with us on Gitter.
1.4. Getting Started
1.4.1. Downloading JUnit Artifacts
To find out what artifacts are available for download and inclusion in your project, refer to
Dependency Metadata. To set up dependency management for your build, refer to Build Support
10.1.2. JUnit Jupiter . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  142
10.1.3. JUnit Vintage . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  142
10.1.4. Bill of Materials (BOM) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  143
10.1.5. Dependencies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  143
10.2. Dependency Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  143

and the Example Projects.
1.4.2. JUnit 5 Features
To find out what features are available in JUnit 5 and how to use them, read the corresponding
sections of this User Guide, organized by topic.
• Writing Tests in JUnit Jupiter
• Migrating from JUnit 4 to JUnit Jupiter
• Running Tests
• Extension Model for JUnit Jupiter
• Advanced Topics
◦ JUnit Platform Launcher API
◦ JUnit Platform Test Kit
1.4.3. Example Projects
To see complete, working examples of projects that you can copy and experiment with, the junit5-
samples repository is a good place to start. The junit5-samples repository hosts a collection of
sample projects based on JUnit Jupiter, JUnit Vintage, and other testing frameworks. You’ll find
appropriate build scripts (e.g., build.gradle, pom.xml, etc.) in the example projects. The links below
highlight some of the combinations you can choose from.
• For Gradle and Java, check out the junit5-jupiter-starter-gradle project.
• For Gradle and Kotlin, check out the junit5-jupiter-starter-gradle-kotlin project.
• For Gradle and Groovy, check out the junit5-jupiter-starter-gradle-groovy project.
• For Maven, check out the junit5-jupiter-starter-maven project.
• For Ant, check out the junit5-jupiter-starter-ant project.
2. Writing Tests
The following example provides a glimpse at the minimum requirements for writing a test in JUnit
Jupiter. Subsequent sections of this chapter will provide further details on all available features.

A first test case
import static org.junit.jupiter.api.Assertions.assertEquals;
import example.util.Calculator;
import org.junit.jupiter.api.Test;
class MyFirstJUnitJupiterTests {
    private final Calculator calculator = new Calculator();
    @Test
    void addition() {
        assertEquals(2, calculator.add(1, 1));
    }
}
2.1. Annotations
JUnit Jupiter supports the following annotations for configuring tests and extending the framework.
Unless otherwise stated, all core annotations are located in the org.junit.jupiter.api package in
the junit-jupiter-api module.
Annotation Description
@Test Denotes that a method is a test method. Unlike JUnit 4’s @Test annotation, this
annotation does not declare any attributes, since test extensions in JUnit
Jupiter operate based on their own dedicated annotations. Such methods are
inherited unless they are overridden.
@ParameterizedTest Denotes that a method is a parameterized test. Such methods are inherited
unless they are overridden.
@RepeatedTest Denotes that a method is a test template for a repeated test. Such methods are
inherited unless they are overridden.
@TestFactory Denotes that a method is a test factory for dynamic tests. Such methods are
inherited unless they are overridden.
@TestTemplate Denotes that a method is a template for test cases designed to be invoked
multiple times depending on the number of invocation contexts returned by
the registered providers. Such methods are inherited unless they are
overridden.
@TestMethodOrder Used to configure the test method execution order for the annotated test class;
similar to JUnit 4’s @FixMethodOrder. Such annotations are inherited.
@TestInstance Used to configure the test instance lifecycle for the annotated test class. Such
annotations are inherited.

Annotation Description
@DisplayName Declares a custom display name for the test class or test method. Such
annotations are not inherited.
@DisplayNameGenera
tion
Declares a custom display name generator for the test class. Such annotations
are inherited.
@BeforeEach Denotes that the annotated method should be executed before each @Test,
@RepeatedTest, @ParameterizedTest, or @TestFactory method in the current class;
analogous to JUnit 4’s @Before. Such methods are inherited unless they are
overridden.
@AfterEach Denotes that the annotated method should be executed after each @Test,
@RepeatedTest, @ParameterizedTest, or @TestFactory method in the current class;
analogous to JUnit 4’s @After. Such methods are inherited unless they are
overridden.
@BeforeAll Denotes that the annotated method should be executed before all @Test,
@RepeatedTest, @ParameterizedTest, and @TestFactory methods in the current
class; analogous to JUnit 4’s @BeforeClass. Such methods are inherited (unless
they are hidden or overridden) and must be static (unless the "per-class" test
instance lifecycle is used).
@AfterAll Denotes that the annotated method should be executed after all @Test,
@RepeatedTest, @ParameterizedTest, and @TestFactory methods in the current
class; analogous to JUnit 4’s @AfterClass. Such methods are inherited (unless
they are hidden or overridden) and must be static (unless the "per-class" test
instance lifecycle is used).
@Nested Denotes that the annotated class is a non-static nested test class. @BeforeAll
and @AfterAll methods cannot be used directly in a @Nested test class unless
the "per-class" test instance lifecycle is used. Such annotations are not
inherited.
@Tag Used to declare tags for filtering tests, either at the class or method level;
analogous to test groups in TestNG or Categories in JUnit 4. Such annotations
are inherited at the class level but not at the method level.
@Disabled Used to disable a test class or test method; analogous to JUnit 4’s @Ignore. Such
annotations are not inherited.
@Timeout Used to fail a test, test factory, test template, or lifecycle method if its execution
exceeds a given duration. Such annotations are inherited.
@ExtendWith Used to register extensions declaratively. Such annotations are inherited.
@RegisterExtension Used to register extensions programmatically via fields. Such fields are
inherited unless they are shadowed.
@TempDir Used to supply a temporary directory via field injection or parameter injection
in a lifecycle method or test method; located in the org.junit.jupiter.api.io
package.

 Some annotations may currently be experimental. Consult the table in
Experimental APIs for details.
2.1.1. Meta-Annotations and Composed Annotations
JUnit Jupiter annotations can be used as meta-annotations. That means that you can define your
own composed annotation that will automatically inherit the semantics of its meta-annotations.
For example, instead of copying and pasting @Tag("fast") throughout your code base (see Tagging
and Filtering), you can create a custom composed annotation named @Fast as follows. @Fast can then
be used as a drop-in replacement for @Tag("fast").
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.junit.jupiter.api.Tag;
@Target({ ElementType.TYPE, ElementType.METHOD })
@Retention(RetentionPolicy.RUNTIME)
@Tag("fast")
public @interface Fast {
}
The following @Test method demonstrates usage of the @Fast annotation.
@Fast
@Test
void myFastTest() {
    // ...
}
You can even take that one step further by introducing a custom @FastTest annotation that can be
used as a drop-in replacement for @Tag("fast") and @Test.

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Tag("fast")
@Test
public @interface FastTest {
}
JUnit automatically recognizes the following as a @Test method that is tagged with "fast".
@FastTest
void myFastTest() {
    // ...
}
2.2. Test Classes and Methods
Test Class: any top-level class, static member class, or @Nested class that contains at least one test
method.
Test classes must not be abstract and must have a single constructor.
Test Method : any instance method that is directly annotated or meta-annotated with @Test,
@RepeatedTest, @ParameterizedTest, @TestFactory, or @TestTemplate.
Lifecycle Method : any method that is directly annotated or meta-annotated with @BeforeAll,
@AfterAll, @BeforeEach, or @AfterEach.
Test methods and lifecycle methods may be declared locally within the current test class, inherited
from superclasses, or inherited from interfaces (see Test Interfaces and Default Methods ). In
addition, test methods and lifecycle methods must not be abstract and must not return a value.
 Test classes, test methods, and lifecycle methods are not required to be public, but
they must not be private.
The following test class demonstrates the use of @Test methods and all supported lifecycle methods.
For further information on runtime semantics, see Test Execution Order and Wrapping Behavior of
Callbacks.
A standard test class

import static org.junit.jupiter.api.Assertions.fail;
import static org.junit.jupiter.api.Assumptions.assumeTrue;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
class StandardTests {
    @BeforeAll
    static void initAll() {
    }
    @BeforeEach
    void init() {
    }
    @Test
    void succeedingTest() {
    }
    @Test
    void failingTest() {
        fail("a failing test");
    }
    @Test
    @Disabled("for demonstration purposes")
    void skippedTest() {
        // not executed
    }
    @Test
    void abortedTest() {
        assumeTrue("abc".contains("Z"));
        fail("test should have been aborted");
    }
    @AfterEach
    void tearDown() {
    }
    @AfterAll
    static void tearDownAll() {
    }
}

2.3. Display Names
Test classes and test methods can declare custom display names via @DisplayName — with spaces,
special characters, and even emojis — that will be displayed in test reports and by test runners and
IDEs.
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
@DisplayName("A special test case")
class DisplayNameDemo {
    @Test
    @DisplayName("Custom test name containing spaces")
    void testWithDisplayNameContainingSpaces() {
    }
    @Test
    @DisplayName("╯°□°）╯")
    void testWithDisplayNameContainingSpecialCharacters() {
    }
    @Test
    @DisplayName(" ")
    void testWithDisplayNameContainingEmoji() {
    }
}
2.3.1. Display Name Generators
JUnit Jupiter supports custom display name generators that can be configured via the
@DisplayNameGeneration annotation. Values provided via @DisplayName annotations always take
precedence over display names generated by a DisplayNameGenerator.
import java.lang.reflect.Method;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.DisplayNameGeneration;
import org.junit.jupiter.api.DisplayNameGenerator;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
class DisplayNameGeneratorDemo {
    @Nested

@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)
    class A_year_is_not_supported {
        @Test
        void if_it_is_zero() {
        }
        @DisplayName("A negative value for year is not supported by the leap year
computation.")
        @ParameterizedTest(name = "For example, year {0} is not supported.")
        @ValueSource(ints = { -1, -4 })
        void if_it_is_negative(int year) {
        }
    }
    @Nested
    @DisplayNameGeneration(IndicativeSentences.class)
    class A_year_is_a_leap_year {
        @Test
        void if_it_is_divisible_by_4_but_not_by_100() {
        }
        @ParameterizedTest(name = "Year {0} is a leap year.")
        @ValueSource(ints = { 2016, 2020, 2048 })
        void if_it_is_one_of_the_following_years(int year) {
        }
    }
    static class IndicativeSentences extends DisplayNameGenerator.ReplaceUnderscores {
        @Override
        public String generateDisplayNameForClass(Class<?> testClass) {
            return super.generateDisplayNameForClass(testClass);
        }
        @Override
        public String generateDisplayNameForNestedClass(Class<?> nestedClass) {
            return super.generateDisplayNameForNestedClass(nestedClass) + "...";
        }
        @Override
        public String generateDisplayNameForMethod(Class<?> testClass, Method
testMethod) {
            String name = testClass.getSimpleName() + ' ' + testMethod.getName();
            return name.replace('_', ' ') + '.';
        }
    }

}
+-- DisplayNameGeneratorDemo [OK]
  +-- A year is not supported [OK]
  | +-- A negative value for year is not supported by the leap year computation. [OK]
  | | +-- For example, year -1 is not supported. [OK]
  | | '-- For example, year -4 is not supported. [OK]
  | '-- if it is zero() [OK]
  '-- A year is a leap year... [OK]
    +-- A year is a leap year if it is divisible by 4 but not by 100. [OK]
    '-- A year is a leap year if it is one of the following years. [OK]
      +-- Year 2016 is a leap year. [OK]
      +-- Year 2020 is a leap year. [OK]
      '-- Year 2048 is a leap year. [OK]
2.3.2. Setting the Default Display Name Generator
You can use the junit.jupiter.displayname.generator.default configuration parameter  to specify
the fully qualified class name of the DisplayNameGenerator you would like to use by default. Just like
for display name generators configured via the @DisplayNameGeneration annotation, the supplied
class has to implement the DisplayNameGenerator interface. The default display name generator will
be used for all tests unless the @DisplayNameGeneration annotation is present on an enclosing test
class or test interface. Values provided via @DisplayName annotations always take precedence over
display names generated by a DisplayNameGenerator.
For example, to use the ReplaceUnderscores display name generator by default, you should set the
configuration parameter to the corresponding fully qualified class name (e.g., in
src/test/resources/junit-platform.properties):
junit.jupiter.displayname.generator.default = \
    org.junit.jupiter.api.DisplayNameGenerator$ReplaceUnderscores
Similarly, you can specify the fully qualified name of any custom class that implements
DisplayNameGenerator.
In summary, the display name for a test class or method is determined according to the following
precedence rules:
1. value of the @DisplayName annotation, if present
2. by calling the DisplayNameGenerator specified in the @DisplayNameGeneration annotation, if
present
3. by calling the default DisplayNameGenerator configured via the configuration parameter, if
present
4. by calling org.junit.jupiter.api.DisplayNameGenerator.Standard

2.4. Assertions
JUnit Jupiter comes with many of the assertion methods that JUnit 4 has and adds a few that lend
themselves well to being used with Java 8 lambdas. All JUnit Jupiter assertions are static methods
in the org.junit.jupiter.api.Assertions class.
import static java.time.Duration.ofMillis;
import static java.time.Duration.ofMinutes;
import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeout;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;
import example.domain.Person;
import example.util.Calculator;
import org.junit.jupiter.api.Test;
class AssertionsDemo {
    private final Calculator calculator = new Calculator();
    private final Person person = new Person("Jane", "Doe");
    @Test
    void standardAssertions() {
        assertEquals(2, calculator.add(1, 1));
        assertEquals(4, calculator.multiply(2, 2),
                "The optional failure message is now the last parameter");
        assertTrue('a' < 'b', () -> "Assertion messages can be lazily evaluated -- "
                + "to avoid constructing complex messages unnecessarily.");
    }
    @Test
    void groupedAssertions() {
        // In a grouped assertion all assertions are executed, and all
        // failures will be reported together.
        assertAll("person",
            () -> assertEquals("Jane", person.getFirstName()),
            () -> assertEquals("Doe", person.getLastName())
        );
    }
    @Test
    void dependentAssertions() {
        // Within a code block, if an assertion fails the
        // subsequent code in the same block will be skipped.

assertAll("properties",
            () -> {
                String firstName = person.getFirstName();
                assertNotNull(firstName);
                // Executed only if the previous assertion is valid.
                assertAll("first name",
                    () -> assertTrue(firstName.startsWith("J")),
                    () -> assertTrue(firstName.endsWith("e"))
                );
            },
            () -> {
                // Grouped assertion, so processed independently
                // of results of first name assertions.
                String lastName = person.getLastName();
                assertNotNull(lastName);
                // Executed only if the previous assertion is valid.
                assertAll("last name",
                    () -> assertTrue(lastName.startsWith("D")),
                    () -> assertTrue(lastName.endsWith("e"))
                );
            }
        );
    }
    @Test
    void exceptionTesting() {
        Exception exception = assertThrows(ArithmeticException.class, () ->
            calculator.divide(1, 0));
        assertEquals("/ by zero", exception.getMessage());
    }
    @Test
    void timeoutNotExceeded() {
        // The following assertion succeeds.
        assertTimeout(ofMinutes(2), () -> {
            // Perform task that takes less than 2 minutes.
        });
    }
    @Test
    void timeoutNotExceededWithResult() {
        // The following assertion succeeds, and returns the supplied object.
        String actualResult = assertTimeout(ofMinutes(2), () -> {
            return "a result";
        });
        assertEquals("a result", actualResult);
    }
    @Test

void timeoutNotExceededWithMethod() {
        // The following assertion invokes a method reference and returns an object.
        String actualGreeting = assertTimeout(ofMinutes(2), AssertionsDemo::greeting);
        assertEquals("Hello, World!", actualGreeting);
    }
    @Test
    void timeoutExceeded() {
        // The following assertion fails with an error message similar to:
        // execution exceeded timeout of 10 ms by 91 ms
        assertTimeout(ofMillis(10), () -> {
            // Simulate task that takes more than 10 ms.
            Thread.sleep(100);
        });
    }
    @Test
    void timeoutExceededWithPreemptiveTermination() {
        // The following assertion fails with an error message similar to:
        // execution timed out after 10 ms
        assertTimeoutPreemptively(ofMillis(10), () -> {
            // Simulate task that takes more than 10 ms.
            Thread.sleep(100);
        });
    }
    private static String greeting() {
        return "Hello, World!";
    }
}


Preemptive Timeouts with assertTimeoutPreemptively()
Contrary to declarative timeouts, the various assertTimeoutPreemptively() methods
in the Assertions class execute the provided executable or supplier in a different
thread than that of the calling code. This behavior can lead to undesirable side
effects if the code that is executed within the executable or supplier relies on
java.lang.ThreadLocal storage.
One common example of this is the transactional testing support in the Spring
Framework. Specifically, Spring’s testing support binds transaction state to the
current thread (via a ThreadLocal) before a test method is invoked. Consequently, if
an executable or supplier provided to assertTimeoutPreemptively() invokes Spring-
managed components that participate in transactions, any actions taken by those
components will not be rolled back with the test-managed transaction. On the
contrary, such actions will be committed to the persistent store (e.g., relational
database) even though the test-managed transaction is rolled back.
Similar side effects may be encountered with other frameworks that rely on
ThreadLocal storage.
2.4.1. Kotlin Assertion Support
JUnit Jupiter also comes with a few assertion methods that lend themselves well to being used in
Kotlin. All JUnit Jupiter Kotlin assertions are top-level functions in the org.junit.jupiter.api
package.
import example.domain.Person
import example.util.Calculator
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertAll
import org.junit.jupiter.api.assertDoesNotThrow
import org.junit.jupiter.api.assertThrows
import org.junit.jupiter.api.assertTimeout
import org.junit.jupiter.api.assertTimeoutPreemptively
import java.time.Duration
class KotlinAssertionsDemo {
    private val person = Person("Jane", "Doe")
    private val people = setOf(person, Person("John", "Doe"))
    @Test
    fun `exception absence testing`() {
        val calculator = Calculator()
        val result = assertDoesNotThrow("Should not throw an exception") {
            calculator.divide(0, 1)
        }
        assertEquals(0, result)

}
    @Test
    fun `expected exception testing`() {
        val calculator = Calculator()
        val exception = assertThrows<ArithmeticException> ("Should throw an exception
") {
            calculator.divide(1, 0)
        }
        assertEquals("/ by zero", exception.message)
    }
    @Test
    fun `grouped assertions`() {
        assertAll("Person properties",
            { assertEquals("Jane", person.firstName) },
            { assertEquals("Doe", person.lastName) }
        )
    }
    @Test
    fun `grouped assertions from a stream`() {
        assertAll("People with first name starting with J",
            people
                .stream()
                .map {
                    // This mapping returns Stream<() -> Unit>
                    { assertTrue(it.firstName.startsWith("J")) }
                }
        )
    }
    @Test
    fun `grouped assertions from a collection`() {
        assertAll("People with last name of Doe",
            people.map { { assertEquals("Doe", it.lastName) } }
        )
    }
    @Test
    fun `timeout not exceeded testing`() {
        val fibonacciCalculator = FibonacciCalculator()
        val result = assertTimeout(Duration.ofMillis(100)) {
            fibonacciCalculator.fib(14)
        }
        assertEquals(377, result)
    }
    @Test
    fun `timeout exceeded with preemptive termination`() {
        // The following assertion fails with an error message similar to:

// execution timed out after 10 ms
        assertTimeoutPreemptively(Duration.ofMillis(10)) {
            // Simulate task that takes more than 10 ms.
            Thread.sleep(100)
        }
    }
}
2.4.2. Third-party Assertion Libraries
Even though the assertion facilities provided by JUnit Jupiter are sufficient for many testing
scenarios, there are times when more power and additional functionality such as matchers are
desired or required. In such cases, the JUnit team recommends the use of third-party assertion
libraries such as AssertJ, Hamcrest, Truth, etc. Developers are therefore free to use the assertion
library of their choice.
For example, the combination of matchers and a fluent API can be used to make assertions more
descriptive and readable. However, JUnit Jupiter’s org.junit.jupiter.api.Assertions class does not
provide an assertThat() method like the one found in JUnit 4’s org.junit.Assert class which accepts
a Hamcrest Matcher. Instead, developers are encouraged to use the built-in support for matchers
provided by third-party assertion libraries.
The following example demonstrates how to use the assertThat() support from Hamcrest in a JUnit
Jupiter test. As long as the Hamcrest library has been added to the classpath, you can statically
import methods such as assertThat(), is(), and equalTo() and then use them in tests like in the
assertWithHamcrestMatcher() method below.
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;
import example.util.Calculator;
import org.junit.jupiter.api.Test;
class HamcrestAssertionsDemo {
    private final Calculator calculator = new Calculator();
    @Test
    void assertWithHamcrestMatcher() {
        assertThat(calculator.subtract(4, 1), is(equalTo(3)));
    }
}
Naturally, legacy tests based on the JUnit 4 programming model can continue using
org.junit.Assert#assertThat.

2.5. Assumptions
JUnit Jupiter comes with a subset of the assumption methods that JUnit 4 provides and adds a few
that lend themselves well to being used with Java 8 lambda expressions and method references. All
JUnit Jupiter assumptions are static methods in the org.junit.jupiter.api.Assumptions class.
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assumptions.assumeTrue;
import static org.junit.jupiter.api.Assumptions.assumingThat;
import example.util.Calculator;
import org.junit.jupiter.api.Test;
class AssumptionsDemo {
    private final Calculator calculator = new Calculator();
    @Test
    void testOnlyOnCiServer() {
        assumeTrue("CI".equals(System.getenv("ENV")));
        // remainder of test
    }
    @Test
    void testOnlyOnDeveloperWorkstation() {
        assumeTrue("DEV".equals(System.getenv("ENV")),
            () -> "Aborting test: not on developer workstation");
        // remainder of test
    }
    @Test
    void testInAllEnvironments() {
        assumingThat("CI".equals(System.getenv("ENV")),
            () -> {
                // perform these assertions only on the CI server
                assertEquals(2, calculator.divide(4, 2));
            });
        // perform these assertions in all environments
        assertEquals(42, calculator.multiply(6, 7));
    }
}


As of JUnit Jupiter 5.4, it is also possible to use methods from JUnit 4’s
org.junit.Assume class for assumptions. Specifically, JUnit Jupiter supports JUnit 4’s
AssumptionViolatedException to signal that a test should be aborted instead of
marked as a failure.
2.6. Disabling Tests
Entire test classes or individual test methods may be disabled via the @Disabled annotation, via one
of the annotations discussed in Conditional Test Execution, or via a custom ExecutionCondition.
Here’s a @Disabled test class.
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
@Disabled("Disabled until bug #99 has been fixed")
class DisabledClassDemo {
    @Test
    void testWillBeSkipped() {
    }
}
And here’s a test class that contains a @Disabled test method.
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
class DisabledTestsDemo {
    @Disabled("Disabled until bug #42 has been resolved")
    @Test
    void testWillBeSkipped() {
    }
    @Test
    void testWillBeExecuted() {
    }
}


@Disabled may be declared without providing a reason; however, the JUnit team
recommends that developers provide a short explanation for why a test class or
test method has been disabled. Consequently, the above examples both show the
use of a reason — for example, @Disabled("Disabled until bug #42 has been
resolved"). Some development teams even require the presence of issue tracking
numbers in the reason for automated traceability, etc.
2.7. Conditional Test Execution
The ExecutionCondition extension API in JUnit Jupiter allows developers to either enable or disable a
container or test based on certain conditions programmatically. The simplest example of such a
condition is the built-in DisabledCondition which supports the @Disabled annotation (see Disabling
Tests). In addition to @Disabled, JUnit Jupiter also supports several other annotation-based
conditions in the org.junit.jupiter.api.condition package that allow developers to enable or
disable containers and tests declaratively. See the following sections for details.

Composed Annotations
Note that any of the conditional annotations listed in the following sections may
also be used as a meta-annotation in order to create a custom composed
annotation. For example, the @TestOnMac annotation in the @EnabledOnOs demo 
shows how you can combine @Test and @EnabledOnOs in a single, reusable
annotation.

Each of the conditional annotations listed in the following sections can only be
declared once on a given test interface, test class, or test method. If a conditional
annotation is directly present, indirectly present, or meta-present multiple times
on a given element, only the first such annotation discovered by JUnit will be used;
any additional declarations will be silently ignored. Note, however, that each
conditional annotation may be used in conjunction with other conditional
annotations in the org.junit.jupiter.api.condition package.
2.7.1. Operating System Conditions
A container or test may be enabled or disabled on a particular operating system via the
@EnabledOnOs and @DisabledOnOs annotations.

@Test
@EnabledOnOs(MAC)
void onlyOnMacOs() {
    // ...
}
@TestOnMac
void testOnMac() {
    // ...
}
@Test
@EnabledOnOs({ LINUX, MAC })
void onLinuxOrMac() {
    // ...
}
@Test
@DisabledOnOs(WINDOWS)
void notOnWindows() {
    // ...
}
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Test
@EnabledOnOs(MAC)
@interface TestOnMac {
}
2.7.2. Java Runtime Environment Conditions
A container or test may be enabled or disabled on a particular version of the Java Runtime
Environment (JRE) via the @EnabledOnJre and @DisabledOnJre annotations.

@Test
@EnabledOnJre(JAVA_8)
void onlyOnJava8() {
    // ...
}
@Test
@EnabledOnJre({ JAVA_9, JAVA_10 })
void onJava9Or10() {
    // ...
}
@Test
@DisabledOnJre(JAVA_9)
void notOnJava9() {
    // ...
}
2.7.3. System Property Conditions
A container or test may be enabled or disabled based on the value of the named JVM system property
via the @EnabledIfSystemProperty and @DisabledIfSystemProperty annotations. The value supplied
via the matches attribute will be interpreted as a regular expression.
@Test
@EnabledIfSystemProperty(named = "os.arch", matches = ".*64.*")
void onlyOn64BitArchitectures() {
    // ...
}
@Test
@DisabledIfSystemProperty(named = "ci-server", matches = "true")
void notOnCiServer() {
    // ...
}
2.7.4. Environment Variable Conditions
A container or test may be enabled or disabled based on the value of the named environment
variable from the underlying operating system via the @EnabledIfEnvironmentVariable and
@DisabledIfEnvironmentVariable annotations. The value supplied via the matches attribute will be
interpreted as a regular expression.

@Test
@EnabledIfEnvironmentVariable(named = "ENV", matches = "staging-server")
void onlyOnStagingServer() {
    // ...
}
@Test
@DisabledIfEnvironmentVariable(named = "ENV", matches = ".*development.*")
void notOnDeveloperWorkstation() {
    // ...
}
2.7.5. Script-based Conditions
 Conditional test execution via @EnabledIf and @DisabledIf is deprecated for
removal in a future release of JUnit Jupiter.
JUnit Jupiter provides the ability to either enable or disable a container or test depending on the
evaluation of a script configured via the @EnabledIf or @DisabledIf annotation. Scripts can be
written in JavaScript, Groovy, or any other scripting language for which there is support for the
Java Scripting API, defined by JSR 223.

If the logic of your script depends only on the current operating system, the
current Java Runtime Environment version, a particular JVM system property, or a
particular environment variable, you should consider using one of the built-in
annotations dedicated to that purpose. See the previous sections of this chapter for
further details.

If you find yourself using the same script-based condition many times, consider
writing a dedicated ExecutionCondition extension in order to implement the
condition in a faster, type-safe, and more maintainable manner.

@Test // Static JavaScript expression.
@EnabledIf("2 * 3 == 6")
void willBeExecuted() {
    // ...
}
@RepeatedTest(10) // Dynamic JavaScript expression.
@DisabledIf("Math.random() < 0.314159")
void mightNotBeExecuted() {
    // ...
}
@Test // Regular expression testing bound system property.
@DisabledIf("/32/.test(systemProperty.get('os.arch'))")
void disabledOn32BitArchitectures() {
    assertFalse(System.getProperty("os.arch").contains("32"));
}
@Test
@EnabledIf("'CI' == systemEnvironment.get('ENV')")
void onlyOnCiServer() {
    assertTrue("CI".equals(System.getenv("ENV")));
}
@Test // Multi-line script, custom engine name and custom reason.
@EnabledIf(value = {
                "load('nashorn:mozilla_compat.js')",
                "importPackage(java.time)",
                "",
                "var today = LocalDate.now()",
                "var tomorrow = today.plusDays(1)",
                "tomorrow.isAfter(today)"
            },
            engine = "nashorn",
            reason = "Self-fulfilling: {result}")
void theDayAfterTomorrow() {
    LocalDate today = LocalDate.now();
    LocalDate tomorrow = today.plusDays(1);
    assertTrue(tomorrow.isAfter(today));
}
Script Bindings
The following names are bound to each script context and therefore usable within the script. An
accessor provides access to a map-like structure via a simple String get(String name) method.
Name Type Description
systemEnvironment accessor Operating system environment variable accessor.

Name Type Description
systemProperty accessor JVM system property accessor.
junitConfiguration
Parameter
accessor Configuration parameter accessor.
junitDisplayName String Display name of the test or container.
junitTags Set<String> All tags assigned to the test or container.
junitUniqueId String Unique ID of the test or container.
2.8. Tagging and Filtering
Test classes and methods can be tagged via the @Tag annotation. Those tags can later be used to
filter test discovery and execution.
 See also: Tag Expressions
2.8.1. Syntax Rules for Tags
• A tag must not be null or blank.
• A trimmed tag must not contain whitespace.
• A trimmed tag must not contain ISO control characters.
• A trimmed tag must not contain any of the following reserved characters.
◦ ,: comma
◦ (: left parenthesis
◦ ): right parenthesis
◦ &: ampersand
◦ |: vertical bar
◦ !: exclamation point
 In the above context, "trimmed" means that leading and trailing whitespace
characters have been removed.

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
@Tag("fast")
@Tag("model")
class TaggingDemo {
    @Test
    @Tag("taxes")
    void testingTaxCalculation() {
    }
}
 See Meta-Annotations and Composed Annotations  for examples demonstrating
how to create custom annotations for tags.
2.9. Test Execution Order
By default, test methods will be ordered using an algorithm that is deterministic but intentionally
nonobvious. This ensures that subsequent runs of a test suite execute test methods in the same
order, thereby allowing for repeatable builds.
 See Test Classes and Methods for a definition of test method.
Although true unit tests typically should not rely on the order in which they are executed, there are
times when it is necessary to enforce a specific test method execution order — for example, when
writing integration tests or functional tests where the sequence of the tests is important, especially
in conjunction with @TestInstance(Lifecycle.PER_CLASS).
To control the order in which test methods are executed, annotate your test class or test interface
with @TestMethodOrder and specify the desired MethodOrderer implementation. You can implement
your own custom MethodOrderer or use one of the following built-in MethodOrderer implementations.
• Alphanumeric: sorts test methods alphanumerically based on their names and formal parameter
lists.
• OrderAnnotation: sorts test methods numerically based on values specified via the @Order
annotation.
• Random: orders test methods pseudo-randomly and supports configuration of a custom seed.
 See also: Wrapping Behavior of Callbacks
The following example demonstrates how to guarantee that test methods are executed in the order
specified via the @Order annotation.

import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
@TestMethodOrder(OrderAnnotation.class)
class OrderedTestsDemo {
    @Test
    @Order(1)
    void nullValues() {
        // perform assertions against null values
    }
    @Test
    @Order(2)
    void emptyValues() {
        // perform assertions against empty values
    }
    @Test
    @Order(3)
    void validValues() {
        // perform assertions against valid values
    }
}
2.10. Test Instance Lifecycle
In order to allow individual test methods to be executed in isolation and to avoid unexpected side
effects due to mutable test instance state, JUnit creates a new instance of each test class before
executing each test method (see Test Classes and Methods). This "per-method" test instance lifecycle
is the default behavior in JUnit Jupiter and is analogous to all previous versions of JUnit.

Please note that the test class will still be instantiated if a given test method  is
disabled via a condition (e.g., @Disabled, @DisabledOnOs, etc.) even when the "per-
method" test instance lifecycle mode is active.
If you would prefer that JUnit Jupiter execute all test methods on the same test instance, annotate
your test class with @TestInstance(Lifecycle.PER_CLASS). When using this mode, a new test instance
will be created once per test class. Thus, if your test methods rely on state stored in instance
variables, you may need to reset that state in @BeforeEach or @AfterEach methods.
The "per-class" mode has some additional benefits over the default "per-method" mode. Specifically,
with the "per-class" mode it becomes possible to declare @BeforeAll and @AfterAll on non-static
methods as well as on interface default methods. The "per-class" mode therefore also makes it
possible to use @BeforeAll and @AfterAll methods in @Nested test classes.

If you are authoring tests using the Kotlin programming language, you may also find it easier to
implement @BeforeAll and @AfterAll methods by switching to the "per-class" test instance lifecycle
mode.
2.10.1. Changing the Default Test Instance Lifecycle
If a test class or test interface is not annotated with @TestInstance, JUnit Jupiter will use a default
lifecycle mode. The standard default mode is PER_METHOD; however, it is possible to change the
default for the execution of an entire test plan. To change the default test instance lifecycle mode,
set the junit.jupiter.testinstance.lifecycle.default configuration parameter  to the name of an
enum constant defined in TestInstance.Lifecycle, ignoring case. This can be supplied as a JVM
system property, as a configuration parameter in the LauncherDiscoveryRequest that is passed to the
Launcher, or via the JUnit Platform configuration file (see Configuration Parameters for details).
For example, to set the default test instance lifecycle mode to Lifecycle.PER_CLASS, you can start
your JVM with the following system property.
-Djunit.jupiter.testinstance.lifecycle.default=per_class
Note, however, that setting the default test instance lifecycle mode via the JUnit Platform
configuration file is a more robust solution since the configuration file can be checked into a
version control system along with your project and can therefore be used within IDEs and your
build software.
To set the default test instance lifecycle mode to Lifecycle.PER_CLASS via the JUnit Platform
configuration file, create a file named junit-platform.properties in the root of the class path (e.g.,
src/test/resources) with the following content.
junit.jupiter.testinstance.lifecycle.default = per_class

Changing the default test instance lifecycle mode can lead to unpredictable results
and fragile builds if not applied consistently. For example, if the build configures
"per-class" semantics as the default but tests in the IDE are executed using "per-
method" semantics, that can make it difficult to debug errors that occur on the
build server. It is therefore recommended to change the default in the JUnit
Platform configuration file instead of via a JVM system property.
2.11. Nested Tests
@Nested tests give the test writer more capabilities to express the relationship among several groups
of tests. Here’s an elaborate example.
Nested test suite for testing a stack
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.util.EmptyStackException;

import java.util.Stack;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
@DisplayName("A stack")
class TestingAStackDemo {
    Stack<Object> stack;
    @Test
    @DisplayName("is instantiated with new Stack()")
    void isInstantiatedWithNew() {
        new Stack<>();
    }
    @Nested
    @DisplayName("when new")
    class WhenNew {
        @BeforeEach
        void createNewStack() {
            stack = new Stack<>();
        }
        @Test
        @DisplayName("is empty")
        void isEmpty() {
            assertTrue(stack.isEmpty());
        }
        @Test
        @DisplayName("throws EmptyStackException when popped")
        void throwsExceptionWhenPopped() {
            assertThrows(EmptyStackException.class, stack::pop);
        }
        @Test
        @DisplayName("throws EmptyStackException when peeked")
        void throwsExceptionWhenPeeked() {
            assertThrows(EmptyStackException.class, stack::peek);
        }
        @Nested
        @DisplayName("after pushing an element")
        class AfterPushing {
            String anElement = "an element";

@BeforeEach
            void pushAnElement() {
                stack.push(anElement);
            }
            @Test
            @DisplayName("it is no longer empty")
            void isNotEmpty() {
                assertFalse(stack.isEmpty());
            }
            @Test
            @DisplayName("returns the element when popped and is empty")
            void returnElementWhenPopped() {
                assertEquals(anElement, stack.pop());
                assertTrue(stack.isEmpty());
            }
            @Test
            @DisplayName("returns the element when peeked but remains not empty")
            void returnElementWhenPeeked() {
                assertEquals(anElement, stack.peek());
                assertFalse(stack.isEmpty());
            }
        }
    }
}

Only non-static nested classes  (i.e. inner classes ) can serve as @Nested test classes.
Nesting can be arbitrarily deep, and those inner classes are considered to be full
members of the test class family with one exception: @BeforeAll and @AfterAll
methods do not work by default . The reason is that Java does not allow static
members in inner classes. However, this restriction can be circumvented by
annotating a @Nested test class with @TestInstance(Lifecycle.PER_CLASS) (see Test
Instance Lifecycle).
2.12. Dependency Injection for Constructors and
Methods
In all prior JUnit versions, test constructors or methods were not allowed to have parameters (at
least not with the standard Runner implementations). As one of the major changes in JUnit Jupiter,
both test constructors and methods are now permitted to have parameters. This allows for greater
flexibility and enables Dependency Injection for constructors and methods.
ParameterResolver defines the API for test extensions that wish to dynamically resolve parameters at
runtime. If a test class  constructor, a test method , or a lifecycle method  (see Test Classes and
Methods) accepts a parameter, the parameter must be resolved at runtime by a registered
ParameterResolver.

There are currently three built-in resolvers that are registered automatically.
• TestInfoParameterResolver: if a constructor or method parameter is of type TestInfo, the
TestInfoParameterResolver will supply an instance of TestInfo corresponding to the current
container or test as the value for the parameter. The TestInfo can then be used to retrieve
information about the current container or test such as the display name, the test class, the test
method, and associated tags. The display name is either a technical name, such as the name of
the test class or test method, or a custom name configured via @DisplayName.
TestInfo acts as a drop-in replacement for the TestName rule from JUnit 4. The following
demonstrates how to have TestInfo injected into a test constructor, @BeforeEach method, and
@Test method.
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInfo;
@DisplayName("TestInfo Demo")
class TestInfoDemo {
    TestInfoDemo(TestInfo testInfo) {
        assertEquals("TestInfo Demo", testInfo.getDisplayName());
    }
    @BeforeEach
    void init(TestInfo testInfo) {
        String displayName = testInfo.getDisplayName();
        assertTrue(displayName.equals("TEST 1") || displayName.equals("test2()"));
    }
    @Test
    @DisplayName("TEST 1")
    @Tag("my-tag")
    void test1(TestInfo testInfo) {
        assertEquals("TEST 1", testInfo.getDisplayName());
        assertTrue(testInfo.getTags().contains("my-tag"));
    }
    @Test
    void test2() {
    }
}

• RepetitionInfoParameterResolver: if a method parameter in a @RepeatedTest, @BeforeEach, or
@AfterEach method is of type RepetitionInfo, the RepetitionInfoParameterResolver will supply an
instance of RepetitionInfo. RepetitionInfo can then be used to retrieve information about the
current repetition and the total number of repetitions for the corresponding @RepeatedTest.
Note, however, that RepetitionInfoParameterResolver is not registered outside the context of a
@RepeatedTest. See Repeated Test Examples.
• TestReporterParameterResolver: if a constructor or method parameter is of type TestReporter, the
TestReporterParameterResolver will supply an instance of TestReporter. The TestReporter can be
used to publish additional data about the current test run. The data can be consumed via the
reportingEntryPublished() method in a TestExecutionListener, allowing it to be viewed in IDEs
or included in reports.
In JUnit Jupiter you should use TestReporter where you used to print information to stdout or
stderr in JUnit 4. Using @RunWith(JUnitPlatform.class) will output all reported entries to stdout.
In addition, some IDEs print report entries to stdout or display them in the user interface for
test results.
class TestReporterDemo {
    @Test
    void reportSingleValue(TestReporter testReporter) {
        testReporter.publishEntry("a status message");
    }
    @Test
    void reportKeyValuePair(TestReporter testReporter) {
        testReporter.publishEntry("a key", "a value");
    }
    @Test
    void reportMultipleKeyValuePairs(TestReporter testReporter) {
        Map<String, String> values = new HashMap<>();
        values.put("user name", "dk38");
        values.put("award year", "1974");
        testReporter.publishEntry(values);
    }
}
 Other parameter resolvers must be explicitly enabled by registering appropriate
extensions via @ExtendWith.
Check out the RandomParametersExtension for an example of a custom ParameterResolver. While not
intended to be production-ready, it demonstrates the simplicity and expressiveness of both the
extension model and the parameter resolution process. MyRandomParametersTest demonstrates how
to inject random values into @Test methods.

@ExtendWith(RandomParametersExtension.class)
class MyRandomParametersTest {
    @Test
    void injectsInteger(@Random int i, @Random int j) {
        assertNotEquals(i, j);
    }
    @Test
    void injectsDouble(@Random double d) {
        assertEquals(0.0, d, 1.0);
    }
}
For real-world use cases, check out the source code for the MockitoExtension and the
SpringExtension.
2.13. Test Interfaces and Default Methods
JUnit Jupiter allows @Test, @RepeatedTest, @ParameterizedTest, @TestFactory, @TestTemplate,
@BeforeEach, and @AfterEach to be declared on interface default methods. @BeforeAll and @AfterAll
can either be declared on static methods in a test interface or on interface default methods if the
test interface or test class is annotated with @TestInstance(Lifecycle.PER_CLASS) (see Test Instance
Lifecycle). Here are some examples.

@TestInstance(Lifecycle.PER_CLASS)
interface TestLifecycleLogger {
    static final Logger logger = Logger.getLogger(TestLifecycleLogger.class.getName()
);
    @BeforeAll
    default void beforeAllTests() {
        logger.info("Before all tests");
    }
    @AfterAll
    default void afterAllTests() {
        logger.info("After all tests");
    }
    @BeforeEach
    default void beforeEachTest(TestInfo testInfo) {
        logger.info(() -> String.format("About to execute [%s]",
            testInfo.getDisplayName()));
    }
    @AfterEach
    default void afterEachTest(TestInfo testInfo) {
        logger.info(() -> String.format("Finished executing [%s]",
            testInfo.getDisplayName()));
    }
}
interface TestInterfaceDynamicTestsDemo {
    @TestFactory
    default Stream<DynamicTest> dynamicTestsForPalindromes() {
        return Stream.of("racecar", "radar", "mom", "dad")
            .map(text -> dynamicTest(text, () -> assertTrue(isPalindrome(text))));
    }
}
@ExtendWith and @Tag can be declared on a test interface so that classes that implement the interface
automatically inherit its tags and extensions. See Before and After Test Execution Callbacks  for the
source code of the TimingExtension.

@Tag("timed")
@ExtendWith(TimingExtension.class)
interface TimeExecutionLogger {
}
In your test class you can then implement these test interfaces to have them applied.
class TestInterfaceDemo implements TestLifecycleLogger,
        TimeExecutionLogger, TestInterfaceDynamicTestsDemo {
    @Test
    void isEqualValue() {
        assertEquals(1, "a".length(), "is always equal");
    }
}
Running the TestInterfaceDemo results in output similar to the following:
INFO  example.TestLifecycleLogger - Before all tests
INFO  example.TestLifecycleLogger - About to execute [dynamicTestsForPalindromes()]
INFO  example.TimingExtension - Method [dynamicTestsForPalindromes] took 19 ms.
INFO  example.TestLifecycleLogger - Finished executing [dynamicTestsForPalindromes()]
INFO  example.TestLifecycleLogger - About to execute [isEqualValue()]
INFO  example.TimingExtension - Method [isEqualValue] took 1 ms.
INFO  example.TestLifecycleLogger - Finished executing [isEqualValue()]
INFO  example.TestLifecycleLogger - After all tests
Another possible application of this feature is to write tests for interface contracts. For example,
you can write tests for how implementations of Object.equals or Comparable.compareTo should
behave as follows.
public interface Testable<T> {
    T createValue();
}

public interface EqualsContract<T> extends Testable<T> {
    T createNotEqualValue();
    @Test
    default void valueEqualsItself() {
        T value = createValue();
        assertEquals(value, value);
    }
    @Test
    default void valueDoesNotEqualNull() {
        T value = createValue();
        assertFalse(value.equals(null));
    }
    @Test
    default void valueDoesNotEqualDifferentValue() {
        T value = createValue();
        T differentValue = createNotEqualValue();
        assertNotEquals(value, differentValue);
        assertNotEquals(differentValue, value);
    }
}

public interface ComparableContract<T extends Comparable<T>> extends Testable<T> {
    T createSmallerValue();
    @Test
    default void returnsZeroWhenComparedToItself() {
        T value = createValue();
        assertEquals(0, value.compareTo(value));
    }
    @Test
    default void returnsPositiveNumberWhenComparedToSmallerValue() {
        T value = createValue();
        T smallerValue = createSmallerValue();
        assertTrue(value.compareTo(smallerValue) > 0);
    }
    @Test
    default void returnsNegativeNumberWhenComparedToLargerValue() {
        T value = createValue();
        T smallerValue = createSmallerValue();
        assertTrue(smallerValue.compareTo(value) < 0);
    }
}
In your test class you can then implement both contract interfaces thereby inheriting the
corresponding tests. Of course you’ll have to implement the abstract methods.
class StringTests implements ComparableContract<String>, EqualsContract<String> {
    @Override
    public String createValue() {
        return "banana";
    }
    @Override
    public String createSmallerValue() {
        return "apple"; // 'a' < 'b' in "banana"
    }
    @Override
    public String createNotEqualValue() {
        return "cherry";
    }
}

 The above tests are merely meant as examples and therefore not complete.
2.14. Repeated Tests
JUnit Jupiter provides the ability to repeat a test a specified number of times by annotating a
method with @RepeatedTest and specifying the total number of repetitions desired. Each invocation
of a repeated test behaves like the execution of a regular @Test method with full support for the
same lifecycle callbacks and extensions.
The following example demonstrates how to declare a test named repeatedTest() that will be
automatically repeated 10 times.
@RepeatedTest(10)
void repeatedTest() {
    // ...
}
In addition to specifying the number of repetitions, a custom display name can be configured for
each repetition via the name attribute of the @RepeatedTest annotation. Furthermore, the display
name can be a pattern composed of a combination of static text and dynamic placeholders. The
following placeholders are currently supported.
• {displayName}: display name of the @RepeatedTest method
• {currentRepetition}: the current repetition count
• {totalRepetitions}: the total number of repetitions
The default display name for a given repetition is generated based on the following pattern:
"repetition {currentRepetition} of {totalRepetitions}" . Thus, the display names for individual
repetitions of the previous repeatedTest() example would be: repetition 1 of 10, repetition 2 of
10, etc. If you would like the display name of the @RepeatedTest method included in the name of
each repetition, you can define your own custom pattern or use the predefined
RepeatedTest.LONG_DISPLAY_NAME pattern. The latter is equal to "{displayName} :: repetition
{currentRepetition} of {totalRepetitions}"  which results in display names for individual
repetitions like repeatedTest() :: repetition 1 of 10, repeatedTest() :: repetition 2 of 10, etc.
In order to retrieve information about the current repetition and the total number of repetitions
programmatically, a developer can choose to have an instance of RepetitionInfo injected into a
@RepeatedTest, @BeforeEach, or @AfterEach method.
2.14.1. Repeated Test Examples
The RepeatedTestsDemo class at the end of this section demonstrates several examples of repeated
tests.
The repeatedTest() method is identical to example from the previous section; whereas,
repeatedTestWithRepetitionInfo() demonstrates how to have an instance of RepetitionInfo injected
into a test to access the total number of repetitions for the current repeated test.

The next two methods demonstrate how to include a custom @DisplayName for the @RepeatedTest
method in the display name of each repetition. customDisplayName() combines a custom display
name with a custom pattern and then uses TestInfo to verify the format of the generated display
name. Repeat! is the {displayName} which comes from the @DisplayName declaration, and 1/1 comes
from {currentRepetition}/{totalRepetitions}. In contrast, customDisplayNameWithLongPattern() uses
the aforementioned predefined RepeatedTest.LONG_DISPLAY_NAME pattern.
repeatedTestInGerman() demonstrates the ability to translate display names of repeated tests into
foreign languages — in this case German, resulting in names for individual repetitions such as:
Wiederholung 1 von 5, Wiederholung 2 von 5, etc.
Since the beforeEach() method is annotated with @BeforeEach it will get executed before each
repetition of each repeated test. By having the TestInfo and RepetitionInfo injected into the
method, we see that it’s possible to obtain information about the currently executing repeated test.
Executing RepeatedTestsDemo with the INFO log level enabled results in the following output.
INFO: About to execute repetition 1 of 10 for repeatedTest
INFO: About to execute repetition 2 of 10 for repeatedTest
INFO: About to execute repetition 3 of 10 for repeatedTest
INFO: About to execute repetition 4 of 10 for repeatedTest
INFO: About to execute repetition 5 of 10 for repeatedTest
INFO: About to execute repetition 6 of 10 for repeatedTest
INFO: About to execute repetition 7 of 10 for repeatedTest
INFO: About to execute repetition 8 of 10 for repeatedTest
INFO: About to execute repetition 9 of 10 for repeatedTest
INFO: About to execute repetition 10 of 10 for repeatedTest
INFO: About to execute repetition 1 of 5 for repeatedTestWithRepetitionInfo
INFO: About to execute repetition 2 of 5 for repeatedTestWithRepetitionInfo
INFO: About to execute repetition 3 of 5 for repeatedTestWithRepetitionInfo
INFO: About to execute repetition 4 of 5 for repeatedTestWithRepetitionInfo
INFO: About to execute repetition 5 of 5 for repeatedTestWithRepetitionInfo
INFO: About to execute repetition 1 of 1 for customDisplayName
INFO: About to execute repetition 1 of 1 for customDisplayNameWithLongPattern
INFO: About to execute repetition 1 of 5 for repeatedTestInGerman
INFO: About to execute repetition 2 of 5 for repeatedTestInGerman
INFO: About to execute repetition 3 of 5 for repeatedTestInGerman
INFO: About to execute repetition 4 of 5 for repeatedTestInGerman
INFO: About to execute repetition 5 of 5 for repeatedTestInGerman
import static org.junit.jupiter.api.Assertions.assertEquals;
import java.util.logging.Logger;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.RepetitionInfo;
import org.junit.jupiter.api.TestInfo;

class RepeatedTestsDemo {
    private Logger logger = // ...
    @BeforeEach
    void beforeEach(TestInfo testInfo, RepetitionInfo repetitionInfo) {
        int currentRepetition = repetitionInfo.getCurrentRepetition();
        int totalRepetitions = repetitionInfo.getTotalRepetitions();
        String methodName = testInfo.getTestMethod().get().getName();
        logger.info(String.format("About to execute repetition %d of %d for %s", //
            currentRepetition, totalRepetitions, methodName));
    }
    @RepeatedTest(10)
    void repeatedTest() {
        // ...
    }
    @RepeatedTest(5)
    void repeatedTestWithRepetitionInfo(RepetitionInfo repetitionInfo) {
        assertEquals(5, repetitionInfo.getTotalRepetitions());
    }
    @RepeatedTest(value = 1, name = "{displayName}
{currentRepetition}/{totalRepetitions}")
    @DisplayName("Repeat!")
    void customDisplayName(TestInfo testInfo) {
        assertEquals("Repeat! 1/1", testInfo.getDisplayName());
    }
    @RepeatedTest(value = 1, name = RepeatedTest.LONG_DISPLAY_NAME)
    @DisplayName("Details...")
    void customDisplayNameWithLongPattern(TestInfo testInfo) {
        assertEquals("Details... :: repetition 1 of 1", testInfo.getDisplayName());
    }
    @RepeatedTest(value = 5, name = "Wiederholung {currentRepetition} von
{totalRepetitions}")
    void repeatedTestInGerman() {
        // ...
    }
}
When using the ConsoleLauncher with the unicode theme enabled, execution of RepeatedTestsDemo
results in the following output to the console.

├─ RepeatedTestsDemo ✔
│  ├─ repeatedTest() ✔
│  │  ├─ repetition 1 of 10 ✔
│  │  ├─ repetition 2 of 10 ✔
│  │  ├─ repetition 3 of 10 ✔
│  │  ├─ repetition 4 of 10 ✔
│  │  ├─ repetition 5 of 10 ✔
│  │  ├─ repetition 6 of 10 ✔
│  │  ├─ repetition 7 of 10 ✔
│  │  ├─ repetition 8 of 10 ✔
│  │  ├─ repetition 9 of 10 ✔
│  │  └─ repetition 10 of 10 ✔
│  ├─ repeatedTestWithRepetitionInfo(RepetitionInfo) ✔
│  │  ├─ repetition 1 of 5 ✔
│  │  ├─ repetition 2 of 5 ✔
│  │  ├─ repetition 3 of 5 ✔
│  │  ├─ repetition 4 of 5 ✔
│  │  └─ repetition 5 of 5 ✔
│  ├─ Repeat! ✔
│  │  └─ Repeat! 1/1 ✔
│  ├─ Details... ✔
│  │  └─ Details... :: repetition 1 of 1 ✔
│  └─ repeatedTestInGerman() ✔
│     ├─ Wiederholung 1 von 5 ✔
│     ├─ Wiederholung 2 von 5 ✔
│     ├─ Wiederholung 3 von 5 ✔
│     ├─ Wiederholung 4 von 5 ✔
│     └─ Wiederholung 5 von 5 ✔
2.15. Parameterized Tests
Parameterized tests make it possible to run a test multiple times with different arguments. They are
declared just like regular @Test methods but use the @ParameterizedTest annotation instead. In
addition, you must declare at least one source that will provide the arguments for each invocation
and then consume the arguments in the test method.
The following example demonstrates a parameterized test that uses the @ValueSource annotation to
specify a String array as the source of arguments.
@ParameterizedTest
@ValueSource(strings = { "racecar", "radar", "able was I ere I saw elba" })
void palindromes(String candidate) {
    assertTrue(StringUtils.isPalindrome(candidate));
}
When executing the above parameterized test method, each invocation will be reported separately.
For instance, the ConsoleLauncher will print output similar to the following.

palindromes(String) ✔
├─ [1] racecar ✔
├─ [2] radar ✔
└─ [3] able was I ere I saw elba ✔
 Parameterized tests are currently an experimental feature. Consult the table in
Experimental APIs for details.
2.15.1. Required Setup
In order to use parameterized tests you need to add a dependency on the junit-jupiter-params
artifact. Please refer to Dependency Metadata for details.
2.15.2. Consuming Arguments
Parameterized test methods typically consume arguments directly from the configured source (see
Sources of Arguments ) following a one-to-one correlation between argument source index and
method parameter index (see examples in @CsvSource). However, a parameterized test method
may also choose to aggregate arguments from the source into a single object passed to the method
(see Argument Aggregation ). Additional arguments may also be provided by a ParameterResolver
(e.g., to obtain an instance of TestInfo, TestReporter, etc.). Specifically, a parameterized test method
must declare formal parameters according to the following rules.
• Zero or more indexed arguments must be declared first.
• Zero or more aggregators must be declared next.
• Zero or more arguments supplied by a ParameterResolver must be declared last.
In this context, an indexed argument is an argument for a given index in the Arguments provided by
an ArgumentsProvider that is passed as an argument to the parameterized method at the same index
in the method’s formal parameter list. An aggregator is any parameter of type ArgumentsAccessor or
any parameter annotated with @AggregateWith.
2.15.3. Sources of Arguments
Out of the box, JUnit Jupiter provides quite a few source annotations. Each of the following
subsections provides a brief overview and an example for each of them. Please refer to the Javadoc
in the org.junit.jupiter.params.provider package for additional information.
@ValueSource
@ValueSource is one of the simplest possible sources. It lets you specify a single array of literal values
and can only be used for providing a single argument per parameterized test invocation.
The following types of literal values are supported by @ValueSource.
• short
• byte

• int
• long
• float
• double
• char
• boolean
• java.lang.String
• java.lang.Class
For example, the following @ParameterizedTest method will be invoked three times, with the values
1, 2, and 3 respectively.
@ParameterizedTest
@ValueSource(ints = { 1, 2, 3 })
void testWithValueSource(int argument) {
    assertTrue(argument > 0 && argument < 4);
}
Null and Empty Sources
In order to check corner cases and verify proper behavior of our software when it is supplied bad
input, it can be useful to have null and empty values supplied to our parameterized tests. The
following annotations serve as sources of null and empty values for parameterized tests that accept
a single argument.
• @NullSource: provides a single null argument to the annotated @ParameterizedTest method.
◦ @NullSource cannot be used for a parameter that has a primitive type.
• @EmptySource: provides a single empty argument to the annotated @ParameterizedTest method for
parameters of the following types: java.lang.String, java.util.List, java.util.Set,
java.util.Map, primitive arrays (e.g., int[], char[][], etc.), object arrays (e.g., String[],
Integer[][], etc.).
◦ Subtypes of the supported types are not supported.
• @NullAndEmptySource: a composed annotation that combines the functionality of @NullSource and
@EmptySource.
If you need to supply multiple varying types of blank strings to a parameterized test, you can
achieve that using @ValueSource — for example, @ValueSource(strings = {" ", "   ", "\t",
"\n"}).
You can also combine @NullSource, @EmptySource, and @ValueSource to test a wider range of null,
empty, and blank input. The following example demonstrates how to achieve this for strings.

@ParameterizedTest
@NullSource
@EmptySource
@ValueSource(strings = { " ", "   ", "\t", "\n" })
void nullEmptyAndBlankStrings(String text) {
    assertTrue(text == null || text.trim().isEmpty());
}
Making use of the composed @NullAndEmptySource annotation simplifies the above as follows.
@ParameterizedTest
@NullAndEmptySource
@ValueSource(strings = { " ", "   ", "\t", "\n" })
void nullEmptyAndBlankStrings(String text) {
    assertTrue(text == null || text.trim().isEmpty());
}

Both variants of the nullEmptyAndBlankStrings(String) parameterized test method
result in six invocations: 1 for null, 1 for the empty string, and 4 for the explicit
blank strings supplied via @ValueSource.
@EnumSource
@EnumSource provides a convenient way to use Enum constants. The annotation provides an optional
names parameter that lets you specify which constants shall be used. If omitted, all constants will be
used like in the following example.
@ParameterizedTest
@EnumSource(TimeUnit.class)
void testWithEnumSource(TimeUnit timeUnit) {
    assertNotNull(timeUnit);
}
@ParameterizedTest
@EnumSource(value = TimeUnit.class, names = { "DAYS", "HOURS" })
void testWithEnumSourceInclude(TimeUnit timeUnit) {
    assertTrue(EnumSet.of(TimeUnit.DAYS, TimeUnit.HOURS).contains(timeUnit));
}
The @EnumSource annotation also provides an optional mode parameter that enables fine-grained
control over which constants are passed to the test method. For example, you can exclude names
from the enum constant pool or specify regular expressions as in the following examples.

@ParameterizedTest
@EnumSource(value = TimeUnit.class, mode = EXCLUDE, names = { "DAYS", "HOURS" })
void testWithEnumSourceExclude(TimeUnit timeUnit) {
    assertFalse(EnumSet.of(TimeUnit.DAYS, TimeUnit.HOURS).contains(timeUnit));
    assertTrue(timeUnit.name().length() > 5);
}
@ParameterizedTest
@EnumSource(value = TimeUnit.class, mode = MATCH_ALL, names = "^(M|N).+SECONDS$")
void testWithEnumSourceRegex(TimeUnit timeUnit) {
    String name = timeUnit.name();
    assertTrue(name.startsWith("M") || name.startsWith("N"));
    assertTrue(name.endsWith("SECONDS"));
}
@MethodSource
@MethodSource allows you to refer to one or more factory methods of the test class or external
classes.
Factory methods within the test class must be static unless the test class is annotated with
@TestInstance(Lifecycle.PER_CLASS); whereas, factory methods in external classes must always be
static. In addition, such factory methods must not accept any arguments.
Each factory method must generate a stream of arguments, and each set of arguments within the
stream will be provided as the physical arguments for individual invocations of the annotated
@ParameterizedTest method. Generally speaking this translates to a Stream of Arguments (i.e.,
Stream<Arguments>); however, the actual concrete return type can take on many forms. In this
context, a "stream" is anything that JUnit can reliably convert into a Stream, such as Stream,
DoubleStream, LongStream, IntStream, Collection, Iterator, Iterable, an array of objects, or an array of
primitives. The "arguments" within the stream can be supplied as an instance of Arguments, an array
of objects (e.g., Object[]), or a single value if the parameterized test method accepts a single
argument.
If you only need a single parameter, you can return a Stream of instances of the parameter type as
demonstrated in the following example.
@ParameterizedTest
@MethodSource("stringProvider")
void testWithExplicitLocalMethodSource(String argument) {
    assertNotNull(argument);
}
static Stream<String> stringProvider() {
    return Stream.of("apple", "banana");
}

If you do not explicitly provide a factory method name via @MethodSource, JUnit Jupiter will search
for a factory method that has the same name as the current @ParameterizedTest method by
convention. This is demonstrated in the following example.
@ParameterizedTest
@MethodSource
void testWithDefaultLocalMethodSource(String argument) {
    assertNotNull(argument);
}
static Stream<String> testWithDefaultLocalMethodSource() {
    return Stream.of("apple", "banana");
}
Streams for primitive types ( DoubleStream, IntStream, and LongStream) are also supported as
demonstrated by the following example.
@ParameterizedTest
@MethodSource("range")
void testWithRangeMethodSource(int argument) {
    assertNotEquals(9, argument);
}
static IntStream range() {
    return IntStream.range(0, 20).skip(10);
}
If a parameterized test method declares multiple parameters, you need to return a collection,
stream, or array of Arguments instances or object arrays as shown below (see the Javadoc for
@MethodSource for further details on supported return types). Note that arguments(Object…) is a
static factory method defined in the Arguments interface. In addition, Arguments.of(Object…) may be
used as an alternative to arguments(Object…).
@ParameterizedTest
@MethodSource("stringIntAndListProvider")
void testWithMultiArgMethodSource(String str, int num, List<String> list) {
    assertEquals(5, str.length());
    assertTrue(num >=1 && num <=2);
    assertEquals(2, list.size());
}
static Stream<Arguments> stringIntAndListProvider() {
    return Stream.of(
        arguments("apple", 1, Arrays.asList("a", "b")),
        arguments("lemon", 2, Arrays.asList("x", "y"))
    );
}

An external, static factory method can be referenced by providing its fully qualified method name 
as demonstrated in the following example.
package example;
import java.util.stream.Stream;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
class ExternalMethodSourceDemo {
    @ParameterizedTest
    @MethodSource("example.StringsProviders#tinyStrings")
    void testWithExternalMethodSource(String tinyString) {
        // test with tiny string
    }
}
class StringsProviders {
    static Stream<String> tinyStrings() {
        return Stream.of(".", "oo", "OOO");
    }
}
@CsvSource
@CsvSource allows you to express argument lists as comma-separated values (i.e., String literals).
@ParameterizedTest
@CsvSource({
    "apple,         1",
    "banana,        2",
    "'lemon, lime', 0xF1"
})
void testWithCsvSource(String fruit, int rank) {
    assertNotNull(fruit);
    assertNotEquals(0, rank);
}
@CsvSource uses a single quote ' as its quote character. See the 'lemon, lime' value in the example
above and in the table below. An empty, quoted value '' results in an empty String unless the
emptyValue attribute is set; whereas, an entirely empty value is interpreted as a null reference. An
ArgumentConversionException is raised if the target type of a null reference is a primitive type.

Example Input Resulting Argument List
@CsvSource({ "apple, banana" }) "apple", "banana"
@CsvSource({ "apple, 'lemon, lime'" }) "apple", "lemon, lime"
@CsvSource({ "apple, ''" }) "apple", ""
@CsvSource({ "apple, " }) "apple", null
@CsvFileSource
@CsvFileSource lets you use CSV files from the classpath. Each line from a CSV file results in one
invocation of the parameterized test.
@ParameterizedTest
@CsvFileSource(resources = "/two-column.csv", numLinesToSkip = 1)
void testWithCsvFileSource(String country, int reference) {
    assertNotNull(country);
    assertNotEquals(0, reference);
}
two-column.csv
Country, reference
Sweden, 1
Poland, 2
"United States of America", 3

In contrast to the syntax used in @CsvSource, @CsvFileSource uses a double quote "
as the quote character. See the "United States of America"  value in the example
above. An empty, quoted value "" results in an empty String unless the emptyValue
attribute is set; whereas, an entirely empty value is interpreted as a null reference.
An ArgumentConversionException is raised if the target type of a null reference is a
primitive type.
@ArgumentsSource
@ArgumentsSource can be used to specify a custom, reusable ArgumentsProvider. Note that an
implementation of ArgumentsProvider must be declared as either a top-level class or as a static
nested class.
@ParameterizedTest
@ArgumentsSource(MyArgumentsProvider.class)
void testWithArgumentsSource(String argument) {
    assertNotNull(argument);
}

public class MyArgumentsProvider implements ArgumentsProvider {
    @Override
    public Stream<? extends Arguments> provideArguments(ExtensionContext context) {
        return Stream.of("apple", "banana").map(Arguments::of);
    }
}
2.15.4. Argument Conversion
Widening Conversion
JUnit Jupiter supports Widening Primitive Conversion  for arguments supplied to a
@ParameterizedTest. For example, a parameterized test annotated with @ValueSource(ints = { 1, 2,
3 }) can be declared to accept not only an argument of type int but also an argument of type long,
float, or double.
Implicit Conversion
To support use cases like @CsvSource, JUnit Jupiter provides a number of built-in implicit type
converters. The conversion process depends on the declared type of each method parameter.
For example, if a @ParameterizedTest declares a parameter of type TimeUnit and the actual type
supplied by the declared source is a String, the string will be automatically converted into the
corresponding TimeUnit enum constant.
@ParameterizedTest
@ValueSource(strings = "SECONDS")
void testWithImplicitArgumentConversion(TimeUnit argument) {
    assertNotNull(argument.name());
}
String instances are implicitly converted to the following target types.
 Decimal, hexadecimal, and octal String literals will be converted to their integral
types: byte, short, int, long, and their boxed counterparts.
Target
Type
Example
boolean/
Boolean
"true" → true
byte/Byt
e
"15", "0xF", or "017" → (byte) 15
char/Cha
racter
"o" → 'o'

Target
Type
Example
java.tim
e.LocalD
ate
"2017-03-14" → LocalDate.of(2017, 3, 14)
java.tim
e.LocalT
ime
"12:34:56.789" → LocalTime.of(12, 34, 56, 789_000_000)
java.tim
e.MonthD
ay
"--03-14" → MonthDay.of(3, 14)
java.tim
e.Offset
DateTime
"2017-03-14T12:34:56.789Z" → OffsetDateTime.of(2017, 3, 14, 12, 34, 56, 789_000_000,
ZoneOffset.UTC)
java.tim
e.Offset
Time
"12:34:56.789Z" → OffsetTime.of(12, 34, 56, 789_000_000, ZoneOffset.UTC)
java.tim
e.Period
"P2M6D" → Period.of(0, 2, 6)
java.tim
e.YearMo
nth
"2017-03" → YearMonth.of(2017, 3)
java.tim
e.Year
"2017" → Year.of(2017)
java.tim
e.ZonedD
ateTime
"2017-03-14T12:34:56.789Z" → ZonedDateTime.of(2017, 3, 14, 12, 34, 56, 789_000_000,
ZoneOffset.UTC)
java.tim
e.ZoneId
"Europe/Berlin" → ZoneId.of("Europe/Berlin")
java.tim
e.ZoneOf
fset
"+02:30" → ZoneOffset.ofHoursMinutes(2, 30)
java.uti
l.Curren
cy
"JPY" → Currency.getInstance("JPY")
java.uti
l.Locale
"en" → new Locale("en")
java.uti
l.UUID
"d043e930-7b3b-48e3-bdbe-5a3ccfb833db" → UUID.fromString("d043e930-7b3b-48e3-bdbe-
5a3ccfb833db")
Fallback String-to-Object Conversion
In addition to implicit conversion from strings to the target types listed in the above table, JUnit
Jupiter also provides a fallback mechanism for automatic conversion from a String to a given target
type if the target type declares exactly one suitable factory method  or a factory constructor  as
defined below.
• factory method: a non-private, static method declared in the target type that accepts a single
String argument and returns an instance of the target type. The name of the method can be

arbitrary and need not follow any particular convention.
• factory constructor : a non-private constructor in the target type that accepts a single String
argument. Note that the target type must be declared as either a top-level class or as a static
nested class.

If multiple factory methods  are discovered, they will be ignored. If a factory
method and a factory constructor are discovered, the factory method will be used
instead of the constructor.
For example, in the following @ParameterizedTest method, the Book argument will be created by
invoking the Book.fromTitle(String) factory method and passing "42 Cats" as the title of the book.
@ParameterizedTest
@ValueSource(strings = "42 Cats")
void testWithImplicitFallbackArgumentConversion(Book book) {
    assertEquals("42 Cats", book.getTitle());
}
public class Book {
    private final String title;
    private Book(String title) {
        this.title = title;
    }
    public static Book fromTitle(String title) {
        return new Book(title);
    }
    public String getTitle() {
        return this.title;
    }
}
Explicit Conversion
Instead of relying on implicit argument conversion you may explicitly specify an ArgumentConverter
to use for a certain parameter using the @ConvertWith annotation like in the following example. Note
that an implementation of ArgumentConverter must be declared as either a top-level class or as a
static nested class.

@ParameterizedTest
@EnumSource(TimeUnit.class)
void testWithExplicitArgumentConversion(
        @ConvertWith(ToStringArgumentConverter.class) String argument) {
    assertNotNull(TimeUnit.valueOf(argument));
}
public class ToStringArgumentConverter extends SimpleArgumentConverter {
    @Override
    protected Object convert(Object source, Class<?> targetType) {
        assertEquals(String.class, targetType, "Can only convert to String");
        return String.valueOf(source);
    }
}
Explicit argument converters are meant to be implemented by test and extension authors. Thus,
junit-jupiter-params only provides a single explicit argument converter that may also serve as a
reference implementation: JavaTimeArgumentConverter. It is used via the composed annotation
JavaTimeConversionPattern.
@ParameterizedTest
@ValueSource(strings = { "01.01.2017", "31.12.2017" })
void testWithExplicitJavaTimeConverter(
        @JavaTimeConversionPattern("dd.MM.yyyy") LocalDate argument) {
    assertEquals(2017, argument.getYear());
}
2.15.5. Argument Aggregation
By default, each argument provided to a @ParameterizedTest method corresponds to a single method
parameter. Consequently, argument sources which are expected to supply a large number of
arguments can lead to large method signatures.
In such cases, an ArgumentsAccessor can be used instead of multiple parameters. Using this API, you
can access the provided arguments through a single argument passed to your test method. In
addition, type conversion is supported as discussed in Implicit Conversion.

@ParameterizedTest
@CsvSource({
    "Jane, Doe, F, 1990-05-20",
    "John, Doe, M, 1990-10-22"
})
void testWithArgumentsAccessor(ArgumentsAccessor arguments) {
    Person person = new Person(arguments.getString(0),
                               arguments.getString(1),
                               arguments.get(2, Gender.class),
                               arguments.get(3, LocalDate.class));
    if (person.getFirstName().equals("Jane")) {
        assertEquals(Gender.F, person.getGender());
    }
    else {
        assertEquals(Gender.M, person.getGender());
    }
    assertEquals("Doe", person.getLastName());
    assertEquals(1990, person.getDateOfBirth().getYear());
}
An instance of ArgumentsAccessor is automatically injected into any parameter of type
ArgumentsAccessor.
Custom Aggregators
Apart from direct access to a @ParameterizedTest method’s arguments using an ArgumentsAccessor,
JUnit Jupiter also supports the usage of custom, reusable aggregators.
To use a custom aggregator, implement the ArgumentsAggregator interface and register it via the
@AggregateWith annotation on a compatible parameter in the @ParameterizedTest method. The result
of the aggregation will then be provided as an argument for the corresponding parameter when the
parameterized test is invoked. Note that an implementation of ArgumentsAggregator must be
declared as either a top-level class or as a static nested class.
@ParameterizedTest
@CsvSource({
    "Jane, Doe, F, 1990-05-20",
    "John, Doe, M, 1990-10-22"
})
void testWithArgumentsAggregator(@AggregateWith(PersonAggregator.class) Person person)
{
    // perform assertions against person
}

public class PersonAggregator implements ArgumentsAggregator {
    @Override
    public Person aggregateArguments(ArgumentsAccessor arguments, ParameterContext
context) {
        return new Person(arguments.getString(0),
                          arguments.getString(1),
                          arguments.get(2, Gender.class),
                          arguments.get(3, LocalDate.class));
    }
}
If you find yourself repeatedly declaring @AggregateWith(MyTypeAggregator.class) for multiple
parameterized test methods across your codebase, you may wish to create a custom composed
annotation such as @CsvToMyType that is meta-annotated with
@AggregateWith(MyTypeAggregator.class). The following example demonstrates this in action with a
custom @CsvToPerson annotation.
@ParameterizedTest
@CsvSource({
    "Jane, Doe, F, 1990-05-20",
    "John, Doe, M, 1990-10-22"
})
void testWithCustomAggregatorAnnotation(@CsvToPerson Person person) {
    // perform assertions against person
}
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
@AggregateWith(PersonAggregator.class)
public @interface CsvToPerson {
}
2.15.6. Customizing Display Names
By default, the display name of a parameterized test invocation contains the invocation index and
the String representation of all arguments for that specific invocation. However, you can customize
invocation display names via the name attribute of the @ParameterizedTest annotation like in the
following example.
@DisplayName("Display name of container")
@ParameterizedTest(name = "{index} ==> fruit=''{0}'', rank={1}")
@CsvSource({ "apple, 1", "banana, 2", "'lemon, lime', 3" })
void testWithCustomDisplayNames(String fruit, int rank) {
}

When executing the above method using the ConsoleLauncher you will see output similar to the
following.
Display name of container ✔
├─ 1 ==> fruit='apple', rank=1 ✔
├─ 2 ==> fruit='banana', rank=2 ✔
└─ 3 ==> fruit='lemon, lime', rank=3 ✔
The following placeholders are supported within custom display names.
Placeholder Description
{index} the current invocation index (1-based)
{arguments} the complete, comma-separated arguments list
{0}, {1}, … an individual argument
2.15.7. Lifecycle and Interoperability
Each invocation of a parameterized test has the same lifecycle as a regular @Test method. For
example, @BeforeEach methods will be executed before each invocation. Similar to Dynamic Tests,
invocations will appear one by one in the test tree of an IDE. You may at will mix regular @Test
methods and @ParameterizedTest methods within the same test class.
You may use ParameterResolver extensions with @ParameterizedTest methods. However, method
parameters that are resolved by argument sources need to come first in the argument list. Since a
test class may contain regular tests as well as parameterized tests with different parameter lists,
values from argument sources are not resolved for lifecycle methods (e.g. @BeforeEach) and test
class constructors.
@BeforeEach
void beforeEach(TestInfo testInfo) {
    // ...
}
@ParameterizedTest
@ValueSource(strings = "apple")
void testWithRegularParameterResolver(String argument, TestReporter testReporter) {
    testReporter.publishEntry("argument", argument);
}
@AfterEach
void afterEach(TestInfo testInfo) {
    // ...
}

2.16. Test Templates
A @TestTemplate method is not a regular test case but rather a template for test cases. As such, it is
designed to be invoked multiple times depending on the number of invocation contexts returned by
the registered providers. Thus, it must be used in conjunction with a registered
TestTemplateInvocationContextProvider extension. Each invocation of a test template method
behaves like the execution of a regular @Test method with full support for the same lifecycle
callbacks and extensions. Please refer to Providing Invocation Contexts for Test Templates for usage
examples.
 Repeated Tests  and Parameterized Tests  are built-in specializations of test
templates.
2.17. Dynamic Tests
The standard @Test annotation in JUnit Jupiter described in Annotations is very similar to the @Test
annotation in JUnit 4. Both describe methods that implement test cases. These test cases are static in
the sense that they are fully specified at compile time, and their behavior cannot be changed by
anything happening at runtime. Assumptions provide a basic form of dynamic behavior but are
intentionally rather limited in their expressiveness.
In addition to these standard tests a completely new kind of test programming model has been
introduced in JUnit Jupiter. This new kind of test is a dynamic test which is generated at runtime by
a factory method that is annotated with @TestFactory.
In contrast to @Test methods, a @TestFactory method is not itself a test case but rather a factory for
test cases. Thus, a dynamic test is the product of a factory. Technically speaking, a @TestFactory
method must return a single DynamicNode or a Stream, Collection, Iterable, Iterator, or array of
DynamicNode instances. Instantiable subclasses of DynamicNode are DynamicContainer and DynamicTest.
DynamicContainer instances are composed of a display name  and a list of dynamic child nodes,
enabling the creation of arbitrarily nested hierarchies of dynamic nodes. DynamicTest instances will
be executed lazily, enabling dynamic and even non-deterministic generation of test cases.
Any Stream returned by a @TestFactory will be properly closed by calling stream.close(), making it
safe to use a resource such as Files.lines().
As with @Test methods, @TestFactory methods must not be private or static and may optionally
declare parameters to be resolved by ParameterResolvers.
A DynamicTest is a test case generated at runtime. It is composed of a display name  and an
Executable. Executable is a @FunctionalInterface which means that the implementations of dynamic
tests can be provided as lambda expressions or method references.


Dynamic Test Lifecycle
The execution lifecycle of a dynamic test is quite different than it is for a standard
@Test case. Specifically, there are no lifecycle callbacks for individual dynamic
tests. This means that @BeforeEach and @AfterEach methods and their
corresponding extension callbacks are executed for the @TestFactory method but
not for each dynamic test. In other words, if you access fields from the test instance
within a lambda expression for a dynamic test, those fields will not be reset by
callback methods or extensions between the execution of individual dynamic tests
generated by the same @TestFactory method.
As of JUnit Jupiter 5.5.0, dynamic tests must always be created by factory methods; however, this
might be complemented by a registration facility in a later release.
2.17.1. Dynamic Test Examples
The following DynamicTestsDemo class demonstrates several examples of test factories and dynamic
tests.
The first method returns an invalid return type. Since an invalid return type cannot be detected at
compile time, a JUnitException is thrown when it is detected at runtime.
The next five methods are very simple examples that demonstrate the generation of a Collection,
Iterable, Iterator, or Stream of DynamicTest instances. Most of these examples do not really exhibit
dynamic behavior but merely demonstrate the supported return types in principle. However,
dynamicTestsFromStream() and dynamicTestsFromIntStream() demonstrate how easy it is to generate
dynamic tests for a given set of strings or a range of input numbers.
The next method is truly dynamic in nature. generateRandomNumberOfTests() implements an Iterator
that generates random numbers, a display name generator, and a test executor and then provides
all three to DynamicTest.stream(). Although the non-deterministic behavior of
generateRandomNumberOfTests() is of course in conflict with test repeatability and should thus be
used with care, it serves to demonstrate the expressiveness and power of dynamic tests.
The last method generates a nested hierarchy of dynamic tests utilizing DynamicContainer.
import static example.util.StringUtils.isPalindrome;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.DynamicContainer.dynamicContainer;
import static org.junit.jupiter.api.DynamicTest.dynamicTest;
import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.function.Function;

import java.util.stream.IntStream;
import java.util.stream.Stream;
import example.util.Calculator;
import org.junit.jupiter.api.DynamicNode;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.function.ThrowingConsumer;
class DynamicTestsDemo {
    private final Calculator calculator = new Calculator();
    // This will result in a JUnitException!
    @TestFactory
    List<String> dynamicTestsWithInvalidReturnType() {
        return Arrays.asList("Hello");
    }
    @TestFactory
    Collection<DynamicTest> dynamicTestsFromCollection() {
        return Arrays.asList(
            dynamicTest("1st dynamic test", () -> assertTrue(isPalindrome("madam"))),
            dynamicTest("2nd dynamic test", () -> assertEquals(4, calculator.multiply
(2, 2)))
        );
    }
    @TestFactory
    Iterable<DynamicTest> dynamicTestsFromIterable() {
        return Arrays.asList(
            dynamicTest("3rd dynamic test", () -> assertTrue(isPalindrome("madam"))),
            dynamicTest("4th dynamic test", () -> assertEquals(4, calculator.multiply
(2, 2)))
        );
    }
    @TestFactory
    Iterator<DynamicTest> dynamicTestsFromIterator() {
        return Arrays.asList(
            dynamicTest("5th dynamic test", () -> assertTrue(isPalindrome("madam"))),
            dynamicTest("6th dynamic test", () -> assertEquals(4, calculator.multiply
(2, 2)))
        ).iterator();
    }
    @TestFactory
    DynamicTest[] dynamicTestsFromArray() {
        return new DynamicTest[] {

dynamicTest("7th dynamic test", () -> assertTrue(isPalindrome("madam"))),
            dynamicTest("8th dynamic test", () -> assertEquals(4, calculator.multiply
(2, 2)))
        };
    }
    @TestFactory
    Stream<DynamicTest> dynamicTestsFromStream() {
        return Stream.of("racecar", "radar", "mom", "dad")
            .map(text -> dynamicTest(text, () -> assertTrue(isPalindrome(text))));
    }
    @TestFactory
    Stream<DynamicTest> dynamicTestsFromIntStream() {
        // Generates tests for the first 10 even integers.
        return IntStream.iterate(0, n -> n + 2).limit(10)
            .mapToObj(n -> dynamicTest("test" + n, () -> assertTrue(n % 2 == 0)));
    }
    @TestFactory
    Stream<DynamicTest> generateRandomNumberOfTests() {
        // Generates random positive integers between 0 and 100 until
        // a number evenly divisible by 7 is encountered.
        Iterator<Integer> inputGenerator = new Iterator<Integer>() {
            Random random = new Random();
            int current;
            @Override
            public boolean hasNext() {
                current = random.nextInt(100);
                return current % 7 != 0;
            }
            @Override
            public Integer next() {
                return current;
            }
        };
        // Generates display names like: input:5, input:37, input:85, etc.
        Function<Integer, String> displayNameGenerator = (input) -> "input:" + input;
        // Executes tests based on the current input value.
        ThrowingConsumer<Integer> testExecutor = (input) -> assertTrue(input % 7 != 0
);
        // Returns a stream of dynamic tests.
        return DynamicTest.stream(inputGenerator, displayNameGenerator, testExecutor);
    }

@TestFactory
    Stream<DynamicNode> dynamicTestsWithContainers() {
        return Stream.of("A", "B", "C")
            .map(input -> dynamicContainer("Container " + input, Stream.of(
                dynamicTest("not null", () -> assertNotNull(input)),
                dynamicContainer("properties", Stream.of(
                    dynamicTest("length > 0", () -> assertTrue(input.length() > 0)),
                    dynamicTest("not empty", () -> assertFalse(input.isEmpty()))
                ))
            )));
    }
    @TestFactory
    DynamicNode dynamicNodeSingleTest() {
        return dynamicTest("'pop' is a palindrome", () -> assertTrue(isPalindrome("
pop")));
    }
    @TestFactory
    DynamicNode dynamicNodeSingleContainer() {
        return dynamicContainer("palindromes",
            Stream.of("racecar", "radar", "mom", "dad")
                .map(text -> dynamicTest(text, () -> assertTrue(isPalindrome(text)))
        ));
    }
}
2.17.2. URI Test Sources for Dynamic Tests
The JUnit Platform provides TestSource, a representation of the source of a test or container used to
navigate to its location by IDEs and build tools.
The TestSource for a dynamic test or dynamic container can be constructed from a java.net.URI
which can be supplied via the DynamicTest.dynamicTest(String, URI, Executable)  or
DynamicContainer.dynamicContainer(String, URI, Stream) factory method, respectively. The URI will
be converted to one of the following TestSource implementations.
ClasspathResourceSource
If the URI contains the classpath scheme — for example,
classpath:/test/foo.xml?line=20,column=2.
DirectorySource
If the URI represents a directory present in the file system.
FileSource
If the URI represents a file present in the file system.

MethodSource
If the URI contains the method scheme and the fully qualified method name (FQMN) — for
example, method:org.junit.Foo#bar(java.lang.String, java.lang.String[]). Please refer to the
Javadoc for DiscoverySelectors.selectMethod(String) for the supported formats for a FQMN.
UriSource
If none of the above TestSource implementations are applicable.
2.18. Timeouts

Declarative timeouts are an experimental feature
You’re invited to give it a try and provide feedback to the JUnit team so they can
improve and eventually promote this feature.
The @Timeout annotation allows one to declare that a test, test factory, test template, or lifecycle
method should fail if its execution time exceeds a given duration. The time unit for the duration
defaults to seconds but is configurable.
The following example shows how @Timeout is applied to lifecycle and test methods.
class TimeoutDemo {
    @BeforeEach
    @Timeout(5)
    void setUp() {
        // fails if execution time exceeds 5 seconds
    }
    @Test
    @Timeout(value = 100, unit = TimeUnit.MILLISECONDS)
    void failsIfExecutionTimeExceeds100Milliseconds() {
        // fails if execution time exceeds 100 milliseconds
    }
}
Contrary to the assertTimeoutPreemptively() assertion, the execution of the annotated method
proceeds in the main thread of the test. If the timeout is exceeded, the main thread is interrupted
from another thread. This is done to ensure interoperability with frameworks such as Spring that
make use of mechanisms that are sensitive to the currently running thread — for example,
ThreadLocal transaction management.
To apply the same timeout to all test methods within a test class and all of its @Nested classes, you
can declare the @Timeout annotation at the class level. It will then be applied to all test, test factory,
and test template methods within that class and its @Nested classes unless overridden by a @Timeout
annotation on a specific method or @Nested class. Please note that @Timeout annotations declared at
the class level are not applied to lifecycle methods.

Declaring @Timeout on a @TestFactory method checks that the factory method returns within the
specified duration but does verify the execution time of each individual DynamicTest generated by
the factory. Please use assertTimeout() or assertTimeoutPreemptively() for that purpose.
If @Timeout is present on a @TestTemplate method — for example, a @RepeatedTest or
@ParameterizedTest — each invocation will have the given timeout applied to it.
The following configuration parameters can be used to specify global timeouts for all methods of a
certain category unless they or an enclosing test class is annotated with @Timeout:
junit.jupiter.execution.timeout.default
Default timeout for all testable and lifecycle methods
junit.jupiter.execution.timeout.testable.method.default
Default timeout for all testable methods
junit.jupiter.execution.timeout.test.method.default
Default timeout for @Test methods
junit.jupiter.execution.timeout.testtemplate.method.default
Default timeout for @TestTemplate methods
junit.jupiter.execution.timeout.testfactory.method.default
Default timeout for @TestFactory methods
junit.jupiter.execution.timeout.lifecycle.method.default
Default timeout for all lifecycle methods
junit.jupiter.execution.timeout.beforeall.method.default
Default timeout for @BeforeAll methods
junit.jupiter.execution.timeout.beforeeach.method.default
Default timeout for @BeforeEach methods
junit.jupiter.execution.timeout.aftereach.method.default
Default timeout for @AfterEach methods
junit.jupiter.execution.timeout.afterall.method.default
Default timeout for @AfterAll methods
More specific configuration parameters override less specific ones. For example,
junit.jupiter.execution.timeout.test.method.default overrides
junit.jupiter.execution.timeout.testable.method.default which overrides
junit.jupiter.execution.timeout.default.
The values of such configuration parameters must be in the following, case-insensitive format:
<number> [ns| μs|ms|s|m|h|d]. The space between the number and the unit may be omitted.
Specifying no unit is equivalent to using seconds.
Table 1. Example timeout configuration parameter values

Parameter value Equivalent annotation
42 @Timeout(42)
42 ns @Timeout(value = 42, unit = NANOSECONDS)
42 μs @Timeout(value = 42, unit = MICROSECONDS)
42 ms @Timeout(value = 42, unit = MILLISECONDS)
42 s @Timeout(value = 42, unit = SECONDS)
42 m @Timeout(value = 42, unit = MINUTES)
42 h @Timeout(value = 42, unit = HOURS)
42 d @Timeout(value = 42, unit = DAYS)
2.18.1. Using @Timeout for Polling Tests
When dealing with asynchronous code, it is common to write tests that poll while waiting for
something to happen before performing any assertions. In some cases you can rewrite the logic to
use a CountDownLatch or another synchronization mechanism, but sometimes that is not possible —
for example, if the subject under test sends a message to a channel in an external message broker
and assertions cannot be performed until the message has been successfully sent through the
channel. Asynchronous tests like these require some form of timeout to ensure they don’t hang the
test suite by executing indefinitely, as would be the case if an asynchronous message never gets
successfully delivered.
By configuring a timeout for an asynchronous test that polls, you can ensure that the test does not
execute indefinitely. The following example demonstrates how to achieve this with JUnit Jupiter’s
@Timeout annotation. This technique can be used to implement "poll until" logic very easily.
@Test
@Timeout(5) // Poll at most 5 seconds
void pollUntil() throws InterruptedException {
    while (asynchronousResultNotAvailable()) {
        Thread.sleep(250); // custom poll interval
    }
    // Obtain the asynchronous result and perform assertions
}
 If you need more control over polling intervals and greater flexibility with
asynchronous tests, consider using a dedicated library such as Awaitility.
2.19. Parallel Execution

Parallel test execution is an experimental feature
You’re invited to give it a try and provide feedback to the JUnit team so they can
improve and eventually promote this feature.
By default, JUnit Jupiter tests are run sequentially in a single thread. Running tests in parallel — for

example, to speed up execution — is available as an opt-in feature since version 5.3. To enable
parallel execution, set the junit.jupiter.execution.parallel.enabled configuration parameter to
true — for example, in junit-platform.properties (see Configuration Parameters for other options).
Please note that enabling this property is only the first step required to execute tests in parallel. If
enabled, test classes and methods will still be executed sequentially by default. Whether or not a
node in the test tree is executed concurrently is controlled by its execution mode. The following two
modes are available.
SAME_THREAD
Force execution in the same thread used by the parent. For example, when used on a test
method, the test method will be executed in the same thread as any @BeforeAll or @AfterAll
methods of the containing test class.
CONCURRENT
Execute concurrently unless a resource lock forces execution in the same thread.
By default, nodes in the test tree use the SAME_THREAD execution mode. You can change the default by
setting the junit.jupiter.execution.parallel.mode.default configuration parameter. Alternatively,
you can use the @Execution annotation to change the execution mode for the annotated element and
its subelements (if any) which allows you to activate parallel execution for individual test classes,
one by one.
Configuration parameters to execute all tests in parallel
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.mode.default = concurrent
The default execution mode is applied to all nodes of the test tree with a few notable exceptions,
namely test classes that use the Lifecycle.PER_CLASS mode or a MethodOrderer (except for Random). In
the former case, test authors have to ensure that the test class is thread-safe; in the latter,
concurrent execution might conflict with the configured execution order. Thus, in both cases, test
methods in such test classes are only executed concurrently if the @Execution(CONCURRENT)
annotation is present on the test class or method.
All nodes of the test tree that are configured with the CONCURRENT execution mode will be executed
fully in parallel according to the provided configuration while observing the declarative
synchronization mechanism. Please note that Capturing Standard Output/Error needs to be enabled
separately.
In addition, you can configure the default execution mode for top-level classes by setting the
junit.jupiter.execution.parallel.mode.classes.default configuration parameter. By combining
both configuration parameters, you can configure classes to run in parallel but their methods in the
same thread:

Configuration parameters to execute top-level classes in parallel but methods in same thread
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.mode.default = same_thread
junit.jupiter.execution.parallel.mode.classes.default = concurrent
The opposite combination will run all methods within one class in parallel, but top-level classes will
run sequentially:
Configuration parameters to execute top-level classes in sequentially but their methods in parallel
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.mode.default = concurrent
junit.jupiter.execution.parallel.mode.classes.default = same_thread
The following diagram illustrates how the execution of two top-level test classes A and B with two
test methods per class behaves for all four combinations of
junit.jupiter.execution.parallel.mode.default and
junit.jupiter.execution.parallel.mode.classes.default (see labels in first column).

A.test1()
A.test2()
B.test1()
B.test2()
A.test1()
A.test2()
B.test1()
B.test2()
A.test1()
A.test2()
B.test1()
B.test2()
A.test1()
A.test2()
B.test1()
B.test2()
(same_thread, same_thread)
(same_thread, concurrent)
(concurrent, same_thread)
(concurrent, concurrent)
Default execution mode configuration combinations

If the junit.jupiter.execution.parallel.mode.classes.default configuration parameter is not
explicitly set, the value for junit.jupiter.execution.parallel.mode.default will be used instead.
2.19.1. Configuration
Properties such as the desired parallelism and the maximum pool size can be configured using a
ParallelExecutionConfigurationStrategy. The JUnit Platform provides two implementations out of
the box: dynamic and fixed. Alternatively, you may implement a custom strategy.
To select a strategy, set the junit.jupiter.execution.parallel.config.strategy configuration
parameter to one of the following options.
dynamic
Computes the desired parallelism based on the number of available processors/cores multiplied
by the junit.jupiter.execution.parallel.config.dynamic.factor configuration parameter
(defaults to 1).
fixed
Uses the mandatory junit.jupiter.execution.parallel.config.fixed.parallelism configuration
parameter as the desired parallelism.
custom
Allows you to specify a custom ParallelExecutionConfigurationStrategy implementation via the
mandatory junit.jupiter.execution.parallel.config.custom.class configuration parameter to
determine the desired configuration.
If no configuration strategy is set, JUnit Jupiter uses the dynamic configuration strategy with a factor
of 1. Consequently, the desired parallelism will be equal to the number of available
processors/cores.

Parallelism does not imply maximum number of concurrent threads
JUnit Jupiter does not guarantee that the number of concurrently executing tests
will not exceed the configured parallelism. For example, when using one of the
synchronization mechanisms described in the next section, the ForkJoinPool that is
used behind the scenes may spawn additional threads to ensure execution
continues with sufficient parallelism. Thus, if you require such guarantees in a test
class, please use your own means of controlling concurrency.
2.19.2. Synchronization
In addition to controlling the execution mode using the @Execution annotation, JUnit Jupiter
provides another annotation-based declarative synchronization mechanism. The @ResourceLock
annotation allows you to declare that a test class or method uses a specific shared resource that
requires synchronized access to ensure reliable test execution. The shared resource is identified by
a unique name which is a String. The name can be user-defined or one of the predefined constants
in Resources: SYSTEM_PROPERTIES, SYSTEM_OUT, SYSTEM_ERR, LOCALE, or TIME_ZONE.
If the tests in the following example were run in parallel without the use of @ResourceLock, they
would be flaky. Sometimes they would pass, and at other times they would fail due to the inherent

race condition of writing and then reading the same JVM System Property.
When access to shared resources is declared using the @ResourceLock annotation, the JUnit Jupiter
engine uses this information to ensure that no conflicting tests are run in parallel.
In addition to the String that uniquely identifies the shared resource, you may specify an access
mode. Two tests that require READ access to a shared resource may run in parallel with each other
but not while any other test that requires READ_WRITE access to the same shared resource is running.
@Execution(CONCURRENT)
class SharedResourcesDemo {
    private Properties backup;
    @BeforeEach
    void backup() {
        backup = new Properties();
        backup.putAll(System.getProperties());
    }
    @AfterEach
    void restore() {
        System.setProperties(backup);
    }
    @Test
    @ResourceLock(value = SYSTEM_PROPERTIES, mode = READ)
    void customPropertyIsNotSetByDefault() {
        assertNull(System.getProperty("my.prop"));
    }
    @Test
    @ResourceLock(value = SYSTEM_PROPERTIES, mode = READ_WRITE)
    void canSetCustomPropertyToApple() {
        System.setProperty("my.prop", "apple");
        assertEquals("apple", System.getProperty("my.prop"));
    }
    @Test
    @ResourceLock(value = SYSTEM_PROPERTIES, mode = READ_WRITE)
    void canSetCustomPropertyToBanana() {
        System.setProperty("my.prop", "banana");
        assertEquals("banana", System.getProperty("my.prop"));
    }
}

2.20. Built-in Extensions
While the JUnit team encourages reusable extensions to be packaged and maintained in separate
libraries, the JUnit Jupiter API artifact includes a few user-facing extension implementations that
are considered so generally useful that users shouldn’t have to add another dependency.
2.20.1. The TempDirectory Extension

@TempDir is an experimental feature
You’re invited to give it a try and provide feedback to the JUnit team so they can
improve and eventually promote this feature.
The built-in TempDirectory extension is used to create and clean up a temporary directory for an
individual test or all tests in a test class. It is registered by default. To use it, annotate a non-private
field of type java.nio.file.Path or java.io.File with @TempDir or add a parameter of type
java.nio.file.Path or java.io.File annotated with @TempDir to a lifecycle method or test method.
For example, the following test declares a parameter annotated with @TempDir for a single test
method, creates and writes to a file in the temporary directory, and checks its content.
A test method that requires a temporary directory
@Test
void writeItemsToFile(@TempDir Path tempDir) throws IOException {
    Path file = tempDir.resolve("test.txt");
    new ListWriter(file).write("a", "b", "c");
    assertEquals(singletonList("a,b,c"), Files.readAllLines(file));
}

@TempDir is not supported on constructor parameters. If you wish to retain a single
reference to a temp directory across lifecycle methods and the current test
method, please use field injection, by annotating a non-private instance field with
@TempDir.
The following example stores a shared temporary directory in a static field. This allows the same
sharedTempDir to be used in all lifecycle methods and test methods of the test class.

A test class that shares a temporary directory across test methods
class SharedTempDirectoryDemo {
    @TempDir
    static Path sharedTempDir;
    @Test
    void writeItemsToFile() throws IOException {
        Path file = sharedTempDir.resolve("test.txt");
        new ListWriter(file).write("a", "b", "c");
        assertEquals(singletonList("a,b,c"), Files.readAllLines(file));
    }
    @Test
    void anotherTestThatUsesTheSameTempDir() {
        // use sharedTempDir
    }
}
3. Migrating from JUnit 4
Although the JUnit Jupiter programming model and extension model will not support JUnit 4
features such as Rules and Runners natively, it is not expected that source code maintainers will
need to update all of their existing tests, test extensions, and custom build test infrastructure to
migrate to JUnit Jupiter.
Instead, JUnit provides a gentle migration path via a JUnit Vintage test engine which allows existing
tests based on JUnit 3 and JUnit 4 to be executed using the JUnit Platform infrastructure. Since all
classes and annotations specific to JUnit Jupiter reside under a new org.junit.jupiter base
package, having both JUnit 4 and JUnit Jupiter in the classpath does not lead to any conflicts. It is
therefore safe to maintain existing JUnit 4 tests alongside JUnit Jupiter tests. Furthermore, since the
JUnit team will continue to provide maintenance and bug fix releases for the JUnit 4.x baseline,
developers have plenty of time to migrate to JUnit Jupiter on their own schedule.
3.1. Running JUnit 4 Tests on the JUnit Platform
Just make sure that the junit-vintage-engine artifact is in your test runtime path. In that case JUnit
3 and JUnit 4 tests will automatically be picked up by the JUnit Platform launcher.
See the example projects in the junit5-samples repository to find out how this is done with Gradle
and Maven.

3.1.1. Categories Support
For test classes or methods that are annotated with @Category, the JUnit Vintage test engine  exposes
the category’s fully qualified class name as a tag of the corresponding test identifier. For example, if
a test method is annotated with @Category(Example.class), it will be tagged with "com.acme.Example".
Similar to the Categories runner in JUnit 4, this information can be used to filter the discovered
tests before executing them (see Running Tests for details).
3.2. Migration Tips
The following are topics that you should be aware of when migrating existing JUnit 4 tests to JUnit
Jupiter.
• Annotations reside in the org.junit.jupiter.api package.
• Assertions reside in org.junit.jupiter.api.Assertions.
◦ Note that you may continue to use assertion methods from org.junit.Assert or any other
assertion library such as AssertJ, Hamcrest, Truth, etc.
• Assumptions reside in org.junit.jupiter.api.Assumptions.
◦ Note that JUnit Jupiter 5.4 and later versions support methods from JUnit 4’s
org.junit.Assume class for assumptions. Specifically, JUnit Jupiter supports JUnit 4’s
AssumptionViolatedException to signal that a test should be aborted instead of marked as a
failure.
• @Before and @After no longer exist; use @BeforeEach and @AfterEach instead.
• @BeforeClass and @AfterClass no longer exist; use @BeforeAll and @AfterAll instead.
• @Ignore no longer exists: use @Disabled or one of the other built-in execution conditions instead
◦ See also JUnit 4 @Ignore Support.
• @Category no longer exists; use @Tag instead.
• @RunWith no longer exists; superseded by @ExtendWith.
• @Rule and @ClassRule no longer exist; superseded by @ExtendWith and @RegisterExtension
◦ See also Limited JUnit 4 Rule Support.
3.3. Limited JUnit 4 Rule Support
As stated above, JUnit Jupiter does not and will not support JUnit 4 rules natively. The JUnit team
realizes, however, that many organizations, especially large ones, are likely to have large JUnit 4
code bases that make use of custom rules. To serve these organizations and enable a gradual
migration path the JUnit team has decided to support a selection of JUnit 4 rules verbatim within
JUnit Jupiter. This support is based on adapters and is limited to those rules that are semantically
compatible to the JUnit Jupiter extension model, i.e. those that do not completely change the overall
execution flow of the test.
The junit-jupiter-migrationsupport module from JUnit Jupiter currently supports the following
three Rule types including subclasses of these types:

• org.junit.rules.ExternalResource (including org.junit.rules.TemporaryFolder)
• org.junit.rules.Verifier (including org.junit.rules.ErrorCollector)
• org.junit.rules.ExpectedException
As in JUnit 4, Rule-annotated fields as well as methods are supported. By using these class-level
extensions on a test class such Rule implementations in legacy code bases can be left unchanged 
including the JUnit 4 rule import statements.
This limited form of Rule support can be switched on by the class-level annotation
@EnableRuleMigrationSupport. This annotation is a composed annotation  which enables all rule
migration support extensions: VerifierSupport, ExternalResourceSupport, and
ExpectedExceptionSupport. You may alternatively choose to annotate your test class with
@EnableJUnit4MigrationSupport which registers migration support for rules and JUnit 4’s @Ignore
annotation (see JUnit 4 @Ignore Support).
However, if you intend to develop a new extension for JUnit 5 please use the new extension model
of JUnit Jupiter instead of the rule-based model of JUnit 4.
 JUnit 4 Rule support in JUnit Jupiter is currently an experimental feature. Consult
the table in Experimental APIs for detail.
3.4. JUnit 4 @Ignore Support
In order to provide a smooth migration path from JUnit 4 to JUnit Jupiter, the junit-jupiter-
migrationsupport module provides support for JUnit 4’s @Ignore annotation analogous to Jupiter’s
@Disabled annotation.
To use @Ignore with JUnit Jupiter based tests, configure a test dependency on the junit-jupiter-
migrationsupport module in your build and then annotate your test class with
@ExtendWith(IgnoreCondition.class) or @EnableJUnit4MigrationSupport (which automatically
registers the IgnoreCondition along with Limited JUnit 4 Rule Support ). The IgnoreCondition is an
ExecutionCondition that disables test classes or test methods that are annotated with @Ignore.

import org.junit.Ignore;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.migrationsupport.EnableJUnit4MigrationSupport;
// @ExtendWith(IgnoreCondition.class)
@EnableJUnit4MigrationSupport
class IgnoredTestsDemo {
    @Ignore
    @Test
    void testWillBeIgnored() {
    }
    @Test
    void testWillBeExecuted() {
    }
}
 JUnit 4 @Ignore support in JUnit Jupiter is currently an experimental feature.
Consult the table in Experimental APIs for detail.
4. Running Tests
4.1. IDE Support
4.1.1. IntelliJ IDEA
IntelliJ IDEA supports running tests on the JUnit Platform since version 2016.2. For details please
see the post on the IntelliJ IDEA blog . Note, however, that it is recommended to use IDEA 2017.3 or
newer since these newer versions of IDEA will download the following JARs automatically based on
the API version used in the project: junit-platform-launcher, junit-jupiter-engine, and junit-
vintage-engine.

IntelliJ IDEA releases prior to IDEA 2017.3 bundle specific versions of JUnit 5. Thus,
if you want to use a newer version of JUnit Jupiter, execution of tests within the
IDE might fail due to version conflicts. In such cases, please follow the instructions
below to use a newer version of JUnit 5 than the one bundled with IntelliJ IDEA.
In order to use a different JUnit 5 version (e.g., 5.5.0), you may need to include the corresponding
versions of the junit-platform-launcher, junit-jupiter-engine, and junit-vintage-engine JARs in the
classpath.

Additional Gradle Dependencies
// Only needed to run tests in a version of IntelliJ IDEA that bundles older versions
testRuntimeOnly("org.junit.platform:junit-platform-launcher:1.5.0")
testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.5.0")
testRuntimeOnly("org.junit.vintage:junit-vintage-engine:5.5.0")
Additional Maven Dependencies
<!-- Only needed to run tests in a version of IntelliJ IDEA that bundles older
versions -->
<dependency>
    <groupId>org.junit.platform</groupId>
    <artifactId>junit-platform-launcher</artifactId>
    <version>1.5.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-engine</artifactId>
    <version>5.5.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.vintage</groupId>
    <artifactId>junit-vintage-engine</artifactId>
    <version>5.5.0</version>
    <scope>test</scope>
</dependency>
4.1.2. Eclipse
Eclipse IDE offers support for the JUnit Platform since the Eclipse Oxygen.1a (4.7.1a) release.
For more information on using JUnit 5 in Eclipse consult the official Eclipse support for JUnit 5 
section of the Eclipse Project Oxygen.1a (4.7.1a) - New and Noteworthy documentation.
4.1.3. NetBeans
NetBeans offers support for JUnit Jupiter and the JUnit Platform since the Apache NetBeans 10.0
release.
For more information consult the JUnit 5 section of the Apache NetBeans 10.0 release notes.
4.1.4. Visual Studio Code
Visual Studio Code supports JUnit Jupiter and the JUnit Platform via the Java Test Runner extension
which is installed by default as part of the Java Extension Pack.

For more information consult the Testing section of the Java in Visual Studio Code documentation.
4.1.5. Other IDEs
If you are using an editor or IDE other than one of those listed in the previous sections, the JUnit
team provides two alternative solutions to assist you in using JUnit 5. You can use the Console
Launcher manually — for example, from the command line — or execute tests with a JUnit 4 based
Runner if your IDE has built-in support for JUnit 4.
4.2. Build Support
4.2.1. Gradle

The JUnit Platform Gradle Plugin has been discontinued
The junit-platform-gradle-plugin developed by the JUnit team was deprecated in
JUnit Platform 1.2 and discontinued in 1.3. Please switch to Gradle’s standard test
task.
Starting with version 4.6, Gradle provides native support for executing tests on the JUnit Platform.
To enable it, you just need to specify useJUnitPlatform() within a test task declaration in
build.gradle:
test {
    useJUnitPlatform()
}
Filtering by tags or engines is also supported:
test {
    useJUnitPlatform {
        includeTags 'fast', 'smoke & feature-a'
        // excludeTags 'slow', 'ci'
        includeEngines 'junit-jupiter'
        // excludeEngines 'junit-vintage'
    }
}
Please refer to the official Gradle documentation for a comprehensive list of options.
Configuration Parameters
The standard Gradle test task currently does not provide a dedicated DSL to set JUnit Platform
configuration parameters  to influence test discovery and execution. However, you can provide
configuration parameters within the build script via system properties (as shown below) or via the
junit-platform.properties file.

test {
    // ...
    systemProperty 'junit.jupiter.conditions.deactivate', '*'
    systemProperties = [
        'junit.jupiter.extensions.autodetection.enabled': 'true',
        'junit.jupiter.testinstance.lifecycle.default': 'per_class'
    ]
    // ...
}
Configuring Test Engines
In order to run any tests at all, a TestEngine implementation must be on the classpath.
To configure support for JUnit Jupiter based tests, configure a testImplementation dependency on
the JUnit Jupiter API and a testRuntimeOnly dependency on the JUnit Jupiter TestEngine
implementation similar to the following.
dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.5.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.5.0")
}
The JUnit Platform can run JUnit 4 based tests as long as you configure a testImplementation
dependency on JUnit 4 and a testRuntimeOnly dependency on the JUnit Vintage TestEngine
implementation similar to the following.
dependencies {
    testImplementation("junit:junit:4.12")
    testRuntimeOnly("org.junit.vintage:junit-vintage-engine:5.5.0")
}
Configuring Logging (optional)
JUnit uses the Java Logging APIs in the java.util.logging package (a.k.a. JUL) to emit warnings and
debug information. Please refer to the official documentation of LogManager for configuration
options.
Alternatively, it’s possible to redirect log messages to other logging frameworks such as Log4j or
Logback. To use a logging framework that provides a custom implementation of LogManager, set the
java.util.logging.manager system property to the fully qualified class name  of the LogManager
implementation to use. The example below demonstrates how to configure Log4j 2.x (see Log4j JDK
Logging Adapter for details).

test {
    systemProperty 'java.util.logging.manager',
'org.apache.logging.log4j.jul.LogManager'
}
Other logging frameworks provide different means to redirect messages logged using
java.util.logging. For example, for Logback you can use the JUL to SLF4J Bridge  by adding an
additional dependency to the runtime classpath.
4.2.2. Maven

The JUnit Platform Maven Surefire Provider has been discontinued
The junit-platform-surefire-provider, which was originally developed by the
JUnit team, was deprecated in JUnit Platform 1.3 and discontinued in 1.4. Please
use Maven Surefire’s native support instead.
Starting with version 2.22.0 , Maven Surefire and Maven Failsafe provide native support  for
executing tests on the JUnit Platform. The pom.xml file in the junit5-jupiter-starter-maven project
demonstrates how to use the Maven Surefire plugin and can serve as a starting point for
configuring your Maven build.
Configuring Test Engines
In order to have Maven Surefire or Maven Failsafe run any tests at all, at least one TestEngine
implementation must be added to the test classpath.
To configure support for JUnit Jupiter based tests, configure test scoped dependencies on the JUnit
Jupiter API and the JUnit Jupiter TestEngine implementation similar to the following.

<build>
    <plugins>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
        </plugin>
        <plugin>
            <artifactId>maven-failsafe-plugin</artifactId>
            <version>2.22.2</version>
        </plugin>
    </plugins>
</build>
<!-- ... -->
<dependencies>
    <!-- ... -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-api</artifactId>
        <version>5.5.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.5.0</version>
        <scope>test</scope>
    </dependency>
    <!-- ... -->
</dependencies>
<!-- ... -->
Maven Surefire and Maven Failsafe can run JUnit 4 based tests alongside Jupiter tests as long as you
configure test scoped dependencies on JUnit 4 and the JUnit Vintage TestEngine implementation
similar to the following.

<!-- ... -->
<build>
    <plugins>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
        </plugin>
        <plugin>
            <artifactId>maven-failsafe-plugin</artifactId>
            <version>2.22.2</version>
        </plugin>
    </plugins>
</build>
<!-- ... -->
<dependencies>
    <!-- ... -->
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.12</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.vintage</groupId>
        <artifactId>junit-vintage-engine</artifactId>
        <version>5.5.0</version>
        <scope>test</scope>
    </dependency>
    <!-- ... -->
</dependencies>
<!-- ... -->
Filtering by Test Class Names
The Maven Surefire Plugin will scan for test classes whose fully qualified names match the
following patterns.
• **/Test*.java
• **/*Test.java
• **/*Tests.java
• **/*TestCase.java
Moreover, it will exclude all nested classes (including static member classes) by default.
Note, however, that you can override this default behavior by configuring explicit include and
exclude rules in your pom.xml file. For example, to keep Maven Surefire from excluding static
member classes, you can override its exclude rules as follows.

Overriding exclude rules of Maven Surefire
<!-- ... -->
<build>
    <plugins>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
            <configuration>
                <excludes>
                    <exclude/>
                </excludes>
            </configuration>
        </plugin>
    </plugins>
</build>
<!-- ... -->
Please see the Inclusions and Exclusions of Tests documentation for Maven Surefire for details.
Filtering by Tags
You can filter tests by tags or tag expressions using the following configuration properties.
• to include tags or tag expressions, use groups.
• to exclude tags or tag expressions, use excludedGroups.
<!-- ... -->
<build>
    <plugins>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
            <configuration>
                <groups>acceptance | !feature-a</groups>
                <excludedGroups>integration, regression</excludedGroups>
            </configuration>
        </plugin>
    </plugins>
</build>
<!-- ... -->
Configuration Parameters
You can set JUnit Platform configuration parameters to influence test discovery and execution by
declaring the configurationParameters property and providing key-value pairs using the Java
Properties file syntax (as shown below) or via the junit-platform.properties file.

<!-- ... -->
<build>
    <plugins>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
            <configuration>
                <properties>
                    <configurationParameters>
                        junit.jupiter.conditions.deactivate = *
                        junit.jupiter.extensions.autodetection.enabled = true
                        junit.jupiter.testinstance.lifecycle.default = per_class
                    </configurationParameters>
                </properties>
            </configuration>
        </plugin>
    </plugins>
</build>
<!-- ... -->
4.2.3. Ant
Starting with version 1.10.3 of Ant, a new junitlauncher task has been introduced to provide native
support for launching tests on the JUnit Platform. The junitlauncher task is solely responsible for
launching the JUnit Platform and passing it the selected collection of tests. The JUnit Platform then
delegates to registered test engines to discover and execute the tests.
The junitlauncher task attempts to align as close as possible with native Ant constructs such as
resource collections for allowing users to select the tests that they want executed by test engines.
This gives the task a consistent and natural feel when compared to many other core Ant tasks.
Starting with version 1.10.6 of Ant, the junitlauncher task supports forking the tests in a separate
JVM.
The build.xml file in the junit5-jupiter-starter-ant project demonstrates how to use the task and
can serve as a starting point.
Basic Usage
The following example demonstrates how to configure the junitlauncher task to select a single test
class (i.e., org.myapp.test.MyFirstJUnit5Test).

<path id="test.classpath">
    <!-- The location where you have your compiled classes -->
    <pathelement location="${build.classes.dir}" />
</path>
<!-- ... -->
<junitlauncher>
    <classpath refid="test.classpath" />
    <test name="org.myapp.test.MyFirstJUnit5Test" />
</junitlauncher>
The test element allows you to specify a single test class that you want to be selected and executed.
The classpath element allows you to specify the classpath to be used to launch the JUnit Platform.
This classpath will also be used to locate test classes that are part of the execution.
The following example demonstrates how to configure the junitlauncher task to select test classes
from multiple locations.
<path id="test.classpath">
    <!-- The location where you have your compiled classes -->
    <pathelement location="${build.classes.dir}" />
</path>
<!-- ... -->
<junitlauncher>
    <classpath refid="test.classpath" />
    <testclasses outputdir="${output.dir}">
        <fileset dir="${build.classes.dir}">
            <include name="org/example/**/demo/**/" />
        </fileset>
        <fileset dir="${some.other.dir}">
            <include name="org/myapp/**/" />
        </fileset>
    </testclasses>
</junitlauncher>
In the above example, the testclasses element allows you to select multiple test classes that reside
in different locations.
For further details on usage and configuration options please refer to the official Ant
documentation for the junitlauncher task.
4.3. Console Launcher
The ConsoleLauncher is a command-line Java application that lets you launch the JUnit Platform
from the console. For example, it can be used to run JUnit Vintage and JUnit Jupiter tests and print
test execution results to the console.

An executable junit-platform-console-standalone-1.5.0.jar with all dependencies included is
published in the Maven Central repository under the junit-platform-console-standalone directory.
You can run the standalone ConsoleLauncher as shown below.
java -jar junit-platform-console-standalone-1.5.0.jar <Options>
Here’s an example of its output:
├─ JUnit Vintage
│  └─ example.JUnit4Tests
│     └─ standardJUnit4Test ✔
└─ JUnit Jupiter
   ├─ StandardTests
   │  ├─ succeedingTest() ✔
   │  └─ skippedTest() ↷ for demonstration purposes
   └─ A special test case
      ├─ Custom test name containing spaces ✔
      ├─ ╯°□°）╯ ✔
      └─  ✔
Test run finished after 64 ms
[         5 containers found      ]
[         0 containers skipped    ]
[         5 containers started    ]
[         0 containers aborted    ]
[         5 containers successful ]
[         0 containers failed     ]
[         6 tests found           ]
[         1 tests skipped         ]
[         5 tests started         ]
[         0 tests aborted         ]
[         5 tests successful      ]
[         0 tests failed          ]

Exit Code
The ConsoleLauncher exits with a status code of 1 if any containers or tests failed. If
no tests are discovered and the --fail-if-no-tests command-line option is
supplied, the ConsoleLauncher exits with a status code of 2. Otherwise the exit code
is 0.
4.3.1. Options
Thanks for using JUnit! Support its development at https://junit.org/sponsoring
Usage: ConsoleLauncher [-h] [--disable-ansi-colors] [--disable-banner]
                       [--fail-if-no-tests] [--scan-modules] [--scan-
classpath[=PATH[;|:
                       PATH...]]]... [--details=MODE] [--details-theme=THEME]

[--reports-dir=DIR] [--config=KEY=VALUE]...
                       [--exclude-package=PKG]... [--include-package=PKG]...
                       [-c=CLASS]... [-cp=PATH[;|:PATH...]]... [-d=DIR]... [-e=ID]...
                       [-E=ID]... [-f=FILE]... [-m=NAME]... [-n=PATTERN]...
                       [-N=PATTERN]... [-o=NAME]... [-p=PKG]... [-r=RESOURCE]...
                       [-t=TAG]... [-T=TAG]... [-u=URI]...
Launches the JUnit Platform from the console.
  -h, --help                 Display help information.
      --disable-ansi-colors  Disable ANSI colors in output (not supported by all
terminals).
      --disable-banner       Disable print out of the welcome message.
      --details=MODE         Select an output details mode for when tests are
executed. Use
                               one of: none, summary, flat, tree, verbose. If 'none'
is
                               selected, then only the summary and test failures are
shown.
                               Default: tree.
      --details-theme=THEME  Select an output details tree theme for when tests are
executed.
                               Use one of: ascii, unicode. Default: unicode.
      -cp, --classpath, --class-path=PATH[;|:PATH...]
                             Provide additional classpath entries -- for example, for
adding
                               engines and their dependencies. This option can be
repeated.
      --fail-if-no-tests     Fail and return exit status code 2 if no tests are found.
      --reports-dir=DIR      Enable report output into a specified local directory
(will be
                               created if it does not exist).
      --scan-modules         EXPERIMENTAL: Scan all resolved modules for test
discovery.
  -o, --select-module=NAME   EXPERIMENTAL: Select single module for test discovery.
This
                               option can be repeated.
      --scan-classpath, --scan-class-path[=PATH[;|:PATH...]]
                             Scan all directories on the classpath or explicit
classpath
                               roots. Without arguments, only directories on the
system
                               classpath as well as additional classpath entries
supplied via
                               -cp (directories and JAR files) are scanned. Explicit
classpath
                               roots that are not on the classpath will be silently
ignored.
                               This option can be repeated.
  -u, --select-uri=URI       Select a URI for test discovery. This option can be
repeated.
  -f, --select-file=FILE     Select a file for test discovery. This option can be
repeated.

-d, --select-directory=DIR Select a directory for test discovery. This option can be
                               repeated.
  -p, --select-package=PKG   Select a package for test discovery. This option can be
repeated.
  -c, --select-class=CLASS   Select a class for test discovery. This option can be
repeated.
  -m, --select-method=NAME   Select a method for test discovery. This option can be
repeated.
  -r, --select-resource=RESOURCE
                             Select a classpath resource for test discovery. This
option can
                               be repeated.
  -n, --include-classname=PATTERN
                             Provide a regular expression to include only classes
whose fully
                               qualified names match. To avoid loading classes
unnecessarily,
                               the default pattern only includes class names that
begin with
                               "Test" or end with "Test" or "Tests". When this option
is
                               repeated, all patterns will be combined using OR
semantics.
                               Default: [^(Test.*|.+[.$]Test.*|.*Tests?)$]
  -N, --exclude-classname=PATTERN
                             Provide a regular expression to exclude those classes
whose fully
                               qualified names match. When this option is repeated,
all
                               patterns will be combined using OR semantics.
      --include-package=PKG  Provide a package to be included in the test run. This
option can
                               be repeated.
      --exclude-package=PKG  Provide a package to be excluded from the test run. This
option
                               can be repeated.
  -t, --include-tag=TAG      Provide a tag or tag expression to include only tests
whose tags
                               match. When this option is repeated, all patterns will
be
                               combined using OR semantics.
  -T, --exclude-tag=TAG      Provide a tag or tag expression to exclude those tests
whose tags
                               match. When this option is repeated, all patterns will
be
                               combined using OR semantics.
  -e, --include-engine=ID    Provide the ID of an engine to be included in the test
run. This
                               option can be repeated.
  -E, --exclude-engine=ID    Provide the ID of an engine to be excluded from the test
run.

This option can be repeated.
      --config=KEY=VALUE     Set a configuration parameter for test discovery and
execution.
                               This option can be repeated.
4.3.2. Argument Files (@-files)
On some platforms you may run into system limitations on the length of a command line when
creating a command line with lots of options or with long arguments.
Since version 1.3, the ConsoleLauncher supports argument files, also known as @-files. Argument files
are files that themselves contain arguments to be passed to the command. When the underlying
picocli command line parser encounters an argument beginning with the character @, it expands
the contents of that file into the argument list.
The arguments within a file can be separated by spaces or newlines. If an argument contains
embedded whitespace, the whole argument should be wrapped in double or single quotes — for
example, "-f=My Files/Stuff.java".
If the argument file does not exist or cannot be read, the argument will be treated literally and will
not be removed. This will likely result in an "unmatched argument" error message. You can
troubleshoot such errors by executing the command with the picocli.trace system property set to
DEBUG.
Multiple @-files may be specified on the command line. The specified path may be relative to the
current directory or absolute.
You can pass a real parameter with an initial @ character by escaping it with an additional @ symbol.
For example, @@somearg will become @somearg and will not be subject to expansion.
4.4. Using JUnit 4 to run the JUnit Platform
The JUnitPlatform runner is a JUnit 4 based Runner which enables you to run any test whose
programming model is supported on the JUnit Platform in a JUnit 4 environment — for example, a
JUnit Jupiter test class.
Annotating a class with @RunWith(JUnitPlatform.class) allows it to be run with IDEs and build
systems that support JUnit 4 but do not yet support the JUnit Platform directly.

Since the JUnit Platform has features that JUnit 4 does not have, the runner is only
able to support a subset of the JUnit Platform functionality, especially with regard
to reporting (see Display Names vs. Technical Names ). But for the time being the
JUnitPlatform runner is an easy way to get started.
4.4.1. Setup
You need the following artifacts and their dependencies on the classpath. See Dependency Metadata
for details regarding group IDs, artifact IDs, and versions.

Explicit Dependencies
• junit-platform-runner in test scope: location of the JUnitPlatform runner
• junit-4.12.jar in test scope: to run tests using JUnit 4
• junit-jupiter-api in test scope: API for writing tests using JUnit Jupiter, including @Test, etc.
• junit-jupiter-engine in test runtime  scope: implementation of the TestEngine API for JUnit
Jupiter
Transitive Dependencies
• junit-platform-suite-api in test scope
• junit-platform-launcher in test scope
• junit-platform-engine in test scope
• junit-platform-commons in test scope
• opentest4j in test scope
4.4.2. Display Names vs. Technical Names
To define a custom display name  for the class run via @RunWith(JUnitPlatform.class) simply
annotate the class with @SuiteDisplayName and provide a custom value.
By default, display names will be used for test artifacts; however, when the JUnitPlatform runner is
used to execute tests with a build tool such as Gradle or Maven, the generated test report often
needs to include the technical names of test artifacts — for example, fully qualified class names —
instead of shorter display names like the simple name of a test class or a custom display name
containing special characters. To enable technical names for reporting purposes, simply declare the
@UseTechnicalNames annotation alongside @RunWith(JUnitPlatform.class).
Note that the presence of @UseTechnicalNames overrides any custom display name configured via
@SuiteDisplayName.
4.4.3. Single Test Class
One way to use the JUnitPlatform runner is to annotate a test class with
@RunWith(JUnitPlatform.class) directly. Please note that the test methods in the following example
are annotated with org.junit.jupiter.api.Test (JUnit Jupiter), not org.junit.Test (JUnit 4).
Moreover, in this case the test class must be public; otherwise, some IDEs and build tools might not
recognize it as a JUnit 4 test class.

import static org.junit.jupiter.api.Assertions.fail;
import org.junit.jupiter.api.Test;
import org.junit.platform.runner.JUnitPlatform;
import org.junit.runner.RunWith;
@RunWith(JUnitPlatform.class)
public class JUnitPlatformClassDemo {
    @Test
    void succeedingTest() {
        /* no-op */
    }
    @Test
    void failingTest() {
        fail("Failing for failing's sake.");
    }
}
4.4.4. Test Suite
If you have multiple test classes you can create a test suite as can be seen in the following example.
import org.junit.platform.runner.JUnitPlatform;
import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.SuiteDisplayName;
import org.junit.runner.RunWith;
@RunWith(JUnitPlatform.class)
@SuiteDisplayName("JUnit Platform Suite Demo")
@SelectPackages("example")
public class JUnitPlatformSuiteDemo {
}
The JUnitPlatformSuiteDemo will discover and run all tests in the example package and its
subpackages. By default, it will only include test classes whose names either begin with Test or end
with Test or Tests.

Additional Configuration Options
There are more configuration options for discovering and filtering tests than just
@SelectPackages. Please consult the Javadoc for further details.


Test classes and suites annotated with @RunWith(JUnitPlatform.class) cannot be
executed directly on the JUnit Platform (or as a "JUnit 5" test as documented in
some IDEs). Such classes and suites can only be executed using JUnit 4
infrastructure.
4.5. Configuration Parameters
In addition to instructing the platform which test classes and test engines to include, which
packages to scan, etc., it is sometimes necessary to provide additional custom configuration
parameters that are specific to a particular test engine or registered extension. For example, the
JUnit Jupiter TestEngine supports configuration parameters for the following use cases.
• Changing the Default Test Instance Lifecycle
• Enabling Automatic Extension Detection
• Deactivating Conditions
• Setting the Default Display Name Generator
Configuration Parameters  are text-based key-value pairs that can be supplied to test engines
running on the JUnit Platform via one of the following mechanisms.
1. The configurationParameter() and configurationParameters() methods in the
LauncherDiscoveryRequestBuilder which is used to build a request supplied to the Launcher API.
When running tests via one of the tools provided by the JUnit Platform you can specify
configuration parameters as follows:
◦ Console Launcher: use the --config command-line option.
◦ Gradle: use the systemProperty or systemProperties DSL.
◦ Maven Surefire provider: use the configurationParameters property.
2. JVM system properties.
3. The JUnit Platform configuration file: a file named junit-platform.properties in the root of the
class path that follows the syntax rules for a Java Properties file.

Configuration parameters are looked up in the exact order defined above.
Consequently, configuration parameters supplied directly to the Launcher take
precedence over those supplied via system properties and the configuration file.
Similarly, configuration parameters supplied via system properties take
precedence over those supplied via the configuration file.
4.6. Tag Expressions
Tag expressions are boolean expressions with the operators !, & and |. In addition, ( and ) can be
used to adjust for operator precedence.
Table 2. Operators (in descending order of precedence)

Operator Meaning Associativity
! not right
& and left
| or left
If you are tagging your tests across multiple dimensions, tag expressions help you to select which
tests to execute. When tagging by test type (e.g., micro, integration, end-to-end) and feature (e.g.,
product, catalog, shipping), the following tag expressions can be useful.
Tag Expression Selection
product all tests for product
catalog | shipping all tests for catalog plus all tests for shipping
catalog & shipping all tests for the intersection between catalog and shipping
product & !end-to-end all tests for product, but not the end-to-end tests
(micro | integration) & (product |
shipping)
all micro or integration tests for product or shipping
4.7. Capturing Standard Output/Error
Since version 1.3, the JUnit Platform provides opt-in support for capturing output printed to
System.out and System.err. To enable it, simply set the junit.platform.output.capture.stdout and/or
junit.platform.output.capture.stderr configuration parameter  to true. In addition, you may
configure the maximum number of buffered bytes to be used per executed test or container using
junit.platform.output.capture.maxBuffer.
If enabled, the JUnit Platform captures the corresponding output and publishes it as a report entry
using the stdout or stderr keys to all registered TestExecutionListener instances immediately before
reporting the test or container as finished.
Please note that the captured output will only contain output emitted by the thread that was used to
execute a container or test. Any output by other threads will be omitted because particularly when
executing tests in parallel it would be impossible to attribute it to a specific test or container.

Capturing output is currently an experimental feature. You’re invited to give it a try
and provide feedback to the JUnit team so they can improve and eventually
promote this feature.
5. Extension Model
5.1. Overview
In contrast to the competing Runner, TestRule, and MethodRule extension points in JUnit 4, the JUnit
Jupiter extension model consists of a single, coherent concept: the Extension API. Note, however,

that Extension itself is just a marker interface.
5.2. Registering Extensions
Extensions can be registered declaratively via @ExtendWith, programmatically via
@RegisterExtension, or automatically via Java’s ServiceLoader mechanism.
5.2.1. Declarative Extension Registration
Developers can register one or more extensions declaratively by annotating a test interface, test
class, test method, or custom composed annotation  with @ExtendWith(…) and supplying class
references for the extensions to register.
For example, to register a custom RandomParametersExtension for a particular test method, you
would annotate the test method as follows.
@ExtendWith(RandomParametersExtension.class)
@Test
void test(@Random int i) {
    // ...
}
To register a custom RandomParametersExtension for all tests in a particular class and its subclasses,
you would annotate the test class as follows.
@ExtendWith(RandomParametersExtension.class)
class MyTests {
    // ...
}
Multiple extensions can be registered together like this:
@ExtendWith({ DatabaseExtension.class, WebServerExtension.class })
class MyFirstTests {
    // ...
}
As an alternative, multiple extensions can be registered separately like this:
@ExtendWith(DatabaseExtension.class)
@ExtendWith(WebServerExtension.class)
class MySecondTests {
    // ...
}


Extension Registration Order
Extensions registered declaratively via @ExtendWith will be executed in the order in
which they are declared in the source code. For example, the execution of tests in
both MyFirstTests and MySecondTests will be extended by the DatabaseExtension and
WebServerExtension, in exactly that order.
5.2.2. Programmatic Extension Registration
Developers can register extensions programmatically by annotating fields in test classes with
@RegisterExtension.
When an extension is registered declaratively via @ExtendWith, it can typically only be configured via
annotations. In contrast, when an extension is registered via @RegisterExtension, it can be
configured programmatically — for example, in order to pass arguments to the extension’s
constructor, a static factory method, or a builder API.

Extension Registration Order
By default, extensions registered programmatically via @RegisterExtension will be
ordered using an algorithm that is deterministic but intentionally nonobvious.
This ensures that subsequent runs of a test suite execute extensions in the same
order, thereby allowing for repeatable builds. However, there are times when
extensions need to be registered in an explicit order. To achieve that, annotate
each @RegisterExtension field with @Order. Any @RegisterExtension field not
annotated with @Order will appear at the end of the sorted list.
 @RegisterExtension fields must not be private or null (at evaluation time) but may
be either static or non-static.
Static Fields
If a @RegisterExtension field is static, the extension will be registered after extensions that are
registered at the class level via @ExtendWith. Such static extensions  are not limited in which
extension APIs they can implement. Extensions registered via static fields may therefore implement
class-level and instance-level extension APIs such as BeforeAllCallback, AfterAllCallback, and
TestInstancePostProcessor as well as method-level extension APIs such as BeforeEachCallback, etc.
In the following example, the server field in the test class is initialized programmatically by using a
builder pattern supported by the WebServerExtension. The configured WebServerExtension will be
automatically registered as an extension at the class level — for example, in order to start the
server before all tests in the class and then stop the server after all tests in the class have
completed. In addition, static lifecycle methods annotated with @BeforeAll or @AfterAll as well as
@BeforeEach, @AfterEach, and @Test methods can access the instance of the extension via the server
field if necessary.

An extension registered via a static field
class WebServerDemo {
    @RegisterExtension
    static WebServerExtension server = WebServerExtension.builder()
        .enableSecurity(false)
        .build();
    @Test
    void getProductList() {
        WebClient webClient = new WebClient();
        String serverUrl = server.getServerUrl();
        // Use WebClient to connect to web server using serverUrl and verify response
        assertEquals(200, webClient.get(serverUrl + "/products").getResponseStatus());
    }
}
Static Fields in Kotlin
The Kotlin programming language does not have the concept of a static field. However, the
compiler can be instructed to generate static fields using annotations. Since, as stated earlier,
@RegisterExtension fields must not be private nor null, one cannot use the @JvmStatic annotation in
Kotlin as it generates private fields. Rather, the @JvmField annotation must be used.
The following example is a version of the WebServerDemo from the previous section that has been
ported to Kotlin.
Registering an extension via a static field in Kotlin
class KotlinWebServerDemo {
    companion object {
        @JvmField
        @RegisterExtension
        val server = WebServerExtension.builder()
                .enableSecurity(false)
                .build()
    }
    @Test
    fun getProductList() {
        // Use WebClient to connect to web server using serverUrl and verify response
        val webClient = WebClient()
        val serverUrl = server.serverUrl
        assertEquals(200, webClient.get("$serverUrl/products").responseStatus)
    }
}

Instance Fields
If a @RegisterExtension field is non-static (i.e., an instance field), the extension will be registered
after the test class has been instantiated and after each registered TestInstancePostProcessor has
been given a chance to post-process the test instance (potentially injecting the instance of the
extension to be used into the annotated field). Thus, if such an instance extension implements class-
level or instance-level extension APIs such as BeforeAllCallback, AfterAllCallback, or
TestInstancePostProcessor, those APIs will not be honored. By default, an instance extension will be
registered after extensions that are registered at the method level via @ExtendWith; however, if the
test class is configured with @TestInstance(Lifecycle.PER_CLASS) semantics, an instance extension
will be registered before extensions that are registered at the method level via @ExtendWith.
In the following example, the docs field in the test class is initialized programmatically by invoking
a custom lookUpDocsDir() method and supplying the result to the static forPath() factory method in
the DocumentationExtension. The configured DocumentationExtension will be automatically registered
as an extension at the method level. In addition, @BeforeEach, @AfterEach, and @Test methods can
access the instance of the extension via the docs field if necessary.
An extension registered via an instance field
class DocumentationDemo {
    static Path lookUpDocsDir() {
        // return path to docs dir
    }
    @RegisterExtension
    DocumentationExtension docs = DocumentationExtension.forPath(lookUpDocsDir());
    @Test
    void generateDocumentation() {
        // use this.docs ...
    }
}
5.2.3. Automatic Extension Registration
In addition to declarative extension registration  and programmatic extension registration  support
using annotations, JUnit Jupiter also supports global extension registration  via Java’s
java.util.ServiceLoader mechanism, allowing third-party extensions to be auto-detected and
automatically registered based on what is available in the classpath.
Specifically, a custom extension can be registered by supplying its fully qualified class name in a file
named org.junit.jupiter.api.extension.Extension within the /META-INF/services folder in its
enclosing JAR file.
Enabling Automatic Extension Detection
Auto-detection is an advanced feature and is therefore not enabled by default. To enable it, simply

set the junit.jupiter.extensions.autodetection.enabled configuration parameter to true. This can be
supplied as a JVM system property, as a configuration parameter in the LauncherDiscoveryRequest
that is passed to the Launcher, or via the JUnit Platform configuration file (see Configuration
Parameters for details).
For example, to enable auto-detection of extensions, you can start your JVM with the following
system property.
-Djunit.jupiter.extensions.autodetection.enabled=true
When auto-detection is enabled, extensions discovered via the ServiceLoader mechanism will be
added to the extension registry after JUnit Jupiter’s global extensions (e.g., support for TestInfo,
TestReporter, etc.).
5.2.4. Extension Inheritance
Registered extensions are inherited within test class hierarchies with top-down semantics.
Similarly, extensions registered at the class-level are inherited at the method-level. Furthermore, a
specific extension implementation can only be registered once for a given extension context and its
parent contexts. Consequently, any attempt to register a duplicate extension implementation will be
ignored.
5.3. Conditional Test Execution
ExecutionCondition defines the Extension API for programmatic, conditional test execution.
An ExecutionCondition is evaluated for each container (e.g., a test class) to determine if all the tests it
contains should be executed based on the supplied ExtensionContext. Similarly, an
ExecutionCondition is evaluated for each test to determine if a given test method should be executed
based on the supplied ExtensionContext.
When multiple ExecutionCondition extensions are registered, a container or test is disabled as soon
as one of the conditions returns disabled. Thus, there is no guarantee that a condition is evaluated
because another extension might have already caused a container or test to be disabled. In other
words, the evaluation works like the short-circuiting boolean OR operator.
See the source code of DisabledCondition and @Disabled for concrete examples.
5.3.1. Deactivating Conditions
Sometimes it can be useful to run a test suite without certain conditions being active. For example,
you may wish to run tests even if they are annotated with @Disabled in order to see if they are still
broken. To do this, simply provide a pattern for the junit.jupiter.conditions.deactivate
configuration parameter to specify which conditions should be deactivated (i.e., not evaluated) for
the current test run. The pattern can be supplied as a JVM system property, as a configuration
parameter in the LauncherDiscoveryRequest that is passed to the Launcher, or via the JUnit Platform
configuration file (see Configuration Parameters for details).
For example, to deactivate JUnit’s @Disabled condition, you can start your JVM with the following

system property.
-Djunit.jupiter.conditions.deactivate=org.junit.*DisabledCondition
Pattern Matching Syntax
If the junit.jupiter.conditions.deactivate pattern consists solely of an asterisk ( *), all conditions
will be deactivated. Otherwise, the pattern will be used to match against the fully qualified class
name (FQCN) of each registered condition. Any dot ( .) in the pattern will match against a dot ( .) or
a dollar sign ( $) in the FQCN. Any asterisk ( *) will match against one or more characters in the
FQCN. All other characters in the pattern will be matched one-to-one against the FQCN.
Examples:
• *: deactivates all conditions.
• org.junit.*: deactivates every condition under the org.junit base package and any of its
subpackages.
• *.MyCondition: deactivates every condition whose simple class name is exactly MyCondition.
• *System*: deactivates every condition whose simple class name contains System.
• org.example.MyCondition: deactivates the condition whose FQCN is exactly
org.example.MyCondition.
5.4. Test Instance Factories
TestInstanceFactory defines the API for Extensions that wish to create test class instances.
Common use cases include acquiring the test instance from a dependency injection framework or
invoking a static factory method to create the test class instance.
If no TestInstanceFactory is registered, the framework will simply invoke the sole constructor for
the test class to instantiate it, potentially resolving constructor arguments via registered
ParameterResolver extensions.
Extensions that implement TestInstanceFactory can be registered on test interfaces, top-level test
classes, or @Nested test classes.

Registering multiple extensions that implement TestInstanceFactory for any single
class will result in an exception being thrown for all tests in that class, in any
subclass, and in any nested class. Note that any TestInstanceFactory registered in a
superclass or enclosing class (i.e., in the case of a @Nested test class) is inherited. It is
the user’s responsibility to ensure that only a single TestInstanceFactory is
registered for any specific test class.
5.5. Test Instance Post-processing
TestInstancePostProcessor defines the API for Extensions that wish to post process test instances.

Common use cases include injecting dependencies into the test instance, invoking custom
initialization methods on the test instance, etc.
For a concrete example, consult the source code for the MockitoExtension and the SpringExtension.
5.6. Parameter Resolution
ParameterResolver defines the Extension API for dynamically resolving parameters at runtime.
If a test class constructor, test method, or lifecycle method (see Test Classes and Methods ) accepts a
parameter, the parameter must be resolved at runtime by a ParameterResolver. A ParameterResolver
can either be built-in (see TestInfoParameterResolver) or registered by the user. Generally speaking,
parameters may be resolved by name, type, annotation, or any combination thereof. For concrete
examples, consult the source code for CustomTypeParameterResolver and
CustomAnnotationParameterResolver.

Due to a bug in the byte code generated by javac on JDK versions prior to JDK 9,
looking up annotations on parameters directly via the core
java.lang.reflect.Parameter API will always fail for inner class constructors (e.g., a
constructor in a @Nested test class).
The ParameterContext API supplied to ParameterResolver implementations therefore
includes the following convenience methods for correctly looking up annotations
on parameters. Extension authors are strongly encouraged to use these methods
instead of those provided in java.lang.reflect.Parameter in order to avoid this bug
in the JDK.
• boolean isAnnotated(Class<? extends Annotation> annotationType)
• Optional<A> findAnnotation(Class<A> annotationType)
• List<A> findRepeatableAnnotations(Class<A> annotationType)
5.7. Test Result Processing
TestWatcher defines the API for extensions that wish to process the results of test method executions.
Specifically, a TestWatcher will be invoked with contextual information for the following events.
• testDisabled: invoked after a disabled test method has been skipped
• testSuccessful: invoked after a test method has completed successfully
• testAborted: invoked after a test method has been aborted
• testFailed: invoked after a test method has failed

In contrast to the definition of "test method" presented in Test Classes and
Methods, in this context test method refers to any @Test method or @TestTemplate
method (for example, a @RepeatedTest or @ParameterizedTest).
Extensions implementing this interface can be registered at the method level or at the class level. In
the latter case they will be invoked for any contained test method including those in @Nested classes.


Any instances of ExtensionContext.Store.CloseableResource stored in the Store of
the provided ExtensionContext will be closed before methods in this API are
invoked (see Keeping State in Extensions). You can use the parent context’s Store to
work with such resources.
5.8. Test Lifecycle Callbacks
The following interfaces define the APIs for extending tests at various points in the test execution
lifecycle. Consult the following sections for examples and the Javadoc for each of these interfaces in
the org.junit.jupiter.api.extension package for further details.
• BeforeAllCallback
◦ BeforeEachCallback
▪ BeforeTestExecutionCallback
▪ AfterTestExecutionCallback
◦ AfterEachCallback
• AfterAllCallback

Implementing Multiple Extension APIs
Extension developers may choose to implement any number of these interfaces
within a single extension. Consult the source code of the SpringExtension for a
concrete example.
5.8.1. Before and After Test Execution Callbacks
BeforeTestExecutionCallback and AfterTestExecutionCallback define the APIs for Extensions that
wish to add behavior that will be executed immediately before and immediately after a test method
is executed, respectively. As such, these callbacks are well suited for timing, tracing, and similar use
cases. If you need to implement callbacks that are invoked around @BeforeEach and @AfterEach
methods, implement BeforeEachCallback and AfterEachCallback instead.
The following example shows how to use these callbacks to calculate and log the execution time of
a test method. TimingExtension implements both BeforeTestExecutionCallback and
AfterTestExecutionCallback in order to time and log the test execution.

An extension that times and logs the execution of test methods
import java.lang.reflect.Method;
import java.util.logging.Logger;
import org.junit.jupiter.api.extension.AfterTestExecutionCallback;
import org.junit.jupiter.api.extension.BeforeTestExecutionCallback;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.ExtensionContext.Namespace;
import org.junit.jupiter.api.extension.ExtensionContext.Store;
public class TimingExtension implements BeforeTestExecutionCallback,
AfterTestExecutionCallback {
    private static final Logger logger = Logger.getLogger(TimingExtension.class
.getName());
    private static final String START_TIME = "start time";
    @Override
    public void beforeTestExecution(ExtensionContext context) throws Exception {
        getStore(context).put(START_TIME, System.currentTimeMillis());
    }
    @Override
    public void afterTestExecution(ExtensionContext context) throws Exception {
        Method testMethod = context.getRequiredTestMethod();
        long startTime = getStore(context).remove(START_TIME, long.class);
        long duration = System.currentTimeMillis() - startTime;
        logger.info(() ->
            String.format("Method [%s] took %s ms.", testMethod.getName(), duration));
    }
    private Store getStore(ExtensionContext context) {
        return context.getStore(Namespace.create(getClass(), context
.getRequiredTestMethod()));
    }
}
Since the TimingExtensionTests class registers the TimingExtension via @ExtendWith, its tests will have
this timing applied when they execute.

A test class that uses the example TimingExtension
@ExtendWith(TimingExtension.class)
class TimingExtensionTests {
    @Test
    void sleep20ms() throws Exception {
        Thread.sleep(20);
    }
    @Test
    void sleep50ms() throws Exception {
        Thread.sleep(50);
    }
}
The following is an example of the logging produced when TimingExtensionTests is run.
INFO: Method [sleep20ms] took 24 ms.
INFO: Method [sleep50ms] took 53 ms.
5.9. Exception Handling
Exceptions thrown during the test execution may be intercepted and handled accordingly before
propagating further, so that certain actions like error logging or resource releasing may be defined
in specialized Extensions. JUnit Jupiter offers API for Extensions that wish to handle exceptions
thrown during @Test methods via TestExecutionExceptionHandler and for those thrown during one
of test lifecycle methods ( @BeforeAll, @BeforeEach, @AfterEach and @AfterAll) via
LifecycleMethodExecutionExceptionHandler.
The following example shows an extension which will swallow all instances of IOException but
rethrow any other type of exception.

An exception handling extension that filters IOExceptions in test execution
public class IgnoreIOExceptionExtension implements TestExecutionExceptionHandler {
    @Override
    public void handleTestExecutionException(ExtensionContext context, Throwable
throwable)
            throws Throwable {
        if (throwable instanceof IOException) {
            return;
        }
        throw throwable;
    }
}
Another example shows how to record the state of an application under test exactly at the point of
unexpected exception being thrown during setup and cleanup. Note that unlike relying on lifecycle
callbacks, which may or may not be executed depending on the test status, this solution guarantees
execution immediately after failing @BeforeAll, @BeforeEach, @AfterEach or @AfterAll.

An exception handling extension that records application state on error
class RecordStateOnErrorExtension implements LifecycleMethodExecutionExceptionHandler
{
    @Override
    public void handleBeforeAllMethodExecutionException(ExtensionContext context,
Throwable ex)
            throws Throwable {
        memoryDumpForFurtherInvestigation("Failure recorded during class setup");
        throw ex;
    }
    @Override
    public void handleBeforeEachMethodExecutionException(ExtensionContext context,
Throwable ex)
            throws Throwable {
        memoryDumpForFurtherInvestigation("Failure recorded during test setup");
        throw ex;
    }
    @Override
    public void handleAfterEachMethodExecutionException(ExtensionContext context,
Throwable ex)
            throws Throwable {
        memoryDumpForFurtherInvestigation("Failure recorded during test cleanup");
        throw ex;
    }
    @Override
    public void handleAfterAllMethodExecutionException(ExtensionContext context,
Throwable ex)
            throws Throwable {
        memoryDumpForFurtherInvestigation("Failure recorded during class cleanup");
        throw ex;
    }
}
Multiple execution exception handlers may be invoked for the same lifecycle method in order of
declaration. If one of the handlers swallows the handled exception, subsequent ones will not be
executed, and no failure will be propagated to JUnit engine, as if the exception was never thrown.
Handlers may also choose to rethrow the exception or throw a different one, potentially wrapping
the original.
Extensions implementing LifecycleMethodExecutionExceptionHandler that wish to handle exceptions
thrown during @BeforeAll or @AfterAll need to be registered on a class level, while handlers for
BeforeEach and AfterEach may be also registered for individual test methods.

Registering multiple exception handling extensions
// Register handlers for @Test, @BeforeEach, @AfterEach as well as @BeforeAll and
@AfterAll
@ExtendWith(ThirdExecutedHandler.class)
class MultipleHandlersTestCase {
    // Register handlers for @Test, @BeforeEach, @AfterEach only
    @ExtendWith(SecondExecutedHandler.class)
    @ExtendWith(FirstExecutedHandler.class)
    @Test
    void testMethod() {
    }
}
5.10. Intercepting Invocations
InvocationInterceptor defines the API for Extensions that wish to intercept calls to test code.
The following example shows an extension that executes all test methods in Swing’s Event Dispatch
Thread.
An extension that executes tests in a user-defined thread
public class SwingEdtInterceptor implements InvocationInterceptor {
    @Override
    public void interceptTestMethod(Invocation<Void> invocation,
            ReflectiveInvocationContext<Method> invocationContext,
            ExtensionContext extensionContext) throws Throwable {
        AtomicReference<Throwable> throwable = new AtomicReference<>();
        SwingUtilities.invokeAndWait(() -> {
            try {
                invocation.proceed();
            }
            catch (Throwable t) {
                throwable.set(t);
            }
        });
        Throwable t = throwable.get();
        if (t != null) {
            throw t;
        }
    }
}

5.11. Providing Invocation Contexts for Test Templates
A @TestTemplate method can only be executed when at least one
TestTemplateInvocationContextProvider is registered. Each such provider is responsible for
providing a Stream of TestTemplateInvocationContext instances. Each context may specify a custom
display name and a list of additional extensions that will only be used for the next invocation of the
@TestTemplate method.
The following example shows how to write a test template as well as how to register and implement
a TestTemplateInvocationContextProvider.
A test template with accompanying extension
final List<String> fruits = Arrays.asList("apple", "banana", "lemon");
@TestTemplate
@ExtendWith(MyTestTemplateInvocationContextProvider.class)
void testTemplate(String fruit) {
    assertTrue(fruits.contains(fruit));
}
public class MyTestTemplateInvocationContextProvider
        implements TestTemplateInvocationContextProvider {
    @Override
    public boolean supportsTestTemplate(ExtensionContext context) {
        return true;
    }
    @Override
    public Stream<TestTemplateInvocationContext>
provideTestTemplateInvocationContexts(
            ExtensionContext context) {
        return Stream.of(invocationContext("apple"), invocationContext("banana"));
    }
    private TestTemplateInvocationContext invocationContext(String parameter) {
        return new TestTemplateInvocationContext() {
            @Override
            public String getDisplayName(int invocationIndex) {
                return parameter;
            }
            @Override
            public List<Extension> getAdditionalExtensions() {
                return Collections.singletonList(new ParameterResolver() {
                    @Override
                    public boolean supportsParameter(ParameterContext
parameterContext,

ExtensionContext extensionContext) {
                        return parameterContext.getParameter().getType().equals(
String.class);
                    }
                    @Override
                    public Object resolveParameter(ParameterContext parameterContext,
                            ExtensionContext extensionContext) {
                        return parameter;
                    }
                });
            }
        };
    }
}
In this example, the test template will be invoked twice. The display names of the invocations will
be apple and banana as specified by the invocation context. Each invocation registers a custom
ParameterResolver which is used to resolve the method parameter. The output when using the
ConsoleLauncher is as follows.
└─ testTemplate(String) ✔
   ├─ apple ✔
   └─ banana ✔
The TestTemplateInvocationContextProvider extension API is primarily intended for implementing
different kinds of tests that rely on repetitive invocation of a test-like method albeit in different
contexts — for example, with different parameters, by preparing the test class instance differently,
or multiple times without modifying the context. Please refer to the implementations of Repeated
Tests or Parameterized Tests which use this extension point to provide their functionality.
5.12. Keeping State in Extensions
Usually, an extension is instantiated only once. So the question becomes relevant: How do you keep
the state from one invocation of an extension to the next? The ExtensionContext API provides a
Store exactly for this purpose. Extensions may put values into a store for later retrieval. See the
TimingExtension for an example of using the Store with a method-level scope. It is important to
remember that values stored in an ExtensionContext during test execution will not be available in
the surrounding ExtensionContext. Since ExtensionContexts may be nested, the scope of inner
contexts may also be limited. Consult the corresponding Javadoc for details on the methods
available for storing and retrieving values via the Store.

ExtensionContext.Store.CloseableResource
An extension context store is bound to its extension context lifecycle. When an
extension context lifecycle ends it closes its associated store. All stored values that
are instances of CloseableResource are notified by an invocation of their close()
method.

5.13. Supported Utilities in Extensions
The junit-platform-commons artifact exposes a package named org.junit.platform.commons.support
that contains maintained utility methods for working with annotations, classes, reflection, and
classpath scanning tasks. TestEngine and Extension authors are encouraged to use these supported
methods in order to align with the behavior of the JUnit Platform.
5.13.1. Annotation Support
AnnotationSupport provides static utility methods that operate on annotated elements (e.g.,
packages, annotations, classes, interfaces, constructors, methods, and fields). These include
methods to check whether an element is annotated or meta-annotated with a particular annotation,
to search for specific annotations, and to find annotated methods and fields in a class or interface.
Some of these methods search on implemented interfaces and within class hierarchies to find
annotations. Consult the Javadoc for AnnotationSupport for further details.
5.13.2. Class Support
ClassSupport provides static utility methods for working with classes (i.e., instances of
java.lang.Class). Consult the Javadoc for ClassSupport for further details.
5.13.3. Reflection Support
ReflectionSupport provides static utility methods that augment the standard JDK reflection and
class-loading mechanisms. These include methods to scan the classpath in search of classes
matching specified predicates, to load and create new instances of a class, and to find and invoke
methods. Some of these methods traverse class hierarchies to locate matching methods. Consult the
Javadoc for ReflectionSupport for further details.
5.13.4. Modifier Support
ModifierSupport provides static utility methods for working with member and class modifiers — for
example, to determine if a member is declared as public, private, abstract, static, etc. Consult the
Javadoc for ModifierSupport for further details.
5.14. Relative Execution Order of User Code and
Extensions
When executing a test class that contains one or more test methods, a number of extension
callbacks are called in addition to the user-supplied test and lifecycle methods.
 See also: Test Execution Order
5.14.1. User and Extension Code
The following diagram illustrates the relative order of user-supplied code and extension code. User-
supplied test and lifecycle methods are shown in orange, with callback code implemented by

extensions shown in blue. The grey box denotes the execution of a single test method and will be
repeated for every test method in the test class.
User code and extension code
The following table further explains the sixteen steps in the User code and extension code diagram.
St
ep
Interface/A
nnotation
Description
1 interface
org.junit.jup
iter.api.exte
nsion.BeforeA
llCallback
extension code executed before all tests of the container are executed
2 annotation
org.junit.jup
iter.api.Befo
reAll
user code executed before all tests of the container are executed

St
ep
Interface/A
nnotation
Description
3 interface
org.junit.jup
iter.api.exte
nsion.Lifecyc
leMethodExecu
tionException
Handler
#handleBefore
AllMethodExec
utionExceptio
n
extension code for handling exceptions thrown from @BeforeAll methods
4 interface
org.junit.jup
iter.api.exte
nsion.BeforeE
achCallback
extension code executed before each test is executed
5 annotation
org.junit.jup
iter.api.Befo
reEach
user code executed before each test is executed
6 interface
org.junit.jup
iter.api.exte
nsion.Lifecyc
leMethodExecu
tionException
Handler
#handleBefore
EachMethodExe
cutionExcepti
on
extension code for handling exceptions thrown from @BeforeEach methods
7 interface
org.junit.jup
iter.api.exte
nsion.BeforeT
estExecutionC
allback
extension code executed immediately before a test is executed
8 annotation
org.junit.jup
iter.api.Test
user code of the actual test method
9 interface
org.junit.jup
iter.api.exte
nsion.TestExe
cutionExcepti
onHandler
extension code for handling exceptions thrown during a test

St
ep
Interface/A
nnotation
Description
10 interface
org.junit.jup
iter.api.exte
nsion.AfterTe
stExecutionCa
llback
extension code executed immediately after test execution and its
corresponding exception handlers
11 annotation
org.junit.jup
iter.api.Afte
rEach
user code executed after each test is executed
12 interface
org.junit.jup
iter.api.exte
nsion.Lifecyc
leMethodExecu
tionException
Handler
#handleAfterE
achMethodExec
utionExceptio
n
extension code for handling exceptions thrown from @AfterEach methods
13 interface
org.junit.jup
iter.api.exte
nsion.AfterEa
chCallback
extension code executed after each test is executed
14 annotation
org.junit.jup
iter.api.Afte
rAll
user code executed after all tests of the container are executed
15 interface
org.junit.jup
iter.api.exte
nsion.Lifecyc
leMethodExecu
tionException
Handler
#handleAfterA
llMethodExecu
tionException
extension code for handling exceptions thrown from @AfterAll methods
16 interface
org.junit.jup
iter.api.exte
nsion.AfterAl
lCallback
extension code executed after all tests of the container are executed
In the simplest case only the actual test method will be executed (step 8); all other steps are optional
depending on the presence of user code or extension support for the corresponding lifecycle
callback. For further details on the various lifecycle callbacks please consult the respective Javadoc
for each annotation and extension.

All invocations of user code methods in the above table can additionally be intercepted by
implementing InvocationInterceptor.
5.14.2. Wrapping Behavior of Callbacks
JUnit Jupiter always guarantees wrapping behavior for multiple registered extensions that
implement lifecycle callbacks such as BeforeAllCallback, AfterAllCallback, BeforeEachCallback,
AfterEachCallback, BeforeTestExecutionCallback, and AfterTestExecutionCallback.
That means that, given two extensions Extension1 and Extension2 with Extension1 registered before
Extension2, any "before" callbacks implemented by Extension1 are guaranteed to execute before
any "before" callbacks implemented by Extension2. Similarly, given the two same two extensions
registered in the same order, any "after" callbacks implemented by Extension1 are guaranteed to
execute after any "after" callbacks implemented by Extension2. Extension1 is therefore said to wrap
Extension2.
JUnit Jupiter also guarantees wrapping behavior within class and interface hierarchies for user-
supplied lifecycle methods (see Test Classes and Methods).
• @BeforeAll methods are inherited from superclasses as long as they are not hidden or
overridden. Furthermore, @BeforeAll methods from superclasses will be executed before
@BeforeAll methods in subclasses.
◦ Similarly, @BeforeAll methods declared in an interface are inherited as long as they are not
hidden or overridden, and @BeforeAll methods from an interface will be executed before
@BeforeAll methods in the class that implements the interface.
• @AfterAll methods are inherited from superclasses as long as they are not hidden or overridden.
Furthermore, @AfterAll methods from superclasses will be executed after @AfterAll methods in
subclasses.
◦ Similarly, @AfterAll methods declared in an interface are inherited as long as they are not
hidden or overridden, and @AfterAll methods from an interface will be executed after
@AfterAll methods in the class that implements the interface.
• @BeforeEach methods are inherited from superclasses as long as they are not overridden.
Furthermore, @BeforeEach methods from superclasses will be executed before @BeforeEach
methods in subclasses.
◦ Similarly, @BeforeEach methods declared as interface default methods are inherited as long
as they are not overridden, and @BeforeEach default methods will be executed before
@BeforeEach methods in the class that implements the interface.
• @AfterEach methods are inherited from superclasses as long as they are not overridden.
Furthermore, @AfterEach methods from superclasses will be executed after @AfterEach methods
in subclasses.
◦ Similarly, @AfterEach methods declared as interface default methods are inherited as long as
they are not overridden, and @AfterEach default methods will be executed after @AfterEach
methods in the class that implements the interface.
The following examples demonstrate this behavior. Please note that the examples do not actually
do anything realistic. Instead, they mimic common scenarios for testing interactions with the

database. All methods imported statically from the Logger class simply log contextual information
in order to help us better understand the execution order of user-supplied callback methods and
callback methods in extensions.
Extension1
import static example.callbacks.Logger.afterEachCallback;
import static example.callbacks.Logger.beforeEachCallback;
import org.junit.jupiter.api.extension.AfterEachCallback;
import org.junit.jupiter.api.extension.BeforeEachCallback;
import org.junit.jupiter.api.extension.ExtensionContext;
public class Extension1 implements BeforeEachCallback, AfterEachCallback {
    @Override
    public void beforeEach(ExtensionContext context) {
        beforeEachCallback(this);
    }
    @Override
    public void afterEach(ExtensionContext context) {
        afterEachCallback(this);
    }
}
Extension2
import static example.callbacks.Logger.afterEachCallback;
import static example.callbacks.Logger.beforeEachCallback;
import org.junit.jupiter.api.extension.AfterEachCallback;
import org.junit.jupiter.api.extension.BeforeEachCallback;
import org.junit.jupiter.api.extension.ExtensionContext;
public class Extension2 implements BeforeEachCallback, AfterEachCallback {
    @Override
    public void beforeEach(ExtensionContext context) {
        beforeEachCallback(this);
    }
    @Override
    public void afterEach(ExtensionContext context) {
        afterEachCallback(this);
    }
}

AbstractDatabaseTests
import static example.callbacks.Logger.afterAllMethod;
import static example.callbacks.Logger.afterEachMethod;
import static example.callbacks.Logger.beforeAllMethod;
import static example.callbacks.Logger.beforeEachMethod;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
/**
 * Abstract base class for tests that use the database.
 */
abstract class AbstractDatabaseTests {
    @BeforeAll
    static void createDatabase() {
        beforeAllMethod(AbstractDatabaseTests.class.getSimpleName() +
".createDatabase()");
    }
    @BeforeEach
    void connectToDatabase() {
        beforeEachMethod(AbstractDatabaseTests.class.getSimpleName() +
".connectToDatabase()");
    }
    @AfterEach
    void disconnectFromDatabase() {
        afterEachMethod(AbstractDatabaseTests.class.getSimpleName() +
".disconnectFromDatabase()");
    }
    @AfterAll
    static void destroyDatabase() {
        afterAllMethod(AbstractDatabaseTests.class.getSimpleName() +
".destroyDatabase()");
    }
}

DatabaseTestsDemo
import static example.callbacks.Logger.afterEachMethod;
import static example.callbacks.Logger.beforeAllMethod;
import static example.callbacks.Logger.beforeEachMethod;
import static example.callbacks.Logger.testMethod;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
/**
 * Extension of {@link AbstractDatabaseTests} that inserts test data
 * into the database (after the database connection has been opened)
 * and deletes test data (before the database connection is closed).
 */
@ExtendWith({ Extension1.class, Extension2.class })
class DatabaseTestsDemo extends AbstractDatabaseTests {
    @BeforeAll
    static void beforeAll() {
        beforeAllMethod(DatabaseTestsDemo.class.getSimpleName() + ".beforeAll()");
    }
    @BeforeEach
    void insertTestDataIntoDatabase() {
        beforeEachMethod(getClass().getSimpleName() + ".insertTestDataIntoDatabase()"
);
    }
    @Test
    void testDatabaseFunctionality() {
        testMethod(getClass().getSimpleName() + ".testDatabaseFunctionality()");
    }
    @AfterEach
    void deleteTestDataFromDatabase() {
        afterEachMethod(getClass().getSimpleName() + ".deleteTestDataFromDatabase()");
    }
    @AfterAll
    static void afterAll() {
        beforeAllMethod(DatabaseTestsDemo.class.getSimpleName() + ".afterAll()");
    }
}

When the DatabaseTestsDemo test class is executed, the following is logged.
@BeforeAll AbstractDatabaseTests.createDatabase()
@BeforeAll DatabaseTestsDemo.beforeAll()
  Extension1.beforeEach()
  Extension2.beforeEach()
    @BeforeEach AbstractDatabaseTests.connectToDatabase()
    @BeforeEach DatabaseTestsDemo.insertTestDataIntoDatabase()
      @Test DatabaseTestsDemo.testDatabaseFunctionality()
    @AfterEach DatabaseTestsDemo.deleteTestDataFromDatabase()
    @AfterEach AbstractDatabaseTests.disconnectFromDatabase()
  Extension2.afterEach()
  Extension1.afterEach()
@BeforeAll DatabaseTestsDemo.afterAll()
@AfterAll AbstractDatabaseTests.destroyDatabase()
The following sequence diagram helps to shed further light on what actually goes on within the
JupiterTestEngine when the DatabaseTestsDemo test class is executed.

DatabaseTestsDemo
JUnit Jupiter does not guarantee the execution order of multiple lifecycle methods that are declared
within a single test class or test interface. It may at times appear that JUnit Jupiter invokes such
methods in alphabetical order. However, that is not precisely true. The ordering is analogous to the
ordering for @Test methods within a single test class.


Lifecycle methods that are declared within a single test class or test interface will
be ordered using an algorithm that is deterministic but intentionally non-obvious.
This ensures that subsequent runs of a test suite execute lifecycle methods in the
same order, thereby allowing for repeatable builds.
In addition, JUnit Jupiter does not support wrapping behavior for multiple lifecycle methods
declared within a single test class or test interface.
The following example demonstrates this behavior. Specifically, the lifecycle method configuration
is broken due to the order in which the locally declared lifecycle methods are executed.
• Test data is inserted before the database connection has been opened, which results in a failure
to connect to the database.
• The database connection is closed before deleting the test data, which results in a failure to
connect to the database.

BrokenLifecycleMethodConfigDemo
import static example.callbacks.Logger.afterEachMethod;
import static example.callbacks.Logger.beforeEachMethod;
import static example.callbacks.Logger.testMethod;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
/**
 * Example of "broken" lifecycle method configuration.
 *
 * <p>Test data is inserted before the database connection has been opened.
 *
 * <p>Database connection is closed before deleting test data.
 */
@ExtendWith({ Extension1.class, Extension2.class })
class BrokenLifecycleMethodConfigDemo {
    @BeforeEach
    void connectToDatabase() {
        beforeEachMethod(getClass().getSimpleName() + ".connectToDatabase()");
    }
    @BeforeEach
    void insertTestDataIntoDatabase() {
        beforeEachMethod(getClass().getSimpleName() + ".insertTestDataIntoDatabase()"
);
    }
    @Test
    void testDatabaseFunctionality() {
        testMethod(getClass().getSimpleName() + ".testDatabaseFunctionality()");
    }
    @AfterEach
    void deleteTestDataFromDatabase() {
        afterEachMethod(getClass().getSimpleName() + ".deleteTestDataFromDatabase()");
    }
    @AfterEach
    void disconnectFromDatabase() {
        afterEachMethod(getClass().getSimpleName() + ".disconnectFromDatabase()");
    }
}
When the BrokenLifecycleMethodConfigDemo test class is executed, the following is logged.

Extension1.beforeEach()
Extension2.beforeEach()
  @BeforeEach BrokenLifecycleMethodConfigDemo.insertTestDataIntoDatabase()
  @BeforeEach BrokenLifecycleMethodConfigDemo.connectToDatabase()
    @Test BrokenLifecycleMethodConfigDemo.testDatabaseFunctionality()
  @AfterEach BrokenLifecycleMethodConfigDemo.disconnectFromDatabase()
  @AfterEach BrokenLifecycleMethodConfigDemo.deleteTestDataFromDatabase()
Extension2.afterEach()
Extension1.afterEach()
The following sequence diagram helps to shed further light on what actually goes on within the
JupiterTestEngine when the BrokenLifecycleMethodConfigDemo test class is executed.
BrokenLifecycleMethodConfigDemo


Due to the aforementioned behavior, the JUnit Team recommends that developers
declare at most one of each type of lifecycle method (see Test Classes and Methods)
per test class or test interface unless there are no dependencies between such
lifecycle methods.
6. Advanced Topics
6.1. JUnit Platform Launcher API
One of the prominent goals of JUnit 5 is to make the interface between JUnit and its programmatic
clients – build tools and IDEs – more powerful and stable. The purpose is to decouple the internals
of discovering and executing tests from all the filtering and configuration that’s necessary from the
outside.
JUnit 5 introduces the concept of a Launcher that can be used to discover, filter, and execute tests.
Moreover, third party test libraries – like Spock, Cucumber, and FitNesse – can plug into the JUnit
Platform’s launching infrastructure by providing a custom TestEngine.
The launcher API is in the junit-platform-launcher module.
An example consumer of the launcher API is the ConsoleLauncher in the junit-platform-console
project.
6.1.1. Discovering Tests
Introducing test discovery as a dedicated feature of the platform itself will (hopefully) free IDEs and
build tools from most of the difficulties they had to go through to identify test classes and test
methods in the past.
Usage Example:

import static
org.junit.platform.engine.discovery.ClassNameFilter.includeClassNamePatterns;
import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;
import static org.junit.platform.engine.discovery.DiscoverySelectors.selectPackage;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.TestExecutionListener;
import org.junit.platform.launcher.TestPlan;
import org.junit.platform.launcher.core.LauncherConfig;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;
import org.junit.platform.launcher.listeners.TestExecutionSummary;
import org.junit.platform.reporting.legacy.xml.LegacyXmlReportGeneratingListener;
LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
    .selectors(
        selectPackage("com.example.mytests"),
        selectClass(MyTestClass.class)
    )
    .filters(
        includeClassNamePatterns(".*Tests")
    )
    .build();
Launcher launcher = LauncherFactory.create();
TestPlan testPlan = launcher.discover(request);
There’s currently the possibility to select classes, methods, and all classes in a package or even
search for all tests in the classpath. Discovery takes place across all participating test engines.
The resulting TestPlan is a hierarchical (and read-only) description of all engines, classes, and test
methods that fit the LauncherDiscoveryRequest. The client can traverse the tree, retrieve details
about a node, and get a link to the original source (like class, method, or file position). Every node in
the test plan has a unique ID that can be used to invoke a particular test or group of tests.
6.1.2. Executing Tests
To execute tests, clients can use the same LauncherDiscoveryRequest as in the discovery phase or
create a new request. Test progress and reporting can be achieved by registering one or more
TestExecutionListener implementations with the Launcher as in the following example.

LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
    .selectors(
        selectPackage("com.example.mytests"),
        selectClass(MyTestClass.class)
    )
    .filters(
        includeClassNamePatterns(".*Tests")
    )
    .build();
Launcher launcher = LauncherFactory.create();
// Register a listener of your choice
SummaryGeneratingListener listener = new SummaryGeneratingListener();
launcher.registerTestExecutionListeners(listener);
launcher.execute(request);
TestExecutionSummary summary = listener.getSummary();
// Do something with the TestExecutionSummary.
There is no return value for the execute() method, but you can easily use a listener to aggregate the
final results in an object of your own. For examples see the SummaryGeneratingListener and
LegacyXmlReportGeneratingListener.
6.1.3. Plugging in your own Test Engine
JUnit currently provides two TestEngine implementations.
• junit-jupiter-engine: The core of JUnit Jupiter.
• junit-vintage-engine: A thin layer on top of JUnit 4 to allow running vintage tests with the
launcher infrastructure.
Third parties may also contribute their own TestEngine by implementing the interfaces in the junit-
platform-engine module and registering their engine. By default, engine registration is supported
via Java’s java.util.ServiceLoader mechanism. For example, the junit-jupiter-engine module
registers its org.junit.jupiter.engine.JupiterTestEngine in a file named
org.junit.platform.engine.TestEngine within the /META-INF/services in the junit-jupiter-engine
JAR.

HierarchicalTestEngine is a convenient abstract base implementation (used by the
junit-jupiter-engine) that only requires implementors to provide the logic for test
discovery. It implements execution of TestDescriptors that implement the Node
interface, including support for parallel execution.


The junit- prefix is reserved for TestEngines from the JUnit Team
The JUnit Platform Launcher enforces that only TestEngine implementations
published by the JUnit Team may use the junit- prefix for their TestEngine IDs.
• If any third-party TestEngine claims to be junit-jupiter or junit-vintage, an
exception will be thrown, immediately halting execution of the JUnit Platform.
• If any third-party TestEngine uses the junit- prefix for its ID, a warning
message will be logged. Later releases of the JUnit Platform will throw an
exception for such violations.
6.1.4. Plugging in your own Test Execution Listener
In addition to the public Launcher API method for registering test execution listeners
programmatically, by default custom TestExecutionListener implementations will be discovered at
runtime via Java’s java.util.ServiceLoader mechanism and automatically registered with the
Launcher created via the LauncherFactory. For example, an example.TestInfoPrinter class
implementing TestExecutionListener and declared within the /META-
INF/services/org.junit.platform.launcher.TestExecutionListener file is loaded and registered
automatically.
6.1.5. JUnit Platform Reporting
The junit-platform-reporting artifact contains TestExecutionListener implementations that
generate test reports. These listeners are typically used by IDEs and build tools. The package
org.junit.platform.reporting.legacy.xml currently contains the following implementation.
• LegacyXmlReportGeneratingListener generates a separate XML report for each root in the
TestPlan. Note that the generated XML format is compatible with the de facto standard for JUnit
4 based test reports that was made popular by the Ant build system. The
LegacyXmlReportGeneratingListener is used by the Console Launcher as well.

The junit-platform-launcher module also contains TestExecutionListener
implementations that can be used for reporting purposes. See LoggingListener and
SummaryGeneratingListener for details.
6.1.6. Configuring the Launcher
If you require fine-grained control over automatic detection and registration of test engines and
test execution listeners, you may create an instance of LauncherConfig and supply that to the
LauncherFactory.create(LauncherConfig) method. Typically an instance of LauncherConfig is created
via the built-in fluent builder API, as demonstrated in the following example.

LauncherConfig launcherConfig = LauncherConfig.builder()
    .enableTestEngineAutoRegistration(false)
    .enableTestExecutionListenerAutoRegistration(false)
    .addTestEngines(new CustomTestEngine())
    .addTestExecutionListeners(new LegacyXmlReportGeneratingListener(reportsDir, out))
    .addTestExecutionListeners(new CustomTestExecutionListener())
    .build();
Launcher launcher = LauncherFactory.create(launcherConfig);
LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
    .selectors(selectPackage("com.example.mytests"))
    .build();
launcher.execute(request);
6.2. JUnit Platform Test Kit
The junit-platform-testkit artifact provides support for executing a test plan on the JUnit Platform
and then verifying the expected results. As of JUnit Platform 1.4, this support is limited to the
execution of a single TestEngine (see Engine Test Kit).

Although the Test Kit is currently an experimental feature, the JUnit Team invites
you to try it out and provide feedback to help improve the Test Kit APIs and
eventually promote this feature.
6.2.1. Engine Test Kit
The org.junit.platform.testkit.engine package provides support for executing a TestPlan for a
given TestEngine running on the JUnit Platform and then accessing the results via a fluent API to
verify the expected results. The key entry point into this API is the EngineTestKit which provides
static factory methods named engine() and execute(). It is recommended that you select one of the
engine() variants to benefit from the fluent API for building an EngineDiscoveryRequest.

If you prefer to use the LauncherDiscoveryRequestBuilder from the Launcher API to
build your EngineDiscoveryRequest, you must use one of the execute() variants in
EngineTestKit.
The following test class written using JUnit Jupiter will be used in subsequent examples.

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assumptions.assumeTrue;
import example.util.Calculator;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
@TestMethodOrder(OrderAnnotation.class)
public class ExampleTestCase {
    private final Calculator calculator = new Calculator();
    @Test
    @Disabled("for demonstration purposes")
    @Order(1)
    void skippedTest() {
        // skipped ...
    }
    @Test
    @Order(2)
    void succeedingTest() {
        assertEquals(42, calculator.multiply(6, 7));
    }
    @Test
    @Order(3)
    void abortedTest() {
        assumeTrue("abc".contains("Z"), "abc does not contain Z");
        // aborted ...
    }
    @Test
    @Order(4)
    void failingTest() {
        // The following throws an ArithmeticException: "/ by zero"
        calculator.divide(1, 0);
    }
}
For the sake of brevity, the following sections demonstrate how to test JUnit’s own
JupiterTestEngine whose unique engine ID is "junit-jupiter". If you want to test your own
TestEngine implementation, you need to use its unique engine ID. Alternatively, you may test your
own TestEngine by supplying an instance of it to the EngineTestKit.engine(TestEngine) static factory

method.
6.2.2. Asserting Statistics
One of the most common features of the Test Kit is the ability to assert statistics against events fired
during the execution of a TestPlan. The following tests demonstrate how to assert statistics for
containers and tests in the JUnit Jupiter TestEngine. For details on what statistics are available,
consult the Javadoc for EventStatistics.
import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;
import example.ExampleTestCase;
import org.junit.jupiter.api.Test;
import org.junit.platform.testkit.engine.EngineTestKit;
class EngineTestKitStatisticsDemo {
    @Test
    void verifyJupiterContainerStats() {
        EngineTestKit
            .engine("junit-jupiter") ①
            .selectors(selectClass(ExampleTestCase.class)) ②
            .execute() ③
            .containers() ④
            .assertStatistics(stats -> stats.started(2).succeeded(2)); ⑤
    }
    @Test
    void verifyJupiterTestStats() {
        EngineTestKit
            .engine("junit-jupiter") ①
            .selectors(selectClass(ExampleTestCase.class)) ②
            .execute() ③
            .tests() ⑥
            .assertStatistics(stats ->
                stats.skipped(1).started(3).succeeded(1).aborted(1).failed(1)); ⑦
    }
}
① Select the JUnit Jupiter TestEngine.
② Select the ExampleTestCase test class.
③ Execute the TestPlan.
④ Filter by container events.
⑤ Assert statistics for container events.
⑥ Filter by test events.

⑦ Assert statistics for test events.

In the verifyJupiterContainerStats() test method, the counts for the started and
succeeded statistics are 2 since the JupiterTestEngine and the ExampleTestCase class
are both considered containers.
6.2.3. Asserting Events
If you find that asserting statistics alone is insufficient for verifying the expected behavior of test
execution, you can work directly with the recorded Event elements and perform assertions against
them.
For example, if you want to verify the reason that the skippedTest() method in ExampleTestCase was
skipped, you can do that as follows.

The assertThatEvents() method in the following example is a shortcut for
org.assertj.core.api.Assertions.assertThat(events.list()) from the AssertJ
assertion library.
For details on what conditions are available for use with AssertJ assertions against
events, consult the Javadoc for EventConditions.

import static org.junit.platform.engine.discovery.DiscoverySelectors.selectMethod;
import static org.junit.platform.testkit.engine.EventConditions.event;
import static org.junit.platform.testkit.engine.EventConditions.skippedWithReason;
import static org.junit.platform.testkit.engine.EventConditions.test;
import example.ExampleTestCase;
import org.junit.jupiter.api.Test;
import org.junit.platform.testkit.engine.EngineTestKit;
import org.junit.platform.testkit.engine.Events;
class EngineTestKitSkippedMethodDemo {
    @Test
    void verifyJupiterMethodWasSkipped() {
        String methodName = "skippedTest";
        Events testEvents = EngineTestKit ⑤
            .engine("junit-jupiter") ①
            .selectors(selectMethod(ExampleTestCase.class, methodName)) ②
            .execute() ③
            .tests(); ④
        testEvents.assertStatistics(stats -> stats.skipped(1)); ⑥
        testEvents.assertThatEvents() ⑦
            .haveExactly(1, event(test(methodName),
                skippedWithReason("for demonstration purposes")));
    }
}
① Select the JUnit Jupiter TestEngine.
② Select the skippedTest() method in the ExampleTestCase test class.
③ Execute the TestPlan.
④ Filter by test events.
⑤ Save the test Events to a local variable.
⑥ Optionally assert the expected statistics.
⑦ Assert that the recorded test events contain exactly one skipped test named skippedTest with
"for demonstration purposes" as the reason.
If you want to verify the type of exception thrown from the failingTest() method in
ExampleTestCase, you can do that as follows.


For details on what conditions are available for use with AssertJ assertions against
events and execution results, consult the Javadoc for EventConditions and
TestExecutionResultConditions, respectively.
import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;
import static org.junit.platform.testkit.engine.EventConditions.event;
import static org.junit.platform.testkit.engine.EventConditions.finishedWithFailure;
import static org.junit.platform.testkit.engine.EventConditions.test;
import static
org.junit.platform.testkit.engine.TestExecutionResultConditions.instanceOf;
import static org.junit.platform.testkit.engine.TestExecutionResultConditions.message;
import example.ExampleTestCase;
import org.junit.jupiter.api.Test;
import org.junit.platform.testkit.engine.EngineTestKit;
class EngineTestKitFailedMethodDemo {
    @Test
    void verifyJupiterMethodFailed() {
        EngineTestKit.engine("junit-jupiter") ①
            .selectors(selectClass(ExampleTestCase.class)) ②
            .execute() ③
            .tests() ④
            .assertThatEvents().haveExactly(1, ⑤
                event(test("failingTest"),
                    finishedWithFailure(
                        instanceOf(ArithmeticException.class), message("/ by zero")))
);
    }
}
① Select the JUnit Jupiter TestEngine.
② Select the ExampleTestCase test class.
③ Execute the TestPlan.
④ Filter by test events.
⑤ Assert that the recorded test events contain exactly one failing test named failingTest with an
exception of type ArithmeticException and an error message equal to "/ by zero".
Although typically unnecessary, there are times when you need to verify all of the events fired
during the execution of a TestPlan. The following test demonstrates how to achieve this via the
assertEventsMatchExactly() method in the EngineTestKit API.


Since assertEventsMatchExactly() matches conditions exactly in the order in which
the events were fired, ExampleTestCase has been annotated with
@TestMethodOrder(OrderAnnotation.class) and each test method has been
annotated with @Order(…). This allows us to enforce the order in which the test
methods are executed, which in turn allows our verifyAllJupiterEvents() test to
be reliable.
import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;
import static org.junit.platform.testkit.engine.EventConditions.abortedWithReason;
import static org.junit.platform.testkit.engine.EventConditions.container;
import static org.junit.platform.testkit.engine.EventConditions.engine;
import static org.junit.platform.testkit.engine.EventConditions.event;
import static org.junit.platform.testkit.engine.EventConditions.finishedSuccessfully;
import static org.junit.platform.testkit.engine.EventConditions.finishedWithFailure;
import static org.junit.platform.testkit.engine.EventConditions.skippedWithReason;
import static org.junit.platform.testkit.engine.EventConditions.started;
import static org.junit.platform.testkit.engine.EventConditions.test;
import static
org.junit.platform.testkit.engine.TestExecutionResultConditions.instanceOf;
import static org.junit.platform.testkit.engine.TestExecutionResultConditions.message;
import java.io.StringWriter;
import java.io.Writer;
import example.ExampleTestCase;
import org.junit.jupiter.api.Test;
import org.junit.platform.testkit.engine.EngineTestKit;
import org.opentest4j.TestAbortedException;
class EngineTestKitAllEventsDemo {
    @Test
    void verifyAllJupiterEvents() {
        Writer writer = // create a java.io.Writer for debug output
        EngineTestKit.engine("junit-jupiter") ①
            .selectors(selectClass(ExampleTestCase.class)) ②
            .execute() ③
            .all() ④
            .debug(writer) ⑤
            .assertEventsMatchExactly( ⑥
                event(engine(), started()),
                event(container(ExampleTestCase.class), started()),
                event(test("skippedTest"), skippedWithReason("for demonstration
purposes")),
                event(test("succeedingTest"), started()),
                event(test("succeedingTest"), finishedSuccessfully()),
                event(test("abortedTest"), started()),

event(test("abortedTest"),
                    abortedWithReason(instanceOf(TestAbortedException.class),
                        message(m -> m.contains("abc does not contain Z")))),
                event(test("failingTest"), started()),
                event(test("failingTest"), finishedWithFailure(
                    instanceOf(ArithmeticException.class), message("/ by zero"))),
                event(container(ExampleTestCase.class), finishedSuccessfully()),
                event(engine(), finishedSuccessfully()));
    }
}
① Select the JUnit Jupiter TestEngine.
② Select the ExampleTestCase test class.
③ Execute the TestPlan.
④ Filter by all events.
⑤ Print all events to the supplied writer for debugging purposes. Debug information can also be
written to an OutputStream such as System.out or System.err.
⑥ Assert all events in exactly the order in which they were fired by the test engine.
The debug() invocation from the preceding example results in output similar to the following.

All Events:
    Event [type = STARTED, testDescriptor = JupiterEngineDescriptor: [engine:junit-
jupiter], timestamp = 2018-12-14T12:45:14.082280Z, payload = null]
    Event [type = STARTED, testDescriptor = ClassTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase], timestamp = 2018-12-14T12:45:14.089339Z,
payload = null]
    Event [type = SKIPPED, testDescriptor = TestMethodTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase]/[method:skippedTest()], timestamp = 2018-12-
14T12:45:14.094314Z, payload = 'for demonstration purposes']
    Event [type = STARTED, testDescriptor = TestMethodTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase]/[method:succeedingTest()], timestamp = 2018-
12-14T12:45:14.095182Z, payload = null]
    Event [type = FINISHED, testDescriptor = TestMethodTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase]/[method:succeedingTest()], timestamp = 2018-
12-14T12:45:14.104922Z, payload = TestExecutionResult [status = SUCCESSFUL, throwable
= null]]
    Event [type = STARTED, testDescriptor = TestMethodTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase]/[method:abortedTest()], timestamp = 2018-12-
14T12:45:14.106121Z, payload = null]
    Event [type = FINISHED, testDescriptor = TestMethodTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase]/[method:abortedTest()], timestamp = 2018-12-
14T12:45:14.109956Z, payload = TestExecutionResult [status = ABORTED, throwable =
org.opentest4j.TestAbortedException: Assumption failed: abc does not contain Z]]
    Event [type = STARTED, testDescriptor = TestMethodTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase]/[method:failingTest()], timestamp = 2018-12-
14T12:45:14.110680Z, payload = null]
    Event [type = FINISHED, testDescriptor = TestMethodTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase]/[method:failingTest()], timestamp = 2018-12-
14T12:45:14.111217Z, payload = TestExecutionResult [status = FAILED, throwable =
java.lang.ArithmeticException: / by zero]]
    Event [type = FINISHED, testDescriptor = ClassTestDescriptor: [engine:junit-
jupiter]/[class:example.ExampleTestCase], timestamp = 2018-12-14T12:45:14.113731Z,
payload = TestExecutionResult [status = SUCCESSFUL, throwable = null]]
    Event [type = FINISHED, testDescriptor = JupiterEngineDescriptor: [engine:junit-
jupiter], timestamp = 2018-12-14T12:45:14.113806Z, payload = TestExecutionResult
[status = SUCCESSFUL, throwable = null]]
7. API Evolution
One of the major goals of JUnit 5 is to improve maintainers' capabilities to evolve JUnit despite its
being used in many projects. With JUnit 4 a lot of stuff that was originally added as an internal
construct only got used by external extension writers and tool builders. That made changing JUnit 4
especially difficult and sometimes impossible.
That’s why JUnit 5 introduces a defined lifecycle for all publicly available interfaces, classes, and
methods.

7.1. API Version and Status
Every published artifact has a version number <major>.<minor>.<patch>, and all publicly available
interfaces, classes, and methods are annotated with @API from the @API Guardian  project. The
annotation’s status attribute can be assigned one of the following values.
Status Description
INTERNAL Must not be used by any code other than JUnit itself. Might be removed
without prior notice.
DEPRECATED Should no longer be used; might disappear in the next minor release.
EXPERIMENTAL Intended for new, experimental features where we are looking for feedback.
Use this element with caution; it might be promoted to MAINTAINED or STABLE in
the future, but might also be removed without prior notice, even in a patch.
MAINTAINED Intended for features that will not be changed in a backwards- incompatible
way for at least the next minor release of the current major version. If
scheduled for removal, it will be demoted to DEPRECATED first.
STABLE Intended for features that will not be changed in a backwards- incompatible
way in the current major version (5.*).
If the @API annotation is present on a type, it is considered to be applicable for all public members
of that type as well. A member is allowed to declare a different status value of lower stability.
7.2. Experimental APIs
The following table lists which APIs are currently designated as experimental via @API(status =
EXPERIMENTAL). Caution should be taken when relying on such APIs.
Package Name Type Name Since
org.junit.jupiter.api AssertionsKt (class) 5.1
org.junit.jupiter.api DisplayNameGeneration
(annotation)
5.4
org.junit.jupiter.api DisplayNameGenerator (interface) 5.4
org.junit.jupiter.api MethodDescriptor (interface) 5.4
org.junit.jupiter.api MethodOrderer (interface) 5.4
org.junit.jupiter.api MethodOrdererContext (interface) 5.4
org.junit.jupiter.api Order (annotation) 5.4
org.junit.jupiter.api TestMethodOrder (annotation) 5.4
org.junit.jupiter.api Timeout (annotation) 5.5
org.junit.jupiter.api.extensio
n
InvocationInterceptor
(interface)
5.5

Package Name Type Name Since
org.junit.jupiter.api.extensio
n
Invocation (interface) 5.5
org.junit.jupiter.api.extensio
n
LifecycleMethodExecutionExcept
ionHandler (interface)
5.5
org.junit.jupiter.api.extensio
n
ReflectiveInvocationContext
(interface)
5.5
org.junit.jupiter.api.extensio
n
ScriptEvaluationException
(class)
5.1
org.junit.jupiter.api.extensio
n
TestInstanceFactory (interface) 5.3
org.junit.jupiter.api.extensio
n
TestInstanceFactoryContext
(interface)
5.3
org.junit.jupiter.api.extensio
n
TestInstances (interface) 5.4
org.junit.jupiter.api.extensio
n
TestInstantiationException
(class)
5.3
org.junit.jupiter.api.extensio
n
TestWatcher (interface) 5.4
org.junit.jupiter.api.io TempDir (annotation) 5.4
org.junit.jupiter.api.parallel Execution (annotation) 5.3
org.junit.jupiter.api.parallel ExecutionMode (enum) 5.3
org.junit.jupiter.api.parallel ResourceAccessMode (enum) 5.3
org.junit.jupiter.api.parallel ResourceLock (annotation) 5.3
org.junit.jupiter.api.parallel ResourceLocks (annotation) 5.3
org.junit.jupiter.api.parallel Resources (class) 5.3
org.junit.jupiter.migrationsup
port
EnableJUnit4MigrationSupport
(annotation)
5.4
org.junit.jupiter.migrationsup
port.conditions
IgnoreCondition (class) 5.4
org.junit.jupiter.migrationsup
port.rules
EnableRuleMigrationSupport
(annotation)
5.0
org.junit.jupiter.migrationsup
port.rules
ExpectedExceptionSupport (class) 5.0
org.junit.jupiter.migrationsup
port.rules
ExternalResourceSupport (class) 5.0
org.junit.jupiter.migrationsup
port.rules
VerifierSupport (class) 5.0
org.junit.jupiter.params ParameterizedTest (annotation) 5.0
org.junit.jupiter.params.aggre
gator
AggregateWith (annotation) 5.2

Package Name Type Name Since
org.junit.jupiter.params.aggre
gator
ArgumentAccessException (class) 5.2
org.junit.jupiter.params.aggre
gator
ArgumentsAccessor (interface) 5.2
org.junit.jupiter.params.aggre
gator
ArgumentsAggregationException
(class)
5.2
org.junit.jupiter.params.aggre
gator
ArgumentsAggregator (interface) 5.2
org.junit.jupiter.params.conve
rter
ArgumentConversionException
(class)
5.0
org.junit.jupiter.params.conve
rter
ArgumentConverter (interface) 5.0
org.junit.jupiter.params.conve
rter
ConvertWith (annotation) 5.0
org.junit.jupiter.params.conve
rter
JavaTimeConversionPattern
(annotation)
5.0
org.junit.jupiter.params.conve
rter
SimpleArgumentConverter (class) 5.0
org.junit.jupiter.params.provi
der
Arguments (interface) 5.0
org.junit.jupiter.params.provi
der
ArgumentsProvider (interface) 5.0
org.junit.jupiter.params.provi
der
ArgumentsSource (annotation) 5.0
org.junit.jupiter.params.provi
der
ArgumentsSources (annotation) 5.0
org.junit.jupiter.params.provi
der
CsvFileSource (annotation) 5.0
org.junit.jupiter.params.provi
der
CsvParsingException (class) 5.3
org.junit.jupiter.params.provi
der
CsvSource (annotation) 5.0
org.junit.jupiter.params.provi
der
EmptySource (annotation) 5.4
org.junit.jupiter.params.provi
der
EnumSource (annotation) 5.0
org.junit.jupiter.params.provi
der
MethodSource (annotation) 5.0
org.junit.jupiter.params.provi
der
NullAndEmptySource (annotation) 5.4
org.junit.jupiter.params.provi
der
NullSource (annotation) 5.4
org.junit.jupiter.params.provi
der
ValueSource (annotation) 5.0

Package Name Type Name Since
org.junit.jupiter.params.suppo
rt
AnnotationConsumer (interface) 5.0
org.junit.platform.engine.supp
ort.config
PrefixedConfigurationParameter
s (class)
1.3
org.junit.platform.engine.supp
ort.discovery
EngineDiscoveryRequestResolver
(class)
1.5
org.junit.platform.engine.supp
ort.discovery
Builder (class) 1.5
org.junit.platform.engine.supp
ort.discovery
InitializationContext
(interface)
1.5
org.junit.platform.engine.supp
ort.discovery
SelectorResolver (interface) 1.5
org.junit.platform.engine.supp
ort.discovery
Context (interface) 1.5
org.junit.platform.engine.supp
ort.discovery
Match (class) 1.5
org.junit.platform.engine.supp
ort.discovery
Resolution (class) 1.5
org.junit.platform.engine.supp
ort.hierarchical
DefaultParallelExecutionConfig
urationStrategy (enum)
1.3
org.junit.platform.engine.supp
ort.hierarchical
ExclusiveResource (class) 1.3
org.junit.platform.engine.supp
ort.hierarchical
ForkJoinPoolHierarchicalTestEx
ecutorService (class)
1.3
org.junit.platform.engine.supp
ort.hierarchical
HierarchicalTestExecutorServic
e (interface)
1.3
org.junit.platform.engine.supp
ort.hierarchical
ExecutionMode (enum) 1.3
org.junit.platform.engine.supp
ort.hierarchical
Invocation (interface) 1.4
org.junit.platform.engine.supp
ort.hierarchical
ParallelExecutionConfiguration
(interface)
1.3
org.junit.platform.engine.supp
ort.hierarchical
ParallelExecutionConfiguration
Strategy (interface)
1.3
org.junit.platform.engine.supp
ort.hierarchical
ResourceLock (interface) 1.3
org.junit.platform.engine.supp
ort.hierarchical
SameThreadHierarchicalTestExec
utorService (class)
1.3
org.junit.platform.launcher LauncherConstants (class) 1.3
org.junit.platform.launcher.co
re
LauncherConfig (interface) 1.3
org.junit.platform.reporting.l
egacy.xml
LegacyXmlReportGeneratingListe
ner (class)
1.4

Package Name Type Name Since
org.junit.platform.testkit.eng
ine
EngineExecutionResults (class) 1.4
org.junit.platform.testkit.eng
ine
EngineTestKit (class) 1.4
org.junit.platform.testkit.eng
ine
Event (class) 1.4
org.junit.platform.testkit.eng
ine
EventConditions (class) 1.4
org.junit.platform.testkit.eng
ine
EventStatistics (class) 1.4
org.junit.platform.testkit.eng
ine
EventType (enum) 1.4
org.junit.platform.testkit.eng
ine
Events (class) 1.4
org.junit.platform.testkit.eng
ine
Execution (class) 1.4
org.junit.platform.testkit.eng
ine
Executions (class) 1.4
org.junit.platform.testkit.eng
ine
TerminationInfo (class) 1.4
org.junit.platform.testkit.eng
ine
TestExecutionResultConditions
(class)
1.4
7.3. Deprecated APIs
The following table lists which APIs are currently designated as deprecated via @API(status =
DEPRECATED). You should avoid using deprecated APIs whenever possible, since such APIs will likely
be removed in an upcoming release.
Package Name Type Name Since
org.junit.jupiter.api.conditio
n
DisabledIf (annotation) 5.5
org.junit.jupiter.api.conditio
n
EnabledIf (annotation) 5.5
org.junit.platform.commons.uti
l
PreconditionViolationException
(class)
1.5
org.junit.platform.engine.supp
ort.filter
ClasspathScanningSupport (class) 1.5
org.junit.platform.engine.supp
ort.hierarchical
SingleTestExecutor (class) 1.2
7.4. @API Tooling Support
The @API Guardian project plans to provide tooling support for publishers and consumers of APIs

annotated with @API. For example, the tooling support will likely provide a means to check if JUnit
APIs are being used in accordance with @API annotation declarations.
8. Contributors
Browse the current list of contributors directly on GitHub.
9. Release Notes
The release notes are available here.
10. Appendix
10.1. Dependency Metadata
Artifacts for final releases and milestones are deployed to Maven Central, and snapshot artifacts
are deployed to Sonatype’s snapshots repository under /org/junit.
10.1.1. JUnit Platform
• Group ID: org.junit.platform
• Version: 1.5.0
• Artifact IDs:
junit-platform-commons
Common APIs and support utilities for the JUnit Platform. Any API annotated with
@API(status = INTERNAL) is intended solely for usage within the JUnit framework itself. Any
usage of internal APIs by external parties is not supported!
junit-platform-console
Support for discovering and executing tests on the JUnit Platform from the console. See
Console Launcher for details.
junit-platform-console-standalone
An executable JAR with all dependencies included is provided in Maven Central under the
junit-platform-console-standalone directory. See Console Launcher for details.
junit-platform-engine
Public API for test engines. See Plugging in your own Test Engine for details.
junit-platform-launcher
Public API for configuring and launching test plans — typically used by IDEs and build tools.
See JUnit Platform Launcher API for details.
junit-platform-reporting
TestExecutionListener implementations that generate test reports — typically used by IDEs

and build tools. See JUnit Platform Reporting for details.
junit-platform-runner
Runner for executing tests and test suites on the JUnit Platform in a JUnit 4 environment. See
Using JUnit 4 to run the JUnit Platform for details.
junit-platform-suite-api
Annotations for configuring test suites on the JUnit Platform. Supported by the JUnitPlatform
runner and possibly by third-party TestEngine implementations.
junit-platform-testkit
Provides support for executing a test plan for a given TestEngine and then accessing the
results via a fluent API to verify the expected results.
10.1.2. JUnit Jupiter
• Group ID: org.junit.jupiter
• Version: 5.5.0
• Artifact IDs:
junit-jupiter
JUnit Jupiter aggregator artifact that transitively pulls in dependencies on junit-jupiter-api,
junit-jupiter-params, and junit-jupiter-engine for simplified dependency management in
build tools such as Gradle and Maven.
junit-jupiter-api
JUnit Jupiter API for writing tests and extensions.
junit-jupiter-engine
JUnit Jupiter test engine implementation; only required at runtime.
junit-jupiter-params
Support for parameterized tests in JUnit Jupiter.
junit-jupiter-migrationsupport
Support for migrating from JUnit 4 to JUnit Jupiter; only required for support for JUnit 4’s
@Ignore annotation and for running selected JUnit 4 rules.
10.1.3. JUnit Vintage
• Group ID: org.junit.vintage
• Version: 5.5.0
• Artifact ID:
junit-vintage-engine
JUnit Vintage test engine implementation that allows one to run vintage JUnit tests on the
JUnit Platform. Vintage tests include those written using JUnit 3 or JUnit 4 APIs or tests
written using testing frameworks built on those APIs.

10.1.4. Bill of Materials (BOM)
The Bill of Materials  POM provided under the following Maven coordinates can be used to ease
dependency management when referencing multiple of the above artifacts using Maven or Gradle.
• Group ID: org.junit
• Artifact ID: junit-bom
• Version: 5.5.0
10.1.5. Dependencies
Most of the above artifacts have a dependency in their published Maven POMs on the following
@API Guardian JAR.
• Group ID: org.apiguardian
• Artifact ID: apiguardian-api
• Version: 1.1.0
In addition, most of the above artifacts have a direct or transitive dependency on the following
OpenTest4J JAR.
• Group ID: org.opentest4j
• Artifact ID: opentest4j
• Version: 1.2.0
10.2. Dependency Diagram
org.junit.jupiter
org.junit.vintage
org.junit.platform
org.opentest4j
org.apiguardian
junit-jupiter
junit-jupiter-api
junit-jupiter-enginejunit-jupiter-paramsjunit-jupiter-migrationsupportjunit-vintage-engine
junit:junit
junit-platform-commons
junit-platform-console
junit-platform-engine
junit-platform-launcher
junit-platform-reportingjunit-platform-runner
junit-platform-suite-api
junit-platform-testkit
opentest4j
apiguardian-api
All artifacts exceptopentest4j and junit:junithave a dependency on thisartifact. The edges havebeen omitted from thisdiagram for the sake ofreadability.

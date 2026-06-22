const target = require('./source_under_test');

// TC-001: normalizeLabel trims và chuyển về chữ thường
test('TC-001 normalizeLabel trims and lowercases a regular string', () => {
  const result = target.normalizeLabel('  HeLLo WoRLd  ');
  expect(result).toBe('hello world');
});

// TC-002: normalizeLabel với chuỗi rỗng
test('TC-002 normalizeLabel with empty string', () => {
  const result = target.normalizeLabel('   ');
  expect(result).toBe('');
});

// TC-005: calculateDiscount VIP không đạt ngưỡng cap
test('TC-005 calculateDiscount VIP tier without cap', () => {
  const result = target.calculateDiscount(200, 'VIP');
  // 200 * 0.12 = 24, dưới cap 50 → roundMoney(24) = 24
  expect(result).toBe(24);
});

// TC-006: calculateDiscount VIP đạt ngưỡng cap
test('TC-006 calculateDiscount VIP tier with cap applied', () => {
  const result = target.calculateDiscount(600, 'vip');
  // 600 * 0.12 = 72, vượt cap 50 → min = 50 → roundMoney(50) = 50
  expect(result).toBe(50);
});

// TC-007: calculateDiscount Loyal không đạt ngưỡng cap
test('TC-007 calculateDiscount Loyal tier without cap', () => {
  const result = target.calculateDiscount(200, 'LoYaL');
  // 200 * 0.07 = 14, dưới cap 30 → roundMoney(14) = 14
  expect(result).toBe(14);
});

// TC-008: calculateDiscount Loyal đạt ngưỡng cap
test('TC-008 calculateDiscount Loyal tier with cap applied', () => {
  const result = target.calculateDiscount(500, 'loyal');
  // 500 * 0.07 = 35, vượt cap 30 → min = 30 → roundMoney(30) = 30
  expect(result).toBe(30);
});

// TC-009: calculateDiscount Standard luôn trả 0
test('TC-009 calculateDiscount Standard tier returns zero', () => {
  const result = target.calculateDiscount(150, 'standard');
  expect(result).toBe(0);
});

// TC-010: calculateDiscount ném lỗi khi tier không hỗ trợ
test('TC-010 calculateDiscount throws error for unsupported tier', () => {
  expect(() => target.calculateDiscount(100, 'gold')).toThrow(Error);
});

// TC-011: calculateDiscount ném lỗi khi subtotal âm
test('TC-011 calculateDiscount throws error for negative subtotal', () => {
  expect(() => target.calculateDiscount(-10, 'vip')).toThrow(Error);
});

// TC-012: shippingFee domestic, non‑fragile, weight <=5kg
test('TC-012 shippingFee normal domestic non-fragile weight <=5kg', () => {
  const fee = target.shippingFee(4, 'Domestic', false);
  // base fee domestic = 5, không surcharge, không fragile → roundMoney(5) = 5
  expect(fee).toBe(5);
});

// TC-013: shippingFee weight >5kg và <=20kg thêm surcharge
test('TC-013 shippingFee weight >5kg and <=20kg adds surcharge', () => {
  const fee = target.shippingFee(10, 'domestic', false);
  // base 5 + 10 surcharge = 15 → roundMoney(15) = 15
  expect(fee).toBe(15);
});

// TC-014: shippingFee weight >20kg áp dụng surcharge nặng
test('TC-014 shippingFee weight >20kg applies heavy-weight surcharge', () => {
  const fee = target.shippingFee(25, 'international', false);
  // base international 18 + 25 surcharge = 43 → roundMoney(43) = 43
  expect(fee).toBe(43);
});

// TC-015: shippingFee ném lỗi khi weight <= 0
test('TC-015 shippingFee throws error for zero or negative weight', () => {
  expect(() => target.shippingFee(0, 'domestic', false)).toThrow(Error);
});

// TC-016: shippingFee ném lỗi khi destination không hỗ trợ
test('TC-016 shippingFee throws error for unsupported destination', () => {
  expect(() => target.shippingFee(5, 'moon', false)).toThrow(Error);
});

// TC-017: finalTotal tính đúng với store credit dương
test('TC-017 finalTotal calculates correctly with positive store credit', () => {
  const order = {
    subtotal: 200,
    customerTier: 'vip',
    weightKg: 4,
    destination: 'domestic',
    fragile: false,
    storeCredit: 20,
  };
  // discount = 24 (VIP), shippingFee = 5, subtotal after discount+shipping = 200 - 24 + 5 = 181
  // final = roundMoney(max(181 - 20, 0)) = roundMoney(161) = 161
  const result = target.finalTotal(order);
  expect(result).toBe(161);
});

// TC-018: finalTotal ném lỗi khi storeCredit âm
test('TC-018 finalTotal throws error when storeCredit is negative', () => {
  const order = {
    subtotal: 100,
    customerTier: 'standard',
    weightKg: 2,
    destination: 'domestic',
    fragile: false,
    storeCredit: -5,
  };
  expect(() => target.finalTotal(order)).toThrow(Error);
});

// TC-019: finalTotal không bao giờ trả giá trị âm (floor at 0)
test('TC-019 finalTotal never returns negative value (floored at 0)', () => {
  const order = {
    subtotal: 10,
    customerTier: 'standard',
    weightKg: 1,
    destination: 'domestic',
    fragile: false,
    storeCredit: 50, // credit lớn hơn subtotal + shipping
  };
  // discount = 0, shippingFee = 5, subtotal = 10 + 5 = 15, 15 - 50 = -35 → floor to 0
  const result = target.finalTotal(order);
  expect(result).toBe(0);
});
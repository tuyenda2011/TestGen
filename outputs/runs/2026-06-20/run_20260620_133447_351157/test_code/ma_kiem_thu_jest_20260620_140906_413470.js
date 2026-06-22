const target = require('./source_under_test');

// Plan: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, TC-025, TC-026

describe('normalizeLabel', () => {
  // TC-001: Kiểm tra hàm normalizeLabel cắt khoảng trắng và chuyển về chữ thường
  test('TC-001 should trim whitespace and convert to lowercase', () => {
    // Input: '  VIP  ' -> trim() -> 'VIP' -> toLowerCase() -> 'vip'
    expect(target.normalizeLabel('  VIP  ')).toBe('vip');
  });

  // TC-002: Kiểm tra hàm normalizeLabel xử lý chuỗi rỗng và chuỗi đã chuẩn hóa
  test('TC-002 should handle empty string and already normalized input', () => {
    // Input: '' -> trim() -> '' -> toLowerCase() -> ''
    expect(target.normalizeLabel('')).toBe('');
    // Input: 'standard' -> trim() -> 'standard' -> toLowerCase() -> 'standard'
    expect(target.normalizeLabel('standard')).toBe('standard');
  });
});

describe('calculateDiscount', () => {
  // TC-003: Kiểm tra chiết khấu VIP với subtotal 500, capped tại 50
  test('TC-003 should return correct VIP discount with cap at 50', () => {
    // subtotal = 500, tier = 'vip'
    // discount = Math.min(500 * 0.12, 50) = Math.min(60, 50) = 50
    // roundMoney(50) = 50
    expect(target.calculateDiscount(500, 'vip')).toBe(50);
  });

  // TC-004: Kiểm tra chiết khấu VIP với subtotal 100, dưới mức cap
  test('TC-004 should return correct VIP discount below cap', () => {
    // subtotal = 100, tier = 'VIP' -> normalize -> 'vip'
    // discount = Math.min(100 * 0.12, 50) = Math.min(12, 50) = 12
    // roundMoney(12) = 12
    expect(target.calculateDiscount(100, 'VIP')).toBe(12);
  });

  // TC-005: Kiểm tra chiết khấu loyal với subtotal 500, capped tại 30
  test('TC-005 should return correct loyal discount with cap at 30', () => {
    // subtotal = 500, tier = ' loyal ' -> normalize -> 'loyal'
    // discount = Math.min(500 * 0.07, 30) = Math.min(35, 30) = 30
    // roundMoney(30) = 30
    expect(target.calculateDiscount(500, ' loyal ')).toBe(30);
  });

  // TC-006: Kiểm tra chiết khấu standard bằng 0
  test('TC-006 should return zero for standard tier', () => {
    // subtotal = 1000, tier = 'STANDARD' -> normalize -> 'standard'
    // discount = 0
    expect(target.calculateDiscount(1000, 'STANDARD')).toBe(0);
  });

  // TC-007: Kiểm tra ngoại lệ khi subtotal âm
  test('TC-007 should throw Error for negative subtotal', () => {
    // subtotal = -10 < 0, phải throw Error
    expect(() => target.calculateDiscount(-10, 'vip')).toThrow('subtotal must not be negative');
  });

  // TC-008: Kiểm tra ngoại lệ khi customerTier không hợp lệ
  test('TC-008 should throw Error for invalid customer tier', () => {
    // tier = 'invalid' không phải vip, loyal, hoặc standard
    expect(() => target.calculateDiscount(100, 'invalid')).toThrow('unsupported customer tier: invalid');
  });

  // TC-009: Kiểm tra chiết khấu loyal với subtotal 100, dưới mức cap
  test('TC-009 should return correct loyal discount below cap', () => {
    // subtotal = 100, tier = 'loyal'
    // discount = Math.min(100 * 0.07, 30) = Math.min(7, 30) = 7
    // roundMoney(7) = 7
    expect(target.calculateDiscount(100, 'loyal')).toBe(7);
  });

  // TC-010: Kiểm tra chiết khấu VIP với subtotal 0
  test('TC-010 should return zero VIP discount for zero subtotal', () => {
    // subtotal = 0, tier = 'vip'
    // discount = Math.min(0 * 0.12, 50) = Math.min(0, 50) = 0
    // roundMoney(0) = 0
    expect(target.calculateDiscount(0, 'vip')).toBe(0);
  });

  // TC-011: Kiểm tra chiết khấu loyal với subtotal 0
  test('TC-011 should return zero loyal discount for zero subtotal', () => {
    // subtotal = 0, tier = 'loyal'
    // discount = Math.min(0 * 0.07, 30) = Math.min(0, 30) = 0
    // roundMoney(0) = 0
    expect(target.calculateDiscount(0, 'loyal')).toBe(0);
  });
});

describe('shippingFee', () => {
  // TC-012: Kiểm tra phí vận chuyển nội địa không dễ vỡ, weight <= 5
  test('TC-012 should calculate domestic shipping fee for weight <= 5', () => {
    // weightKg = 1, destination = 'domestic', fragile = false
    // fee = 5 (domestic base), weight <= 5 -> no additional, fragile = false -> no additional
    // roundMoney(5) = 5
    expect(target.shippingFee(1, 'domestic', false)).toBe(5);
  });

  // TC-013: Kiểm tra phí vận chuyển nội địa không dễ vỡ, 5 < weight <= 20
  test('TC-013 should calculate domestic shipping fee for 5 < weight <= 20', () => {
    // weightKg = 10, destination = 'domestic', fragile = false
    // fee = 5 (domestic base) + 10 (weight > 5) = 15
    // roundMoney(15) = 15
    expect(target.shippingFee(10, 'domestic', false)).toBe(15);
  });

  // TC-014: Kiểm tra phí vận chuyển nội địa không dễ vỡ, weight > 20
  test('TC-014 should calculate domestic shipping fee for weight > 20', () => {
    // weightKg = 25, destination = 'domestic', fragile = false
    // fee = 5 (domestic base) + 25 (weight > 20) = 30
    // roundMoney(30) = 30
    expect(target.shippingFee(25, 'domestic', false)).toBe(30);
  });

  // TC-015: Kiểm tra phí vận chuyển quốc tế không dễ vỡ, weight <= 5
  test('TC-015 should calculate international shipping fee for weight <= 5', () => {
    // weightKg = 1, destination = 'international', fragile = false
    // fee = 18 (international base), weight <= 5 -> no additional, fragile = false -> no additional
    // roundMoney(18) = 18
    expect(target.shippingFee(1, 'international', false)).toBe(18);
  });

  // TC-016: Kiểm tra phí vận chuyển nội địa dễ vỡ
  test('TC-016 should calculate domestic fragile shipping fee', () => {
    // weightKg = 1, destination = 'domestic', fragile = true
    // fee = 5 (domestic base) + 7.5 (fragile) = 12.5
    // roundMoney(12.5) = 12.5
    expect(target.shippingFee(1, 'domestic', true)).toBe(12.5);
  });

  // TC-017: Kiểm tra ngoại lệ khi weightKg <= 0
  test('TC-017 should throw Error for weight less than or equal to zero', () => {
    // weightKg = 0, phải throw Error
    expect(() => target.shippingFee(0, 'domestic', false)).toThrow('weight must be greater than zero');
  });

  // TC-018: Kiểm tra ngoại lệ khi destination không hợp lệ
  test('TC-018 should throw Error for invalid destination', () => {
    // destination = 'invalid' không phải domestic hay international
    expect(() => target.shippingFee(1, 'invalid', false)).toThrow('unsupported destination: invalid');
  });

  // TC-019: Kiểm tra phí vận chuyển quốc tế dễ vỡ
  test('TC-019 should calculate international fragile shipping fee', () => {
    // weightKg = 10, destination = 'international', fragile = true
    // fee = 18 (international base) + 10 (weight > 5) + 7.5 (fragile) = 35.5
    // roundMoney(35.5) = 35.5
    expect(target.shippingFee(10, 'international', true)).toBe(35.5);
  });
});

describe('finalTotal', () => {
  // TC-020: Kiểm tra ngoại lệ khi subtotal âm trong finalTotal
  test('TC-020 should throw Error for negative subtotal in order', () => {
    // order.subtotal = -10 < 0, calculateDiscount sẽ throw Error
    const order = {
      subtotal: -10,
      customerTier: 'vip',
      storeCredit: 0,
      weightKg: 1,
      destination: 'domestic',
      fragile: false
    };
    expect(() => target.finalTotal(order)).toThrow('subtotal must not be negative');
  });

  // TC-021: Kiểm tra finalTotal khi storeCredit bằng 0
  test('TC-021 should calculate final total with zero storeCredit', () => {
    // subtotal = 100, tier = 'standard' -> discount = 0
    // shippingFee = 5 (domestic, weight 1, not fragile)
    // subtotal = 100 - 0 + 5 = 105
    // storeCredit = 0, final = 105 - 0 = 105
    const order = {
      subtotal: 100,
      customerTier: 'standard',
      storeCredit: 0,
      weightKg: 1,
      destination: 'domestic',
      fragile: false
    };
    expect(target.finalTotal(order)).toBe(105);
  });

  // TC-022: Kiểm tra finalTotal khi storeCredit lớn hơn tổng phải trả
  test('TC-022 should return zero when storeCredit exceeds total', () => {
    // subtotal = 100, tier = 'standard' -> discount = 0
    // shippingFee = 5 (domestic, weight 1, not fragile)
    // subtotal = 100 - 0 + 5 = 105
    // storeCredit = 150, final = Math.max(105 - 150, 0) = 0
    const order = {
      subtotal: 100,
      customerTier: 'standard',
      storeCredit: 150,
      weightKg: 1,
      destination: 'domestic',
      fragile: false
    };
    expect(target.finalTotal(order)).toBe(0);
  });

  // TC-023: Kiểm tra ngoại lệ khi storeCredit âm
  test('TC-023 should throw Error for negative storeCredit', () => {
    // storeCredit = -10 < 0, phải throw Error
    const order = {
      subtotal: 100,
      customerTier: 'standard',
      storeCredit: -10,
      weightKg: 1,
      destination: 'domestic',
      fragile: false
    };
    expect(() => target.finalTotal(order)).toThrow('store credit must not be negative');
  });

  // TC-024: Kiểm tra finalTotal với VIP tier và storeCredit
  test('TC-024 should calculate final total with VIP discount and storeCredit', () => {
    // subtotal = 500, tier = 'vip' -> discount = 50 (capped)
    // shippingFee = 5 (domestic, weight 1, not fragile)
    // subtotal = 500 - 50 + 5 = 455
    // storeCredit = 50, final = 455 - 50 = 405
    const order = {
      subtotal: 500,
      customerTier: 'vip',
      storeCredit: 50,
      weightKg: 1,
      destination: 'domestic',
      fragile: false
    };
    expect(target.finalTotal(order)).toBe(405);
  });

  // TC-025: Kiểm tra finalTotal với loyal tier và storeCredit
  test('TC-025 should calculate final total with loyal discount and storeCredit', () => {
    // subtotal = 500, tier = 'loyal' -> discount = 30 (capped)
    // shippingFee = 18 (international, weight 1, not fragile)
    // subtotal = 500 - 30 + 18 = 488
    // storeCredit = 100, final = 488 - 100 = 388
    const order = {
      subtotal: 500,
      customerTier: 'loyal',
      storeCredit: 100,
      weightKg: 1,
      destination: 'international',
      fragile: false
    };
    expect(target.finalTotal(order)).toBe(388);
  });
});
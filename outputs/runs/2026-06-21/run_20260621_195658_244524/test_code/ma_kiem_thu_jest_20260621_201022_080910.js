const target = require('./source_under_test');

describe('normalizeLabel', () => {
  // Kiểm tra hàm chuẩn hoá xử lý đúng chữ hoa/thường và khoảng trắng
  test('normalizes case and trims whitespace', () => {
    expect(target.normalizeLabel('  VIP  ')).toBe('vip');
    expect(target.normalizeLabel('LoYaL')).toBe('loyal');
    expect(target.normalizeLabel('  Domestic  ')).toBe('domestic');
  });
});

describe('calculateDiscount', () => {
  // TC-001: VIP giảm 24 khi 12% của 200 nhỏ hơn 50
  test('returns correct VIP discount when subtotal yields less than $50', () => {
    expect(target.calculateDiscount(200, 'VIP')).toBe(24);
  });

  // TC-002: VIP giảm 50 khi 12% của 600 vượt quá 50
  test('returns capped VIP discount of $50 when 12% exceeds $50', () => {
    expect(target.calculateDiscount(600, 'vip')).toBe(50);
  });

  // TC-003: Loyal giảm 21 khi 7% của 300 nhỏ hơn 30
  test('returns correct Loyal discount when subtotal yields less than $30', () => {
    expect(target.calculateDiscount(300, 'LoYaL')).toBe(21);
  });

  // TC-004: Loyal giảm 30 khi 7% của 500 vượt quá 30
  test('returns capped Loyal discount of $30 when 7% exceeds $30', () => {
    expect(target.calculateDiscount(500, 'loyal')).toBe(30);
  });

  // TC-005: Standard không được giảm giá
  test('returns zero for Standard tier', () => {
    expect(target.calculateDiscount(150, 'standard')).toBe(0);
  });

  // TC-006: Ném lỗi khi subtotal âm
  test('throws error for negative subtotal', () => {
    expect(() => target.calculateDiscount(-10, 'vip')).toThrowError(Error);
  });

  // TC-007: Ném lỗi khi tier không hợp lệ
  test('throws error for unsupported customer tier', () => {
    expect(() => target.calculateDiscount(100, 'gold')).toThrowError(Error);
  });

  // TC-008: Xử lý trường hợp subtotal bằng 0
  test('handles subtotal of zero', () => {
    expect(target.calculateDiscount(0, 'vip')).toBe(0);
  });
});

describe('shippingFee', () => {
  // TC-009: Phí cơ bản nội địa 5, không tính phí thêm
  test('calculates domestic base fee without extra weight or fragility', () => {
    expect(target.shippingFee(3, 'Domestic', false)).toBe(5);
  });

  // TC-010: Phí nội địa 15 (5 cơ bản + 10 trọng lượng 10kg)
  test('adds $10 for weight between 5kg and 20kg (domestic)', () => {
    expect(target.shippingFee(10, 'domestic', false)).toBe(15);
  });

  // TC-011: Phí quốc tế 43 (18 cơ bản + 25 trọng lượng >20kg)
  test('adds $25 for weight > 20kg (international)', () => {
    expect(target.shippingFee(25, 'International', false)).toBe(43);
  });

  // TC-012: Phí 22.5 (5 cơ bản + 10 trọng lượng + 7.5 dễ vỡ)
  test('adds fragile surcharge on top of other fees', () => {
    expect(target.shippingFee(8, 'domestic', true)).toBe(22.5);
  });

  // TC-013: Ném lỗi khi trọng lượng không dương
  test('throws error for non-positive weight', () => {
    expect(() => target.shippingFee(0, 'domestic', false)).toThrowError(Error);
  });

  // TC-014: Ném lỗi khi destination không hợp lệ
  test('throws error for unsupported destination', () => {
    expect(() => target.shippingFee(5, 'mars', false)).toThrowError(Error);
  });

  // TC-015: Trọng lượng đúng 5kg không có phí thêm
  test('weight exactly 5kg (no extra weight fee)', () => {
    expect(target.shippingFee(5, 'domestic', false)).toBe(5);
  });

  // TC-016: Trọng lượng đúng 20kg có phí 10, không phải 25
  test('weight exactly 20kg (adds $10 weight fee, not $25)', () => {
    expect(target.shippingFee(20, 'international', false)).toBe(28);
  });
});

describe('finalTotal', () => {
  // TC-017: VIP, nội địa, không credit: 400 - 48 + 5 = 357
  test('computes correct total for VIP customer with domestic shipping, no credit', () => {
    const order = { subtotal: 400, customerTier: 'vip', weightKg: 4, destination: 'domestic', fragile: false, storeCredit: 0 };
    expect(target.finalTotal(order)).toBe(357);
  });

  // TC-018: Loyal, quốc tế, dễ vỡ, có credit: 200 - 14 + 45.5 - 30 = 191.5
  test('applies store credit correctly', () => {
    const order = { subtotal: 200, customerTier: 'loyal', weightKg: 6, destination: 'international', fragile: true, storeCredit: 30 };
    expect(target.finalTotal(order)).toBe(191.5);
  });

  // TC-019: Ném lỗi khi storeCredit âm
  test('throws error when storeCredit is negative', () => {
    const order = { subtotal: 100, customerTier: 'standard', weightKg: 2, destination: 'domestic', fragile: false, storeCredit: -5 };
    expect(() => target.finalTotal(order)).toThrowError(Error);
  });

  // TC-020: Truyền lỗi từ calculateDiscount cho tier không hợp lệ
  test('propagates error from calculateDiscount for invalid tier', () => {
    const order = { subtotal: 100, customerTier: 'gold', weightKg: 2, destination: 'domestic', fragile: false, storeCredit: 0 };
    expect(() => target.finalTotal(order)).toThrowError(Error);
  });

  // TC-021: Truyền lỗi từ shippingFee cho destination không hợp lệ
  test('propagates error from shippingFee for invalid destination', () => {
    const order = { subtotal: 100, customerTier: 'standard', weightKg: 2, destination: 'moon', fragile: false, storeCredit: 0 };
    expect(() => target.finalTotal(order)).toThrowError(Error);
  });

  // TC-022: Khi storeCredit vượt quá tổng, trả về 0
  test('returns 0 when store credit exceeds computed total', () => {
    const order = { subtotal: 50, customerTier: 'standard', weightKg: 1, destination: 'domestic', fragile: false, storeCredit: 100 };
    expect(target.finalTotal(order)).toBe(0);
  });
});
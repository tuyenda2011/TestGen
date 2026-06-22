const target = require('./source_under_test');

describe('calculateDiscount', () => {
  // Kiểm tra giảm giá cho khách VIP, giới hạn 50$
  test('returns capped VIP discount', () => {
    const result = target.calculateDiscount(600, 'VIP');
    expect(result).toBe(50);
  });

  // Kiểm tra giảm giá cho khách Loyal, không vượt ngưỡng
  test('returns Loyal discount below cap', () => {
    const result = target.calculateDiscount(400, 'loyal');
    expect(result).toBe(28);
  });

  // Kiểm tra không giảm giá cho khách Standard
  test('returns zero discount for standard tier', () => {
    const result = target.calculateDiscount(200, 'standard');
    expect(result).toBe(0);
  });

  // Kiểm tra lỗi khi subtotal âm
  test('throws error for negative subtotal', () => {
    expect(() => target.calculateDiscount(-10, 'vip')).toThrowError('subtotal must not be negative');
  });

  // Kiểm tra lỗi khi tier không hỗ trợ
  test('throws error for unsupported customer tier', () => {
    expect(() => target.calculateDiscount(100, 'gold')).toThrowError('unsupported customer tier: gold');
  });
});

describe('shippingFee', () => {
  // Kiểm tra phí nội địa cho trọng lượng ≤5kg, không fragile
  test('calculates domestic fee for light, non‑fragile package', () => {
    const fee = target.shippingFee(4, 'Domestic', false);
    expect(fee).toBe(5);
  });

  // Kiểm tra phụ phí trọng lượng cho 6kg nội địa
  test('adds weight surcharge for 6kg domestic package', () => {
    const fee = target.shippingFee(6, 'domestic', false);
    expect(fee).toBe(15); // 5 + 10
  });

  // Kiểm tra phụ phí nặng và fragile cho quốc tế
  test('adds heavy weight and fragile surcharge for international package', () => {
    const fee = target.shippingFee(25, 'International', true);
    expect(fee).toBe(50.5); // 18 + 25 + 7.5
  });

  // Kiểm tra lỗi khi trọng lượng bằng 0
  test('throws error for zero weight', () => {
    expect(() => target.shippingFee(0, 'domestic', false)).toThrowError('weight must be greater than zero');
  });

  // Kiểm tra lỗi khi destination không hợp lệ
  test('throws error for unsupported destination', () => {
    expect(() => target.shippingFee(3, 'mars', false)).toThrowError('unsupported destination: mars');
  });
});

describe('finalTotal', () => {
  // Kiểm tra tính tổng cuối cùng cho đơn hàng VIP nội địa, không có store credit
  test('computes correct final total for VIP domestic order', () => {
    const order = {
      subtotal: 500,
      customerTier: 'vip',
      weightKg: 4,
      destination: 'domestic',
      fragile: false,
      storeCredit: 0,
    };
    const total = target.finalTotal(order);
    // discount 50, shipping 5 => 500 - 50 + 5 = 455, không có store credit, roundMoney => 455
    expect(total).toBe(455);
  });

  // Kiểm tra lỗi khi storeCredit âm
  test('throws error when store credit is negative', () => {
    const order = {
      subtotal: 100,
      customerTier: 'standard',
      weightKg: 2,
      destination: 'domestic',
      fragile: false,
      storeCredit: -5,
    };
    expect(() => target.finalTotal(order)).toThrowError('store credit must not be negative');
  });

  // Kiểm tra rounding sau tính tổng đầy đủ (sử dụng giá trị thập phân)
  test('applies rounding after full calculation', () => {
    const order = {
      subtotal: 123.456,
      customerTier: 'loyal',
      weightKg: 6.789,
      destination: 'international',
      fragile: true,
      storeCredit: 0,
    };
    const total = target.finalTotal(order);
    // discount: min(123.456*0.07,30)=8.64192 -> roundMoney => 8.64
    // shipping: base 18 + weight surcharge 10 + fragile 7.5 = 35.5 -> roundMoney => 35.5
    // subtotal after ops: 123.456 - 8.64 + 35.5 = 150.316 -> roundMoney => 150.32
    expect(total).toBe(150.32);
  });
});
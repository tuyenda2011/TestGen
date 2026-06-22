// Plan: TC-001, TC-002, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018

const target = require('./source_under_test');

describe('orderPricing module tests', () => {
  // TC-001: normalizeLabel trims spaces and converts to lower case
  test('TC-001 normalizeLabel trims and lowercases string', () => {
    const result = target.normalizeLabel('  HeLLo WoRLd  ');
    expect(result).toBe('hello world');
  });

  // TC-002: normalizeLabel with already normalized string
  test('TC-002 normalizeLabel returns unchanged string when already normalized', () => {
    const result = target.normalizeLabel('test');
    expect(result).toBe('test');
  });

  // TC-005: calculateDiscount for VIP without hitting cap
  test('TC-005 calculateDiscount VIP without cap', () => {
    // 12% của 200 = 24, không vượt giới hạn 50
    const discount = target.calculateDiscount(200, 'vip');
    expect(discount).toBe(24);
  });

  // TC-006: calculateDiscount for VIP hitting $50 cap
  test('TC-006 calculateDiscount VIP with cap', () => {
    // 12% của 600 = 72, nhưng bị giới hạn ở 50
    const discount = target.calculateDiscount(600, 'vip');
    expect(discount).toBe(50);
  });

  // TC-007: calculateDiscount for Loyal without hitting cap
  test('TC-007 calculateDiscount Loyal without cap', () => {
    // 7% của 200 = 14, không vượt giới hạn 30
    const discount = target.calculateDiscount(200, 'loyal');
    expect(discount).toBe(14);
  });

  // TC-008: calculateDiscount for Loyal hitting $30 cap
  test('TC-008 calculateDiscount Loyal with cap', () => {
    // 7% của 600 = 42, nhưng bị giới hạn ở 30
    const discount = target.calculateDiscount(600, 'loyal');
    expect(discount).toBe(30);
  });

  // TC-009: calculateDiscount for Standard tier returns zero
  test('TC-009 calculateDiscount Standard returns zero', () => {
    const discount = target.calculateDiscount(150, 'standard');
    expect(discount).toBe(0);
  });

  // TC-010: calculateDiscount throws error for negative subtotal
  test('TC-010 calculateDiscount throws on negative subtotal', () => {
    expect(() => {
      target.calculateDiscount(-10, 'vip');
    }).toThrowError('subtotal must not be negative');
  });

  // TC-011: calculateDiscount throws error for unsupported tier
  test('TC-011 calculateDiscount throws on unsupported tier', () => {
    expect(() => {
      target.calculateDiscount(100, 'gold');
    }).toThrowError('unsupported customer tier: gold');
  });

  // TC-012: finalTotal calculates correctly with positive store credit
  test('TC-012 finalTotal correct calculation with store credit', () => {
    // shippingFee(3, "domestic", false) = 5
    // discount = 24 (vip 12% of 200)
    // subtotal = 200 - 24 + 5 - 20 = 161
    const order = {
      subtotal: 200,
      customerTier: 'vip',
      weightKg: 3,
      destination: 'domestic',
      fragile: false,
      storeCredit: 20,
    };
    const total = target.finalTotal(order);
    expect(total).toBe(161);
  });

  // TC-013: finalTotal throws error when store credit is negative
  test('TC-013 finalTotal throws on negative store credit', () => {
    const order = {
      subtotal: 100,
      customerTier: 'standard',
      weightKg: 2,
      destination: 'domestic',
      fragile: false,
      storeCredit: -5,
    };
    expect(() => {
      target.finalTotal(order);
    }).toThrowError('store credit must not be negative');
  });

  // TC-014: finalTotal floors result at zero when negative total
  test('TC-014 finalTotal floors at zero for negative result', () => {
    // shippingFee(1, "domestic", false) = 5
    // discount = 3.6 (vip 12% of 30)
    // subtotal = 30 - 3.6 + 5 = 31.4
    // storeCredit 40 > subtotal => total floored to 0
    const order = {
      subtotal: 30,
      customerTier: 'vip',
      weightKg: 1,
      destination: 'domestic',
      fragile: false,
      storeCredit: 40,
    };
    const total = target.finalTotal(order);
    expect(total).toBe(0);
  });

  // TC-015: shippingFee domestic weight <=5 no fragile
  test('TC-015 shippingFee domestic weight <=5 no fragile', () => {
    // fee = 5 (base domestic) vì weight <=5, không thêm phí
    const fee = target.shippingFee(4, 'domestic', false);
    expect(fee).toBe(5);
  });

  // TC-016: shippingFee domestic weight >5 adds 10
  test('TC-016 shippingFee domestic weight >5 adds surcharge', () => {
    // base 5 + 10 = 15
    const fee = target.shippingFee(6, 'domestic', false);
    expect(fee).toBe(15);
  });

  // TC-017: shippingFee international weight >20 adds 25
  test('TC-017 shippingFee international weight >20 adds surcharge', () => {
    // base 18 + 25 = 43
    const fee = target.shippingFee(21, 'international', false);
    expect(fee).toBe(43);
  });

  // TC-018: shippingFee fragile adds 7.5
  test('TC-018 shippingFee adds fragile surcharge', () => {
    // base domestic 5 + fragile 7.5 = 12.5, round to 12.5
    const fee = target.shippingFee(3, 'domestic', true);
    expect(fee).toBe(12.5);
  });
});
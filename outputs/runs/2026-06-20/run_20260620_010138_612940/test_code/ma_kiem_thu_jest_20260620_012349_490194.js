// Plan: TC-001, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016
const target = require('./source_under_test');

describe('orderPricing module', () => {
  // TC-001: normalizeLabel trims and lowercases input
  test('TC-001 normalizeLabel trims and lowercases input', () => {
    const result = target.normalizeLabel('  HeLLo WoRLd  ');
    expect(result).toBe('hello world');
  });

  // TC-003: calculateDiscount for VIP where 12% of subtotal is less than $50
  test('TC-003 calculateDiscount VIP below cap', () => {
    const subtotal = 300;
    const discount = target.calculateDiscount(subtotal, 'vip');
    // 12% của 300 = 36, dưới mức cap 50
    expect(discount).toBeCloseTo(36);
  });

  // TC-004: calculateDiscount for VIP where cap $50 applies
  test('TC-004 calculateDiscount VIP cap applied', () => {
    const subtotal = 600;
    const discount = target.calculateDiscount(subtotal, 'vip');
    // 12% của 600 = 72, nhưng cap 50
    expect(discount).toBeCloseTo(50);
  });

  // TC-005: calculateDiscount for Loyal where 7% of subtotal is less than $30
  test('TC-005 calculateDiscount Loyal below cap', () => {
    const subtotal = 200;
    const discount = target.calculateDiscount(subtotal, 'loyal');
    // 7% của 200 = 14, dưới mức cap 30
    expect(discount).toBeCloseTo(14);
  });

  // TC-006: calculateDiscount for Loyal where cap $30 applies
  test('TC-006 calculateDiscount Loyal cap applied', () => {
    const subtotal = 500;
    const discount = target.calculateDiscount(subtotal, 'loyal');
    // 7% của 500 = 35, nhưng cap 30
    expect(discount).toBeCloseTo(30);
  });

  // TC-007: calculateDiscount for Standard customer returns zero
  test('TC-007 calculateDiscount Standard returns zero', () => {
    const discount = target.calculateDiscount(250, 'standard');
    expect(discount).toBe(0);
  });

  // TC-008: calculateDiscount throws error for negative subtotal
  test('TC-008 calculateDiscount negative subtotal throws', () => {
    expect(() => {
      target.calculateDiscount(-10, 'vip');
    }).toThrowError('subtotal must not be negative');
  });

  // TC-009: calculateDiscount throws error for unsupported customer tier
  test('TC-009 calculateDiscount unsupported tier throws', () => {
    expect(() => {
      target.calculateDiscount(100, 'gold');
    }).toThrowError('unsupported customer tier: gold');
  });

  // TC-010: shippingFee throws error when weightKg is zero or negative
  test('TC-010 shippingFee zero weight throws', () => {
    expect(() => {
      target.shippingFee(0, 'domestic', false);
    }).toThrowError('weight must be greater than zero');
  });

  // TC-011: shippingFee throws error for unsupported destination
  test('TC-011 shippingFee unsupported destination throws', () => {
    expect(() => {
      target.shippingFee(5, 'moon', false);
    }).toThrowError('unsupported destination: moon');
  });

  // TC-012: shippingFee calculates fee for heavy fragile international shipment
  test('TC-012 shippingFee heavy fragile international', () => {
    const fee = target.shippingFee(25, 'international', true);
    // base 18 + surcharge 25 (weight>20) + fragile 7.5 = 50.5, sau khi làm tròn vẫn 50.5
    expect(fee).toBeCloseTo(50.5);
  });

  // TC-013: shippingFee calculates fee for medium non‑fragile domestic shipment
  test('TC-013 shippingFee medium non-fragile domestic', () => {
    const fee = target.shippingFee(10, 'domestic', false);
    // base 5 + surcharge 10 (weight>5) = 15, làm tròn vẫn 15
    expect(fee).toBeCloseTo(15);
  });

  // TC-014: finalTotal throws error when storeCredit is negative
  test('TC-014 finalTotal throws error for negative storeCredit', () => {
    const order = {
      subtotal: 100,
      customerTier: 'standard',
      storeCredit: -5,
      weightKg: 2,
      destination: 'domestic',
      fragile: false,
    };
    expect(() => target.finalTotal(order)).toThrowError('store credit must not be negative');
  });

  // TC-015: finalTotal floors result at zero when discounts and credit exceed subtotal plus shipping
  test('TC-015 finalTotal floors at zero when overdiscounted', () => {
    const order = {
      subtotal: 50,
      customerTier: 'vip',
      storeCredit: 100,
      weightKg: 1,
      destination: 'domestic',
      fragile: false,
    };
    const total = target.finalTotal(order);
    expect(total).toBe(0);
  });

  // TC-016: finalTotal throws error for negative subtotal (propagated from calculateDiscount)
  test('TC-016 finalTotal throws error for negative subtotal', () => {
    const order = {
      subtotal: -20,
      customerTier: 'vip',
      storeCredit: 0,
      weightKg: 1,
      destination: 'domestic',
      fragile: false,
    };
    expect(() => target.finalTotal(order)).toThrowError('subtotal must not be negative');
  });
});
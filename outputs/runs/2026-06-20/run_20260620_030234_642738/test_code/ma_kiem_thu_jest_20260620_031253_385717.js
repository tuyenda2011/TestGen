// Plan: TC-001, TC-002, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014
const target = require('./source_under_test');

function roundMoney(value) {
  return Math.round(value * 100) / 100;
}

describe('orderPricing module', () => {
  // TC-001: normalizeLabel returns trimmed lower‑cased string
  test('TC-001 normalizeLabel trims and lowercases input', () => {
    const result = target.normalizeLabel('  VIP ');
    expect(result).toBe('vip');
  });

  // TC-002: normalizeLabel with already normalized input
  test('TC-002 normalizeLabel returns unchanged string when already normalized', () => {
    const result = target.normalizeLabel('standard');
    expect(result).toBe('standard');
  });

  // TC-005: calculateDiscount VIP tier without cap limit
  test('TC-005 calculateDiscount VIP tier without hitting cap', () => {
    const discount = target.calculateDiscount(300, 'vip');
    expect(discount).toBeCloseTo(36);
  });

  // TC-006: calculateDiscount VIP tier capped at $50
  test('TC-006 calculateDiscount VIP tier capped at $50', () => {
    const discount = target.calculateDiscount(600, 'VIP');
    expect(discount).toBeCloseTo(50);
  });

  // TC-007: calculateDiscount Loyal tier capped at $30
  test('TC-007 calculateDiscount Loyal tier capped at $30', () => {
    const discount = target.calculateDiscount(500, '  loyal  ');
    expect(discount).toBeCloseTo(30);
  });

  // TC-008: calculateDiscount Standard tier receives no discount
  test('TC-008 calculateDiscount Standard tier receives no discount', () => {
    const discount = target.calculateDiscount(200, 'Standard');
    expect(discount).toBe(0);
  });

  // TC-009: calculateDiscount throws error for negative subtotal
  test('TC-009 calculateDiscount throws error when subtotal is negative', () => {
    expect(() => {
      target.calculateDiscount(-10, 'vip');
    }).toThrow(Error);
  });

  // TC-010: calculateDiscount throws error for unsupported customer tier
  test('TC-010 calculateDiscount throws error for unsupported tier', () => {
    expect(() => {
      target.calculateDiscount(100, 'gold');
    }).toThrow(Error);
  });

  // TC-011: finalTotal calculates correct total with store credit less than amount
  test('TC-011 finalTotal calculates total with store credit applied', () => {
    const order = {
      storeCredit: 20,
      subtotal: 200,
      customerTier: 'vip',
      weightKg: 3,
      destination: 'domestic',
      fragile: false,
    };
    const expectedDiscount = target.calculateDiscount(order.subtotal, order.customerTier);
    const expectedShipping = target.shippingFee(order.weightKg, order.destination, order.fragile);
    const rawTotal = order.subtotal - expectedDiscount + expectedShipping - order.storeCredit;
    const expectedTotal = roundMoney(Math.max(rawTotal, 0));
    const result = target.finalTotal(order);
    expect(result).toBeCloseTo(expectedTotal);
  });

  // TC-012: finalTotal floors total to zero when store credit exceeds amount
  test('TC-012 finalTotal floors total to zero when store credit exceeds amount', () => {
    const order = {
      storeCredit: 500,
      subtotal: 100,
      customerTier: 'standard',
      weightKg: 1,
      destination: 'domestic',
      fragile: false,
    };
    const expectedDiscount = target.calculateDiscount(order.subtotal, order.customerTier);
    const expectedShipping = target.shippingFee(order.weightKg, order.destination, order.fragile);
    const rawTotal = order.subtotal - expectedDiscount + expectedShipping - order.storeCredit;
    const expectedTotal = roundMoney(Math.max(rawTotal, 0));
    const result = target.finalTotal(order);
    expect(result).toBeCloseTo(expectedTotal);
    expect(result).toBe(0);
  });

  // TC-013: finalTotal throws error for negative store credit
  test('TC-013 finalTotal throws error when store credit is negative', () => {
    const order = {
      storeCredit: -5,
      subtotal: 100,
      customerTier: 'loyal',
      weightKg: 2,
      destination: 'domestic',
      fragile: false,
    };
    expect(() => {
      target.finalTotal(order);
    }).toThrow(Error);
  });

  // TC-014: shippingFee behavior not validated in finalTotal test plan (out of scope)
  test('TC-014 finalTotal integrates shippingFee without explicit validation', () => {
    const order = {
      storeCredit: 10,
      subtotal: 150,
      customerTier: 'loyal',
      weightKg: 6,
      destination: 'international',
      fragile: true,
    };
    const result = target.finalTotal(order);
    expect(typeof result).toBe('number');
    expect(() => target.finalTotal(order)).not.toThrow();
  });
});
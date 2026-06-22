const pricing = require('./source_under_test');

describe('order pricing', () => {
  test('caps VIP discount at 50', () => {
    expect(pricing.calculateDiscount(1000, 'VIP')).toBe(50);
  });

  test('adds fragile and medium weight shipping surcharge', () => {
    expect(pricing.shippingFee(6, 'domestic', true)).toBe(22.5);
  });

  test('store credit cannot make total negative', () => {
    expect(pricing.applyStoreCredit(25, 30)).toBe(0);
  });

  test('rejects unsupported customer tier', () => {
    expect(() => pricing.calculateDiscount(100, 'guest')).toThrow(/tier/i);
  });
});

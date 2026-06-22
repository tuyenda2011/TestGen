// Plan: TC-001, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013
const target = require('./source_under_test');

describe('orderPricing module tests', () => {
  test('TC-001 normalizeLabel trims spaces and lowercases input', () => {
    // Kiểm tra hàm normalizeLabel loại bỏ khoảng trắng và chuyển về chữ thường
    const result = target.normalizeLabel('  HeLLo WoRLd  ');
    expect(result).toBe('hello world');
  });

  test('TC-004 calculateDiscount throws error for negative subtotal', () => {
    // Kiểm tra calculateDiscount ném lỗi khi subtotal âm
    expect(() => target.calculateDiscount(-5, 'vip')).toThrowError('subtotal must not be negative');
  });

  test('TC-005 calculateDiscount returns correct VIP discount (percentage limit)', () => {
    // subtotal=300, vip => min(300*0.12,50)=36, roundMoney(36)=36
    const discount = target.calculateDiscount(300, 'vip');
    expect(discount).toBe(36);
  });

  test('TC-006 calculateDiscount returns correct VIP discount (fixed limit)', () => {
    // subtotal=600, vip => min(600*0.12,50)=50, roundMoney(50)=50
    const discount = target.calculateDiscount(600, 'vip');
    expect(discount).toBe(50);
  });

  test('TC-007 calculateDiscount returns correct Loyal discount (percentage limit)', () => {
    // subtotal=200, loyal => min(200*0.07,30)=14, roundMoney(14)=14
    const discount = target.calculateDiscount(200, 'loyal');
    expect(discount).toBe(14);
  });

  test('TC-008 calculateDiscount returns correct Loyal discount (fixed limit)', () => {
    // subtotal=500, loyal => min(500*0.07,30)=30, roundMoney(30)=30
    const discount = target.calculateDiscount(500, 'loyal');
    expect(discount).toBe(30);
  });

  test('TC-009 calculateDiscount returns zero for Standard tier', () => {
    // subtotal=150, standard => 0
    const discount = target.calculateDiscount(150, 'standard');
    expect(discount).toBe(0);
  });

  test('TC-010 calculateDiscount throws error for unsupported tier', () => {
    // Kiểm tra lỗi khi tier không được hỗ trợ
    expect(() => target.calculateDiscount(100, 'gold')).toThrowError('unsupported customer tier: gold');
  });

  test('TC-011 finalTotal throws error when store credit is negative', () => {
    // Kiểm tra finalTotal ném lỗi khi storeCredit âm
    const order = {
      subtotal: 100,
      customerTier: 'standard',
      storeCredit: -10,
      weightKg: 2,
      destination: 'domestic',
      fragile: false,
    };
    expect(() => target.finalTotal(order)).toThrowError('store credit must not be negative');
  });

  test('TC-012 finalTotal clamps result to zero when store credit exceeds subtotal after discount and shipping', () => {
    // Mock shippingFee to return 5
    const shippingMock = jest.spyOn(target, 'shippingFee').mockReturnValue(5);
    const order = {
      subtotal: 20,
      customerTier: 'standard',
      storeCredit: 30,
      weightKg: 1,
      destination: 'domestic',
      fragile: false,
    };
    const total = target.finalTotal(order);
    expect(total).toBe(0);
    shippingMock.mockRestore();
  });

  test('TC-013 finalTotal calculates correct amount for VIP tier with positive store credit', () => {
    // Mock shippingFee to return 10
    const shippingMock = jest.spyOn(target, 'shippingFee').mockReturnValue(10);
    const order = {
      subtotal: 200,
      customerTier: 'vip',
      storeCredit: 20,
      weightKg: 3,
      destination: 'domestic',
      fragile: false,
    };
    // discount = min(200*0.12,50)=24, subtotal-discount=176, +shipping 5 (actual) =181, -storeCredit 20 =161, roundMoney => 161
    const total = target.finalTotal(order);
    expect(total).toBe(161);
    shippingMock.mockRestore();
  });
});
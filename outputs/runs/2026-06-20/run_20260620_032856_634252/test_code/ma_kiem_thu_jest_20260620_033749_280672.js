const target = require('./source_under_test');


// Plan: TC-001, TC-002, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015

test('TC-001 normalizeLabel trims whitespace and converts to lower case', () => {
  // Kiểm tra hàm normalizeLabel loại bỏ khoảng trắng và chuyển về chữ thường
  const result = target.normalizeLabel('  HeLLo WoRLd  ');
  expect(result).toBe('hello world');
});

test('TC-002 normalizeLabel with empty string', () => {
  // Kiểm tra khi chuỗi chỉ chứa khoảng trắng, kết quả phải là chuỗi rỗng
  const result = target.normalizeLabel('   ');
  expect(result).toBe('');
});

test('TC-005 calculateDiscount throws error for negative subtotal', () => {
  // Kiểm tra hàm calculateDiscount ném lỗi khi subtotal < 0
  expect(() => {
    target.calculateDiscount(-10, 'vip');
  }).toThrowError('subtotal must not be negative');
});

test('TC-006 calculateDiscount throws error for unsupported tier', () => {
  // Kiểm tra hàm calculateDiscount ném lỗi khi tier không được hỗ trợ
  expect(() => {
    target.calculateDiscount(100, 'gold');
  }).toThrowError('unsupported customer tier: gold');
});

test('TC-007 calculateDiscount VIP tier discount capped at 50', () => {
  // subtotal 600 * 0.12 = 72, cap 50 => kết quả 50.00
  const discount = target.calculateDiscount(600, 'vip');
  expect(discount).toBe(50);
});

test('TC-008 calculateDiscount VIP tier discount below cap', () => {
  // subtotal 200 * 0.12 = 24, dưới cap 50 => kết quả 24.00
  const discount = target.calculateDiscount(200, 'vip');
  expect(discount).toBe(24);
});

test('TC-009 calculateDiscount Loyal tier discount capped at 30', () => {
  // subtotal 500 * 0.07 = 35, cap 30 => kết quả 30.00
  const discount = target.calculateDiscount(500, 'loyal');
  expect(discount).toBe(30);
});

test('TC-010 calculateDiscount Standard tier receives no discount', () => {
  // tier standard không có giảm giá
  const discount = target.calculateDiscount(150, 'standard');
  expect(discount).toBe(0);
});

test('TC-011 finalTotal throws error when store credit is negative', () => {
  // Kiểm tra lỗi khi storeCredit < 0
  const order = {
    storeCredit: -5,
    subtotal: 100,
    customerTier: 'standard',
    weightKg: 2,
    destination: 'domestic',
    fragile: false,
  };
  expect(() => {
    target.finalTotal(order);
  }).toThrowError('store credit must not be negative');
});

test('TC-012 finalTotal computes total with discount and shipping, no store credit', () => {
  // Mock shippingFee để trả về 5 cho trường hợp này
  const shippingMock = jest.spyOn(target, 'shippingFee').mockReturnValue(5);
  const order = {
    storeCredit: 0,
    subtotal: 200,
    customerTier: 'vip',
    weightKg: 2,
    destination: 'domestic',
    fragile: false,
  };
  // discount = 24 (vip), shipping = 5, subtotal - discount + shipping = 181, round = 181, storeCredit 0 => final 181
  const total = target.finalTotal(order);
  expect(total).toBe(181);
  shippingMock.mockRestore();
});

test('TC-013 finalTotal floors at zero when store credit exceeds payable amount', () => {
  // Mock shippingFee để trả về 3 cho trường hợp này
  const shippingMock = jest.spyOn(target, 'shippingFee').mockReturnValue(3);
  const order = {
    storeCredit: 300,
    subtotal: 50,
    customerTier: 'standard',
    weightKg: 1,
    destination: 'domestic',
    fragile: false,
  };
  // discount = 0, shipping = 3, subtotal+shipping = 53, sau khi trừ storeCredit = -247, floor to 0
  const total = target.finalTotal(order);
  expect(total).toBe(0);
  shippingMock.mockRestore();
});

test('TC-014 shippingFee throws error for nonpositive weight', () => {
  // Kiểm tra lỗi khi weightKg <= 0
  expect(() => {
    target.shippingFee(0, 'domestic', false);
  }).toThrowError('weight must be greater than zero');
});

test('TC-015 shippingFee throws error for unsupported destination', () => {
  // Kiểm tra lỗi khi destination không được hỗ trợ
  expect(() => {
    target.shippingFee(5, 'moon', false);
  }).toThrowError('unsupported destination: moon');
});
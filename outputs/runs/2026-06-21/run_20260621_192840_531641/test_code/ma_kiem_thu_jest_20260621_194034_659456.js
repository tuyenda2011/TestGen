const target = require('./source_under_test');

function computeDiscount(subtotal, tier) {
  const normalized = tier.trim().toLowerCase();
  if (normalized === 'vip') return Math.min(subtotal * 0.12, 50);
  if (normalized === 'loyal') return Math.min(subtotal * 0.07, 30);
  return 0;
}

function computeShipping(weightKg, destination, fragile = false) {
  const base = destination.trim().toLowerCase() === 'domestic' ? 5 : 18;
  let fee = base;
  if (weightKg > 20) fee += 25;
  else if (weightKg > 5) fee += 10;
  if (fragile) fee += 7.5;
  return Math.round(fee * 100) / 100;
}

// -------------------- calculateDiscount tests --------------------
describe('calculateDiscount', () => {
  // Kiểm tra giảm giá cho tier VIP khi 12% < $50
  test('vip discount below cap', () => {
    expect(target.calculateDiscount(200, 'vip')).toBe(24);
  });

  // Kiểm tra giảm giá cho tier VIP khi 12% > $50 (đạt cap)
  test('vip discount hits cap', () => {
    expect(target.calculateDiscount(600, 'vip')).toBe(50);
  });

  // Kiểm tra giảm giá cho tier Loyal khi 7% < $30
  test('loyal discount below cap', () => {
    expect(target.calculateDiscount(300, 'loyal')).toBe(21);
  });

  // Kiểm tra giảm giá cho tier Loyal khi 7% > $30 (đạt cap)
  test('loyal discount hits cap', () => {
    expect(target.calculateDiscount(500, 'loyal')).toBe(30);
  });

  // Kiểm tra tier Standard không được giảm giá
  test('standard tier receives no discount', () => {
    expect(target.calculateDiscount(400, 'standard')).toBe(0);
  });

  // Kiểm tra ngoại lệ subtotal âm
  test('throws error for negative subtotal', () => {
    expect(() => target.calculateDiscount(-10, 'vip')).toThrow(Error);
  });

  // Kiểm tra ngoại lệ tier không hỗ trợ
  test('throws error for unsupported tier', () => {
    expect(() => target.calculateDiscount(100, 'gold')).toThrow(Error);
  });

  // Kiểm tra normalizeLabel: bỏ khoảng trắng và chữ hoa
  test('handles tier with spaces and uppercase', () => {
    expect(target.calculateDiscount(200, ' VIP ')).toBe(24);
  });

  // Kiểm tra ranh giới subtotal = 0
  test('boundary subtotal zero returns zero discount', () => {
    expect(target.calculateDiscount(0, 'vip')).toBe(0);
  });
});

// -------------------- shippingFee tests --------------------
describe('shippingFee', () => {
  // Trường hợp cơ bản: domestic, trọng lượng <=5kg, không fragile
  test('domestic base fee without surcharge', () => {
    expect(target.shippingFee(4, 'domestic', false)).toBe(5);
  });

  // Trọng lượng >5kg <=20kg, domestic
  test('adds $10 surcharge for weight >5kg domestic', () => {
    expect(target.shippingFee(8, 'domestic', false)).toBe(15);
  });

  // Trọng lượng >20kg, domestic
  test('adds $25 surcharge for weight >20kg domestic', () => {
    expect(target.shippingFee(22, 'domestic', false)).toBe(30);
  });

  // Trọng lượng >20kg, international
  test('adds $25 surcharge for weight >20kg international', () => {
    expect(target.shippingFee(22, 'international', false)).toBe(43);
  });

  // Trọng lượng =20kg, international (surcharge $25 áp dụng)
  test('boundary weight exactly 20kg applies $25 surcharge international', () => {
    expect(target.shippingFee(20, 'international', false)).toBe(28);
  });

  // Trọng lượng =5kg, domestic (không surcharge)
  test('boundary weight exactly 5kg no surcharge domestic', () => {
    expect(target.shippingFee(5, 'domestic', false)).toBe(5);
  });

  // Fragile phí cộng thêm, không có surcharge trọng lượng
  test('adds fragile fee only, domestic weight <=5kg', () => {
    expect(target.shippingFee(4, 'domestic', true)).toBe(12.5);
  });

  // Fragile phí cộng thêm, có surcharge trọng lượng
  test('adds fragile fee on top of weight surcharge, international', () => {
    expect(target.shippingFee(6, 'international', true)).toBe(35.5);
  });

  // Ngoại lệ trọng lượng không hợp lệ
  test('throws error for non‑positive weight', () => {
    expect(() => target.shippingFee(0, 'domestic', false)).toThrow(Error);
  });

  // Ngoại lệ destination không hỗ trợ
  test('throws error for unsupported destination', () => {
    expect(() => target.shippingFee(3, 'moon', false)).toThrow(Error);
  });
});

// -------------------- finalTotal tests --------------------
describe('finalTotal', () => {
  test('computes total with discount, shipping, and store credit', () => {
    const order = {
      subtotal: 200,
      customerTier: 'vip',
      weightKg: 4,
      destination: 'domestic',
      fragile: false,
      storeCredit: 20,
    };
    // discount 24, shipping 5, subtotal after discount+shipping = 181, minus credit = 161
    // Wait: calculation: 200 - 24 + 5 = 181; 181 - 20 = 161
    expect(target.finalTotal(order)).toBe(161);
  });

  test('returns zero when store credit exceeds amount after discounts and shipping', () => {
    const order = {
      subtotal: 50,
      customerTier: 'standard',
      weightKg: 1,
      destination: 'domestic',
      fragile: false,
      storeCredit: 100,
    };
    // discount 0, shipping 5, subtotal = 55, credit 100 => max(55-100,0)=0
    expect(target.finalTotal(order)).toBe(0);
  });

  test('throws error for negative store credit', () => {
    const order = {
      subtotal: 100,
      customerTier: 'loyal',
      weightKg: 2,
      destination: 'domestic',
      fragile: false,
      storeCredit: -5,
    };
    expect(() => target.finalTotal(order)).toThrow(Error);
  });

  // Kiểm tra finalTotal khi discount = 0, shipping = 0 (điều kiện không tồn tại vì shipping luôn >=5)
  test('finalTotal with standard tier and domestic shipping', () => {
    const order = {
      subtotal: 10,
      customerTier: 'standard',
      weightKg: 0.1,
      destination: 'domestic',
      fragile: false,
      storeCredit: 0,
    };
    // shipping base 5, no surcharge, discount 0
    expect(target.finalTotal(order)).toBe(15);
  });
});
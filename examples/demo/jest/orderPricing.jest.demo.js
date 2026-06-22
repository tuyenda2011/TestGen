const {
  calculateDiscount,
  finalTotal,
  normalizeLabel,
  shippingFee,
} = require("./orderPricing");

describe("order pricing demo", () => {
  test("normalizes labels", () => {
    expect(normalizeLabel(" VIP ")).toBe("vip");
  });

  test.each([
    ["standard", 100, 0],
    ["loyal", 100, 7],
    ["vip", 100, 12],
    ["vip", 1000, 50],
  ])("calculates discount for %s tier", (tier, subtotal, expected) => {
    expect(calculateDiscount(subtotal, tier)).toBe(expected);
  });

  test.each([
    [5, "domestic", false, 5],
    [5.01, "domestic", false, 15],
    [20, "international", true, 35.5],
    [20.01, "international", false, 43],
  ])("calculates shipping boundaries", (weight, destination, fragile, expected) => {
    expect(shippingFee(weight, destination, fragile)).toBe(expected);
  });

  test("rejects invalid values with clear messages", () => {
    expect(() => calculateDiscount(-1, "standard")).toThrow("subtotal must not be negative");
    expect(() => shippingFee(0, "domestic")).toThrow("weight must be greater than zero");
    expect(() => shippingFee(1, "mars")).toThrow("unsupported destination");
  });

  test("combines discount, shipping and credit", () => {
    const total = finalTotal({
      subtotal: 100,
      weightKg: 6,
      destination: " domestic ",
      customerTier: "VIP",
      fragile: true,
      storeCredit: 10,
    });

    expect(total).toBe(100.5);
  });
});

function normalizeLabel(value) {
  return value.trim().toLowerCase();
}

function roundMoney(value) {
  return Math.round(value * 100) / 100;
}

function calculateDiscount(subtotal, customerTier) {
  if (subtotal < 0) {
    throw new Error("subtotal must not be negative");
  }

  const tier = normalizeLabel(customerTier);
  if (tier === "vip") {
    return roundMoney(Math.min(subtotal * 0.12, 50));
  }
  if (tier === "loyal") {
    return roundMoney(Math.min(subtotal * 0.07, 30));
  }
  if (tier === "standard") {
    return 0;
  }
  throw new Error(`unsupported customer tier: ${customerTier}`);
}

function shippingFee(weightKg, destination, fragile = false) {
  if (weightKg <= 0) {
    throw new Error("weight must be greater than zero");
  }

  const normalizedDestination = normalizeLabel(destination);
  if (!["domestic", "international"].includes(normalizedDestination)) {
    throw new Error(`unsupported destination: ${destination}`);
  }

  let fee = normalizedDestination === "domestic" ? 5 : 18;
  if (weightKg > 20) {
    fee += 25;
  } else if (weightKg > 5) {
    fee += 10;
  }
  if (fragile) {
    fee += 7.5;
  }
  return roundMoney(fee);
}

function finalTotal(order) {
  if (order.storeCredit < 0) {
    throw new Error("store credit must not be negative");
  }
  const subtotal = order.subtotal - calculateDiscount(order.subtotal, order.customerTier)
    + shippingFee(order.weightKg, order.destination, order.fragile);
  return roundMoney(Math.max(subtotal - order.storeCredit, 0));
}

module.exports = {
  calculateDiscount,
  finalTotal,
  normalizeLabel,
  shippingFee,
};

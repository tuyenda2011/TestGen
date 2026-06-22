public class OrderPricingService {
    public double calculateDiscount(double subtotal, String customerTier) {
        if (subtotal < 0) {
            throw new IllegalArgumentException("subtotal must not be negative");
        }

        String tier = customerTier.trim().toLowerCase();
        if ("vip".equals(tier)) {
            return round(Math.min(subtotal * 0.12, 50.0));
        }
        if ("loyal".equals(tier)) {
            return round(Math.min(subtotal * 0.07, 30.0));
        }
        if ("standard".equals(tier)) {
            return 0.0;
        }
        throw new IllegalArgumentException("unsupported customer tier: " + customerTier);
    }

    public double shippingFee(double weightKg, String destination, boolean fragile) {
        if (weightKg <= 0) {
            throw new IllegalArgumentException("weight must be greater than zero");
        }

        String normalizedDestination = destination.trim().toLowerCase();
        double fee;
        if ("domestic".equals(normalizedDestination)) {
            fee = 5.0;
        } else if ("international".equals(normalizedDestination)) {
            fee = 18.0;
        } else {
            throw new IllegalArgumentException("unsupported destination: " + destination);
        }

        if (weightKg > 20) {
            fee += 25.0;
        } else if (weightKg > 5) {
            fee += 10.0;
        }
        if (fragile) {
            fee += 7.5;
        }
        return round(fee);
    }

    public double finalTotal(
            double subtotal,
            double weightKg,
            String destination,
            String customerTier,
            boolean fragile,
            double storeCredit) {
        if (storeCredit < 0) {
            throw new IllegalArgumentException("store credit must not be negative");
        }
        double total = subtotal - calculateDiscount(subtotal, customerTier)
                + shippingFee(weightKg, destination, fragile)
                - storeCredit;
        return round(Math.max(total, 0.0));
    }

    private double round(double value) {
        return Math.round(value * 100.0) / 100.0;
    }
}

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

public class OrderPricingJUnitDemo {
    private final OrderPricingService service = new OrderPricingService();

    @Test
    void vipDiscountIsCapped() {
        assertEquals(50.0, service.calculateDiscount(1000.0, "vip"));
    }

    @Test
    void shippingBoundaryAtFiveKgDoesNotAddSurcharge() {
        assertEquals(5.0, service.shippingFee(5.0, "domestic", false));
    }

    @Test
    void shippingAboveTwentyKgUsesHeavySurcharge() {
        assertEquals(43.0, service.shippingFee(20.01, "international", false));
    }

    @Test
    void zeroWeightThrowsClearError() {
        IllegalArgumentException error = assertThrows(
                IllegalArgumentException.class,
                () -> service.shippingFee(0.0, "domestic", false));
        assertEquals("weight must be greater than zero", error.getMessage());
    }

    @Test
    void finalTotalCombinesDiscountShippingAndCredit() {
        double total = service.finalTotal(100.0, 6.0, "domestic", "VIP", true, 10.0);
        assertEquals(100.5, total);
    }
}

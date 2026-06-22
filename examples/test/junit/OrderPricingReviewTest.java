import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class OrderPricingReviewTest {
    @Test
    void capsVipDiscountAtFifty() {
        assertEquals(50.0, OrderPricingService.calculateDiscount(1000.0, "VIP"));
    }

    @Test
    void domesticFragileMediumWeightIncludesSurcharges() {
        assertEquals(22.5, OrderPricingService.shippingFee(6.0, "domestic", true));
    }

    @Test
    void storeCreditCannotMakeTotalNegative() {
        assertEquals(0.0, OrderPricingService.applyStoreCredit(25.0, 30.0));
    }

    @Test
    void rejectsUnsupportedDestination() {
        assertThrows(
                IllegalArgumentException.class,
                () -> OrderPricingService.shippingFee(1.0, "intergalactic", false)
        );
    }
}

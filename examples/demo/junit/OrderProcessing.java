public class OrderProcessing {
    private String status;
    private double totalAmount;

    public OrderProcessing() {
        this.status = "NEW";
        this.totalAmount = 0.0;
    }

    public void addItem(double price) {
        if (!status.equals("NEW")) {
            throw new IllegalStateException("Cannot add items to an order that is not NEW");
        }
        if (price <= 0) {
            throw new IllegalArgumentException("Price must be positive");
        }
        totalAmount += price;
    }

    public void checkout() {
        if (totalAmount < 10.0) {
            throw new IllegalStateException("Minimum order amount is 10.0");
        }
        this.status = "CHECKED_OUT";
    }

    public void cancel() {
        if (status.equals("SHIPPED")) {
            throw new IllegalStateException("Cannot cancel a shipped order");
        }
        this.status = "CANCELLED";
    }

    public void ship() {
        if (!status.equals("CHECKED_OUT")) {
            throw new IllegalStateException("Order must be checked out before shipping");
        }
        this.status = "SHIPPED";
    }

    public String getStatus() {
        return status;
    }

    public double getTotalAmount() {
        return totalAmount;
    }
}

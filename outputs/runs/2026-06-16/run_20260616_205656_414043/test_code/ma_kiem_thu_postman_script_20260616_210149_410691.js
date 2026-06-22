{
  "info": {
    "name": "Order Pricing Demo",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Quote VIP domestic fragile order",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{base_url}}/orders/quote",
          "host": [
            "{{base_url}}"
          ],
          "path": [
            "orders",
            "quote"
          ]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"subtotal\": 100,\n  \"weightKg\": 6,\n  \"destination\": \"domestic\",\n  \"customerTier\": \"VIP\",\n  \"fragile\": true,\n  \"storeCredit\": 10\n}"
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"status is OK\", function () {",
              "  pm.response.to.have.status(200);",
              "});",
              "",
              "pm.test(\"response has expected total\", function () {",
              "  const body = pm.response.json();",
              "  pm.expect(body.total).to.eql(100.5);",
              "});",
              "",
              "pm.test(\"response includes diagnostics\", function () {",
              "  const body = pm.response.json();",
              "  pm.expect(body.diagnostics).to.have.property(\"discount\");",
              "  pm.expect(body.diagnostics).to.have.property(\"shipping\");",
              "});"
            ]
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    }
  ]
}
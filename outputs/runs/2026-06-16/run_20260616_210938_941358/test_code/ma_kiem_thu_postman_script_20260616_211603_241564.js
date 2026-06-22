{
  "info": {
    "name": "Order Pricing Demo",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "TC-001 Quote VIP domestic fragile order",
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
              "  pm.expect(body.diagnostics.discount).to.eql(12);",
              "  pm.expect(body.diagnostics.shipping).to.eql(22.5);",
              "  pm.expect(body.diagnostics.totalBeforeCredit).to.eql(110.5);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-002 Missing subtotal returns validation error",
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
          "raw": "{\n  \"weightKg\": 1,\n  \"destination\": \"domestic\",\n  \"customerTier\": \"standard\",\n  \"fragile\": false,\n  \"storeCredit\": 0\n}"
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"status is Bad Request\", function () {",
              "  pm.response.to.have.status(400);",
              "});",
              "",
              "pm.test(\"response explains missing subtotal\", function () {",
              "  const body = pm.response.json();",
              "  pm.expect(body.error).to.include(\"subtotal\");",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-003 Zero subtotal uses shipping as total",
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
          "raw": "{\n  \"subtotal\": 0,\n  \"weightKg\": 1,\n  \"destination\": \"domestic\",\n  \"customerTier\": \"standard\",\n  \"fragile\": false,\n  \"storeCredit\": 0\n}"
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
              "pm.test(\"total equals domestic base shipping\", function () {",
              "  const body = pm.response.json();",
              "  pm.expect(body.total).to.eql(5);",
              "  pm.expect(body.diagnostics.discount).to.eql(0);",
              "  pm.expect(body.diagnostics.shipping).to.eql(5);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-004 Invalid destination returns validation error",
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
          "raw": "{\n  \"subtotal\": 100,\n  \"weightKg\": 1,\n  \"destination\": \"intergalactic\",\n  \"customerTier\": \"standard\",\n  \"fragile\": false,\n  \"storeCredit\": 0\n}"
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"status is Bad Request\", function () {",
              "  pm.response.to.have.status(400);",
              "});",
              "",
              "pm.test(\"response explains unsupported destination\", function () {",
              "  const body = pm.response.json();",
              "  pm.expect(body.error).to.include(\"destination\");",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-005 Negative store credit returns validation error",
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
          "raw": "{\n  \"subtotal\": 100,\n  \"weightKg\": 1,\n  \"destination\": \"domestic\",\n  \"customerTier\": \"standard\",\n  \"fragile\": false,\n  \"storeCredit\": -1\n}"
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"status is Bad Request\", function () {",
              "  pm.response.to.have.status(400);",
              "});",
              "",
              "pm.test(\"response explains invalid store credit\", function () {",
              "  const body = pm.response.json();",
              "  pm.expect(body.error).to.include(\"storeCredit\");",
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
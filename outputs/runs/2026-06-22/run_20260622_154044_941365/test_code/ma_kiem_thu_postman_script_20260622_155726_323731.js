{
  "info": {
    "name": "JSONPlaceholder API Test Collection",
    "description": "Bộ sưu tập Postman kiểm thử các kịch bản cho JSONPlaceholder API, đáp ứng yêu cầu và phản hồi của reviewer.",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "_postman_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
    "version": {
      "major": 1,
      "minor": 0,
      "patch": 0
    }
  },
  "item": [
    {
      "name": "TC-001 Retrieve existing user information (userId=1)",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/users/1",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "users",
            "1"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra mã trạng thái 200",
              "pm.test(\"Status code is 200\", function () {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "// Kiểm tra cấu trúc JSON trả về",
              "pm.test(\"Response schema contains required fields\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "    pm.expect(json.id).to.eql(1);",
              "    pm.expect(json).to.have.property('name');",
              "    pm.expect(json.name).to.be.a('string').and.not.empty;",
              "    pm.expect(json).to.have.property('username');",
              "    pm.expect(json).to.have.property('email');",
              "    pm.expect(json.email).to.match(/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/);",
              "    pm.expect(json).to.have.property('address');",
              "    pm.expect(json).to.have.property('phone');",
              "    pm.expect(json).to.have.property('website');",
              "    pm.expect(json).to.have.property('company');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-002 Retrieve non‑existent user (userId=9999)",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/users/9999",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "users",
            "9999"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// JSONPlaceholder trả về 404 cho userId không tồn tại",
              "pm.test(\"Status code is 404\", function () {",
              "    pm.response.to.have.status(404);",
              "});",
              "",
              "pm.test(\"Response body is empty object\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.be.empty;",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-003 Retrieve user with invalid userId type (string)",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/users/abc",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "users",
            "abc"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// API trả về 404 khi path parameter không phải số",
              "pm.test(\"Status code is 404\", function () {",
              "    pm.response.to.have.status(404);",
              "});",
              "",
              "pm.test(\"Response body is empty object for invalid id\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.be.empty;",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-004 Create a new post with valid payload",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"userId\": 1,\n  \"title\": \"sample title\",\n  \"body\": \"sample body\"\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "posts"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"Status code is 201 (Created)\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains same userId, title, body\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(1);",
              "    pm.expect(json.title).to.eql('sample title');",
              "    pm.expect(json.body).to.eql('sample body');",
              "});",
              "",
              "pm.test(\"Response includes auto‑generated id\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "    pm.expect(json.id).to.be.a('number');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-005 Create post missing required field (title)",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"userId\": 1,\n  \"body\": \"sample body\"\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "posts"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"Status code is 201 (Created) even without title\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response does not contain title field\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.not.have.property('title');",
              "    pm.expect(json).to.have.property('userId');",
              "    pm.expect(json).to.have.property('body');",
              "    pm.expect(json).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-006 Create post with maximum allowed length strings (≤50 chars title, ≤200 chars body)",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"userId\": 1,\n  \"title\": \"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTU\", \n  \"body\": \"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ\"\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "posts"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"Status code is 201 for long strings\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response echoes back title and body exactly as sent\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.title).to.eql('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTU');",
              "    pm.expect(json.body).to.eql('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ');",
              "});",
              "",
              "pm.test(\"Response contains auto‑generated id\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-007 GET /users (list all users)",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/users",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "users"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"Status code is 200 for users list\", function () {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "pm.test(\"Response is an array with at least one user\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.be.an('array');",
              "    pm.expect(json.length).to.be.above(0);",
              "    pm.expect(json[0]).to.have.property('id');",
              "    pm.expect(json[0]).to.have.property('email');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-008 Create post with non‑existent userId (9999)",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"userId\": 9999,\n  \"title\": \"non existent user\",\n  \"body\": \"testing\"\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "posts"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test(\"Status code is 201 even with non‑existent userId\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response echoes the sent userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(9999);",
              "    pm.expect(json.title).to.eql('non existent user');",
              "    pm.expect(json.body).to.eql('testing');",
              "    pm.expect(json).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
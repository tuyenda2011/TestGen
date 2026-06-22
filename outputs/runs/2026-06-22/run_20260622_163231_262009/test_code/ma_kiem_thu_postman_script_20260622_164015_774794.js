{
  "info": {
    "name": "JSONPlaceholder API Demo - Automated Tests",
    "description": "Bộ sưu tập Postman tự động kiểm thử các kịch bản API theo kế hoạch test.",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "version": {
      "major": 1,
      "minor": 0,
      "patch": 0
    }
  },
  "item": [
    {
      "name": "TC-001 POST /posts - valid userId",
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
          "raw": "{\n  \"userId\": 1\n}"
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
              "// Kiểm tra mã trạng thái 201",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra userId trong phản hồi bằng với giá trị gửi",
              "pm.test(\"Response contains correct userId\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.userId).to.eql(1);",
              "});",
              "",
              "// Kiểm tra thuộc tính id được sinh tự động",
              "pm.test(\"Response has auto‑generated id\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-002 POST /posts - missing userId",
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
          "raw": "{}"
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
              "// Kiểm tra mã trạng thái 201 khi không có userId (API trả về 201 mặc định)",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra rằng phản hồi không chứa thuộc tính userId",
              "pm.test(\"Response does not contain userId\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.not.have.property('userId');",
              "});",
              "",
              "// Kiểm tra thuộc tính id được sinh tự động",
              "pm.test(\"Response has auto‑generated id\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-003 POST /posts - userId zero",
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
          "raw": "{\n  \"userId\": 0\n}"
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
              "// Kiểm tra mã trạng thái 201 cho userId = 0",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra phản hồi chứa userId = 0",
              "pm.test(\"Response contains userId 0\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.userId).to.eql(0);",
              "});",
              "",
              "// Kiểm tra thuộc tính id tự động sinh",
              "pm.test(\"Response has auto‑generated id\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-004 GET /users/1 - existing user",
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
              "// Kiểm tra cấu trúc phản hồi người dùng",
              "pm.test(\"Response contains required fields\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "    pm.expect(jsonData.id).to.eql(1);",
              "    pm.expect(jsonData).to.have.property('name');",
              "    pm.expect(jsonData).to.have.property('username');",
              "    pm.expect(jsonData).to.have.property('email');",
              "    pm.expect(jsonData).to.have.property('address');",
              "    pm.expect(jsonData).to.have.property('phone');",
              "    pm.expect(jsonData).to.have.property('website');",
              "    pm.expect(jsonData).to.have.property('company');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-005 GET /users/abc - invalid id",
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
              "// Kiểm tra mã lỗi khi id không phải số (mong đợi 404 hoặc 400)",
              "pm.test(\"Status code is 404 or 400\", function () {",
              "    var status = pm.response.code;",
              "    pm.expect([400, 404]).to.include(status);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-006 GET /users/999999999 - non‑existent user",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/users/999999999",
          "protocol": "https",
          "host": [
            "jsonplaceholder",
            "typicode",
            "com"
          ],
          "path": [
            "users",
            "999999999"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra mã 404 cho người dùng không tồn tại",
              "pm.test(\"Status code is 404\", function () {",
              "    pm.response.to.have.status(404);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-007 Clarification - authentication requirement",
      "request": {
        "method": "GET",
        "header": [],
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
              "// Kiểm tra rằng API không yêu cầu header xác thực",
              "pm.test(\"No authentication required\", function () {",
              "    pm.response.to.have.status(200);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-008 Clarification - POST payload schema",
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
          "raw": "{\n  \"title\": \"Sample Title\",\n  \"body\": \"Sample body content\",\n  \"userId\": 2\n}"
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
              "// Kiểm tra rằng các trường title và body được chấp nhận khi có",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains sent title and body\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.title).to.eql(\"Sample Title\");",
              "    pm.expect(jsonData.body).to.eql(\"Sample body content\");",
              "    pm.expect(jsonData.userId).to.eql(2);",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
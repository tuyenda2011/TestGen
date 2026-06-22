{
  "info": {
    "name": "JSONPlaceholder API Test Collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "description": "Bộ sưu tập kiểm thử các kịch bản yêu cầu cho JSONPlaceholder"
  },
  "item": [
    {
      "name": "TC-001 Create post with all fields",
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
          "raw": "{\n  \"userId\": 1,\n  \"title\": \"Test Title\",\n  \"body\": \"Test Body\"\n}"
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
              "// Kiểm tra nội dung phản hồi",
              "pm.test(\"Response contains correct userId, title, body and auto‑generated id\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.userId).to.eql(1);",
              "    pm.expect(jsonData.title).to.eql(\"Test Title\");",
              "    pm.expect(jsonData.body).to.eql(\"Test Body\");",
              "    pm.expect(jsonData).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-002 Create post missing required userId",
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
          "raw": "{\n  \"title\": \"No UserId\",\n  \"body\": \"Missing userId\"\n}"
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
              "// Khi thiếu userId, API vẫn trả về 201 với dữ liệu đã gửi và id tự động",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra phản hồi có chứa id được sinh tự động",
              "pm.test(\"Response contains generated id\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-003 Create post with max length fields (short representation)",
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
          "raw": "{\n  \"userId\": 1,\n  \"title\": \"MAX_TITLE_255\",\n  \"body\": \"MAX_BODY_5000\"\n}"
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
              "// Kiểm tra API chấp nhận các trường độ dài lớn (đại diện)",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response echoes long title and body and contains id\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.title).to.eql(\"MAX_TITLE_255\");",
              "    pm.expect(jsonData.body).to.eql(\"MAX_BODY_5000\");",
              "    pm.expect(jsonData).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-004 Retrieve existing user",
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
              "// Kiểm tra dữ liệu người dùng hợp lệ",
              "pm.test(\"Response contains user object with id 1\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "    pm.expect(jsonData.id).to.eql(1);",
              "    pm.expect(jsonData).to.have.property('email');",
              "    pm.expect(jsonData.email).to.be.a('string');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-005 Retrieve user with non‑numeric id",
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
              "// Khi userId không phải số, API nên trả về lỗi (404 hoặc 400)",
              "pm.test(\"Status code is not 200\", function () {",
              "    pm.expect(pm.response.code).to.not.eql(200);",
              "});",
              "",
              "pm.test(\"Status code is 404 or 400\", function () {",
              "    pm.expect([404, 400]).to.include(pm.response.code);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-006 Create post with only required field",
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
          "raw": "{\n  \"userId\": 5\n}"
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
              "// Kiểm tra tạo bài viết chỉ với userId",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains userId 5 and generated id\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.userId).to.eql(5);",
              "    pm.expect(jsonData).to.have.property('id');",
              "    // title và body có thể không tồn tại",
              "    pm.expect(jsonData).to.not.have.property('title');",
              "    pm.expect(jsonData).to.not.have.property('body');",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
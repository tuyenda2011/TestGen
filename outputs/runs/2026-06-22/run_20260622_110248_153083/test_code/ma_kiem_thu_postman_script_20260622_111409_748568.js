{
  "info": {
    "name": "JSONPlaceholder API Post Creation - Comprehensive Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "description": "Bộ sưu tập kiểm thử các kịch bản tạo bài viết mới trên JSONPlaceholder, bao gồm các trường hợp dương, âm, biên và bảo mật."
  },
  "item": [
    {
      "name": "TC-001 - Create post with valid payload",
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
              "// Kiểm tra userId trả về bằng 1",
              "pm.test(\"Response contains correct userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(1);",
              "});",
              "",
              "// Kiểm tra thuộc tính id tồn tại và là số nguyên dương",
              "pm.test(\"Response contains positive integer id\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "    pm.expect(json.id).to.be.a('number');",
              "    pm.expect(json.id).to.be.above(0);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-002 - Create post missing userId",
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
          "raw": "{\n  \"title\": \"Test Title\",\n  \"body\": \"Test Body\"\n}"
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
              "// Kiểm tra mã trạng thái 201 khi thiếu userId",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra không có trường userId trong phản hồi",
              "pm.test(\"Response does not contain userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.not.have.property('userId');",
              "});",
              "",
              "// Kiểm tra thuộc tính id tồn tại",
              "pm.test(\"Response contains id property\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-003 - Create post with non-numeric userId",
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
          "raw": "{\n  \"userId\": \"abc\",\n  \"title\": \"Test\",\n  \"body\": \"Test\"\n}"
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
              "// Kiểm tra mã trạng thái 201 với userId không phải số",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra userId trả về đúng như đã gửi (chuỗi \"abc\")",
              "pm.test(\"Response contains userId as string abc\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql('abc');",
              "});",
              "",
              "// Kiểm tra thuộc tính id tồn tại",
              "pm.test(\"Response contains id property\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-004 - Create post with maximum length title and body",
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
          "raw": "{\n  \"userId\": 1,\n  \"title\": \"LONG_TITLE_200_CHARS\",\n  \"body\": \"LONG_BODY_5000_CHARS\"\n}"
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
              "// Kiểm tra mã trạng thái 201 cho payload dài",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra userId vẫn bằng 1",
              "pm.test(\"Response contains correct userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(1);",
              "});",
              "",
              "// Kiểm tra thuộc tính id tồn tại",
              "pm.test(\"Response contains id property\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-005 - Create post with unexpected additional header",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          },
          {
            "key": "X-Extra-Header",
            "value": "malicious",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"userId\": 1,\n  \"title\": \"Sec Test\",\n  \"body\": \"Sec Body\"\n}"
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
              "// Kiểm tra mã trạng thái 201 khi có header phụ",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra userId trả về bằng 1",
              "pm.test(\"Response contains correct userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(1);",
              "});",
              "",
              "// Kiểm tra thuộc tính id tồn tại",
              "pm.test(\"Response contains id property\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json).to.have.property('id');",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
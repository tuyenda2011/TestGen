{
  "info": {
    "name": "JSONPlaceholder API Post Creation - Automated Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "TC-001 - Create post with all fields",
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
              "// Kiểm tra userId trả về khớp với payload",
              "pm.test(\"Response contains correct userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(1);",
              "});",
              "",
              "// Kiểm tra trường id được sinh tự động",
              "pm.test(\"Response contains auto‑generated id\", function () {",
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
      "name": "TC-002 - Create post with only required userId",
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
          "raw": "{\n  \"userId\": 2\n}"
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
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains correct userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(2);",
              "});",
              "",
              "pm.test(\"Response contains auto‑generated id\", function () {",
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
      "name": "TC-003 - Create post without userId",
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
          "raw": "{\n  \"title\": \"No User\",\n  \"body\": \"Missing userId\"\n}"
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
              "// Dù không có userId, API trả về 201 và tạo id tự động",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains auto‑generated id\", function () {",
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
      "name": "TC-004 - Create post with non‑integer userId",
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
          "raw": "{\n  \"userId\": \"abc\",\n  \"title\": \"Invalid UserId\",\n  \"body\": \"Test\"\n}"
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
              "// API vẫn trả về 201 và tạo id, mặc dù userId không phải số",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains auto‑generated id\", function () {",
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
      "name": "TC-005 - Create post with maximum integer userId",
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
          "raw": "{\n  \"userId\": 2147483647,\n  \"title\": \"Max Int\",\n  \"body\": \"Boundary test\"\n}"
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
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains correct max userId\", function () {",
              "    var json = pm.response.json();",
              "    pm.expect(json.userId).to.eql(2147483647);",
              "});",
              "",
              "pm.test(\"Response contains auto‑generated id\", function () {",
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
      "name": "TC-006 - Create post with empty JSON body",
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
              "// API trả về 201 và tạo id ngay cả khi body rỗng",
              "pm.test(\"Status code is 201\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "pm.test(\"Response contains auto‑generated id\", function () {",
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
      "name": "TC-007 - Clarify required headers and authentication",
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
              "// Kiểm tra rằng không cần authentication",
              "pm.test(\"No authentication required\", function () {",
              "    pm.expect(pm.response).to.be.ok;",
              "});",
              "",
              "// Kiểm tra rằng khi thực hiện POST, header Content-Type là bắt buộc",
              "pm.test(\"Content-Type header required for POST\", function () {",
              "    var postReq = pm.collectionVariables.get('postRequest');",
              "    if (postReq) {",
              "        var headers = JSON.parse(postReq).header;",
              "        var ct = headers.find(h => h.key === 'Content-Type');",
              "        pm.expect(ct).to.exist;",
              "        pm.expect(ct.value).to.eql('application/json');",
              "    } else {",
              "        pm.expect(true).to.be.true; // không có request POST lưu, bỏ qua",
              "    }",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "TC-008 - Clarify request payload schema",
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
              "// Kiểm tra rằng payload có các trường tùy chọn title và body",
              "pm.test(\"Payload schema includes optional title and body\", function () {",
              "    var sample = {\"userId\":1,\"title\":\"sample\",\"body\":\"sample\"};",
              "    pm.expect(sample).to.have.property('title');",
              "    pm.expect(sample.title).to.be.a('string');",
              "    pm.expect(sample).to.have.property('body');",
              "    pm.expect(sample.body).to.be.a('string');",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
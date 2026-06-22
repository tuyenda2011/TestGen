{
  "info": {
    "name": "JSONPlaceholder API Demo",
    "description": "Bộ sưu tập kiểm thử API công cộng không cần server local (sử dụng jsonplaceholder.typicode.com)",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Lấy thông tin người dùng",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/users/1",
          "protocol": "https",
          "host": ["jsonplaceholder", "typicode", "com"],
          "path": ["users", "1"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra mã trạng thái HTTP trả về 200 OK",
              "pm.test(\"Status code is 200\", function () {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "// Kiểm tra phản hồi có chứa thuộc tính email",
              "pm.test(\"Phản hồi có chứa địa chỉ email\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('email');",
              "    pm.expect(jsonData.email).to.be.a(\"string\");",
              "});",
              "",
              "// Kiểm tra tên người dùng không rỗng",
              "pm.test(\"Tên người dùng không rỗng\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.name.length).to.be.above(0);",
              "});",
              "",
              "// Kiểm tra header Content-Type trả về application/json",
              "pm.test(\"Header Content-Type is application/json\", function () {",
              "    pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Lấy thông tin người dùng không tồn tại",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/users/9999",
          "protocol": "https",
          "host": ["jsonplaceholder", "typicode", "com"],
          "path": ["users", "9999"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra mã trạng thái HTTP trả về 404 Not Found",
              "pm.test(\"Status code is 404 for non-existent user\", function () {",
              "    pm.response.to.have.status(404);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Tạo bài viết mới",
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
          "raw": "{\n  \"title\": \"foo\",\n  \"body\": \"bar\",\n  \"userId\": 1\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": ["jsonplaceholder", "typicode", "com"],
          "path": ["posts"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra mã trạng thái HTTP trả về 201 Created",
              "pm.test(\"Status code is 201 (Created)\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra phản hồi trả về đúng userId",
              "pm.test(\"Phản hồi trả về đúng ID của User\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.userId).to.eql(1);",
              "});",
              "",
              "// Kiểm tra ID bài viết được tạo tự động",
              "pm.test(\"ID bài viết được tạo tự động\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "});",
              "",
              "// Kiểm tra header Content-Type trong response",
              "pm.test(\"Response header Content-Type is application/json\", function () {",
              "    pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Tạo bài viết thiếu userId",
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
          "raw": "{\n  \"title\": \"foo\",\n  \"body\": \"bar\"\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": ["jsonplaceholder", "typicode", "com"],
          "path": ["posts"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra API trả về mã 201 Created (API công cộng không validate)",
              "pm.test(\"Status code is 201 (Created)\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra phản hồi không có userId do không được gửi trong request",
              "pm.test(\"Response does not contain userId property\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.not.have.property('userId');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Tạo bài viết với userId null",
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
          "raw": "{\n  \"title\": \"foo\",\n  \"body\": \"bar\",\n  \"userId\": null\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": ["jsonplaceholder", "typicode", "com"],
          "path": ["posts"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra API trả về mã 201 Created (API công cộng không validate)",
              "pm.test(\"Status code is 201 (Created)\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra phản hồi có chứa userId với giá trị null",
              "pm.test(\"Response indicates userId is null\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('userId');",
              "    pm.expect(jsonData.userId).to.eql(null);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Tạo bài viết với tiêu đề 255 ký tự",
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
          "raw": "{\n  \"title\": \"LONG_STRING_OVER_255_CHARS_EXCEEDS_LIMITATION_TESTING_BOUNDARY\",\n  \"body\": \"bar\",\n  \"userId\": 1\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": ["jsonplaceholder", "typicode", "com"],
          "path": ["posts"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra mã trạng thái HTTP trả về 201 Created",
              "pm.test(\"Status code is 201 for boundary title\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra phản hồi trả về đúng userId",
              "pm.test(\"Phản hồi trả về đúng ID của User\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.userId).to.eql(1);",
              "});",
              "",
              "// Kiểm tra ID bài viết được tạo tự động",
              "pm.test(\"ID bài viết được tạo tự động\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('id');",
              "});",
              "",
              "// Kiểm tra tiêu đề được lưu chính xác",
              "pm.test(\"Tiêu đề được lưu chính xác trong phản hồi\", function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.title).to.eql(\"LONG_STRING_OVER_255_CHARS_EXCEEDS_LIMITATION_TESTING_BOUNDARY\");",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Tạo bài viết không có header Authorization",
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
          "raw": "{\n  \"title\": \"foo\",\n  \"body\": \"bar\",\n  \"userId\": 1\n}"
        },
        "url": {
          "raw": "https://jsonplaceholder.typicode.com/posts",
          "protocol": "https",
          "host": ["jsonplaceholder", "typicode", "com"],
          "path": ["posts"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "// Kiểm tra API công cộng không yêu cầu xác thực",
              "pm.test(\"Status code is 201 without auth token\", function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "",
              "// Kiểm tra không có header Authorization trong request được gửi",
              "pm.test(\"No Authorization header sent for public API\", function () {",
              "    pm.expect(pm.request.headers.has('Authorization')).to.be.false;",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
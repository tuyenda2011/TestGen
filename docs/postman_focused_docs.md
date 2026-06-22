# Postman Test Scripts & PM API Official Documentation

## 1. Overview
Postman allows you to write scripts in JavaScript that execute before a request (Pre-request Scripts) or after a response is received (Tests). 

The `pm` object is the core API provided by Postman for writing these scripts.

## 2. Basic Test Structure
Tests are written in the "Tests" tab using `pm.test()`.

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

## 3. Parsing JSON Responses
To assert against the response body, you usually parse it as JSON.

```javascript
pm.test("Response contains correct user ID", function () {
    // Parse the response body as JSON
    var jsonData = pm.response.json();
    
    // Use Chai assertions (pm.expect)
    pm.expect(jsonData.id).to.eql(123);
    pm.expect(jsonData.name).to.be.a("string");
    pm.expect(jsonData.roles).to.include("admin");
});
```

## 4. Variables
Postman variables allow you to share data between requests (Chaining requests).

### Setting Variables
You can extract a token from a login response and save it to the environment.
```javascript
var jsonData = pm.response.json();
pm.environment.set("auth_token", jsonData.token);
pm.collectionVariables.set("user_id", jsonData.id);
```

### Getting Variables
In a Pre-request Script or Test:
```javascript
var token = pm.environment.get("auth_token");
console.log("Using token: " + token);
```
In the Request Builder UI (URL, Headers, Body), you use curly braces: `{{auth_token}}`.

## 5. Pre-request Scripts
Executed *before* the request is sent. Useful for generating dynamic data or signing headers.

```javascript
// Generate a random email
var randomEmail = "user_" + _.random(1000, 9999) + "@example.com";
pm.environment.set("currentEmail", randomEmail);

// Add a dynamic header
pm.request.headers.add({
    key: "X-Timestamp",
    value: new Date().toISOString()
});
```

## 6. Chai Assertion Library (`pm.expect`)
Postman uses BDD-style assertions based on the Chai library.

```javascript
var data = pm.response.json();

pm.test("Advanced Assertions", function() {
    // Deep equality
    pm.expect(data).to.deep.equal({ success: true, count: 5 });
    
    // Existence
    pm.expect(data).to.have.property("users");
    
    // Length
    pm.expect(data.users).to.have.lengthOf(3);
    
    // Regex matching
    pm.expect(data.email).to.match(/^[^@]+@[^@]+\.[^@]+$/);
});
```

## 7. Branching and Workflows (Postman Runner)
When running a Collection via Postman Runner or Newman, you can control the flow.

```javascript
// Skip the next request and jump directly to "Get User Details"
pm.setNextRequest("Get User Details");

// To stop the execution entirely
pm.setNextRequest(null);
```

## 8. Sending Async Requests (`pm.sendRequest`)
You can trigger an HTTP request from within your script.
```javascript
pm.sendRequest("https://api.example.com/setup", function (err, res) {
    if (err) {
        console.log(err);
    } else {
        pm.environment.set("setup_id", res.json().id);
    }
});
```

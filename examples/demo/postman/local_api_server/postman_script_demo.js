pm.test("status is OK", function () {
  pm.response.to.have.status(200);
});

pm.test("response has total amount", function () {
  const body = pm.response.json();
  pm.expect(body).to.have.property("total");
  pm.expect(body.total).to.eql(100.5);
});

pm.test("response includes diagnostics", function () {
  const body = pm.response.json();
  pm.expect(body.diagnostics).to.have.property("discount");
  pm.expect(body.diagnostics).to.have.property("shipping");
});

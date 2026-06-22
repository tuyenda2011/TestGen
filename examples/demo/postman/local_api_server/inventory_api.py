from fastapi import FastAPI, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Local Inventory API")

class Item(BaseModel):
    name: str
    quantity: int
    price: float

class CheckoutReq(BaseModel):
    amount: int

db = {}
id_counter = 1

@app.post("/items")
def add_item(item: Item):
    global id_counter
    if item.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    for v in db.values():
        if v["name"] == item.name:
            raise HTTPException(status_code=409, detail="Item already exists")
    
    db[id_counter] = item.dict()
    db[id_counter]["id"] = id_counter
    id_counter += 1
    return db[id_counter - 1]

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

@app.post("/items/{item_id}/checkout")
def checkout_item(item_id: int, req: CheckoutReq, authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if authorization != "Bearer secret-token":
        raise HTTPException(status_code=403, detail="Invalid token")
        
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
        
    item = db[item_id]
    if req.amount > item["quantity"]:
        raise HTTPException(status_code=400, detail="Not enough stock")
        
    item["quantity"] -= req.amount
    return {"message": "Checkout successful", "remaining_stock": item["quantity"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

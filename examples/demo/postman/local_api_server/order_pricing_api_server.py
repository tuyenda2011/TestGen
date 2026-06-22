from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from typing import Any


HOST = "127.0.0.1"
PORT = 8000


def _round_money(value: float) -> float:
    return round(float(value) + 1e-9, 2)


def _discount(subtotal: float, tier: str) -> float:
    normalized = tier.strip().lower()
    if normalized == "standard":
        return 0.0
    if normalized == "loyal":
        return min(subtotal * 0.07, 30.0)
    if normalized == "vip":
        return min(subtotal * 0.12, 50.0)
    raise ValueError("unsupported customerTier")


def _shipping(weight_kg: float, destination: str, fragile: bool) -> float:
    if weight_kg <= 0:
        raise ValueError("weightKg must be greater than zero")
    normalized = destination.strip().lower()
    if normalized == "domestic":
        fee = 5.0
    elif normalized == "international":
        fee = 18.0
    else:
        raise ValueError("unsupported destination")
    if weight_kg > 20:
        fee += 25.0
    elif weight_kg > 5:
        fee += 10.0
    if fragile:
        fee += 7.5
    return fee


def quote_order(payload: dict[str, Any]) -> dict[str, Any]:
    if "subtotal" not in payload:
        raise ValueError("subtotal is required")
    subtotal = float(payload["subtotal"])
    if subtotal < 0:
        raise ValueError("subtotal must not be negative")
    weight_kg = float(payload.get("weightKg", 0))
    destination = str(payload.get("destination", ""))
    customer_tier = str(payload.get("customerTier", "standard"))
    fragile = bool(payload.get("fragile", False))
    store_credit = float(payload.get("storeCredit", 0))
    if store_credit < 0:
        raise ValueError("storeCredit must not be negative")

    discount = _discount(subtotal, customer_tier)
    shipping = _shipping(weight_kg, destination, fragile)
    total_before_credit = subtotal - discount + shipping
    total = max(0.0, total_before_credit - store_credit)
    return {
        "total": _round_money(total),
        "diagnostics": {
            "discount": _round_money(discount),
            "shipping": _round_money(shipping),
            "totalBeforeCredit": _round_money(total_before_credit),
        },
    }


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/orders/quote":
            self._send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw_body or "{}")
            result = quote_order(payload)
        except (ValueError, json.JSONDecodeError, TypeError) as exc:
            self._send_json(400, {"error": str(exc)})
            return
        self._send_json(200, result)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        self._send_json(404, {"error": "not found"})

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Postman demo API listening on http://localhost:{PORT}", flush=True)
    print("Endpoint: POST /orders/quote", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

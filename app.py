app.py from flask import Flask, request
import hmac
import hashlib
import json

app = Flask(__name__)
IPN_KEY = b"YOUR_IPN_SECRET_KEY"

@app.route('/api/ipn', methods=['POST'])
def handle_ipn():
    raw = request.get_data()
    signature = request.headers.get('x-nowpayments-sig')
    hashed = hmac.new(IPN_KEY, raw, hashlib.sha512).hexdigest()
    
    if hashed != signature:
        return "Invalid signature", 403
    
    data = json.loads(raw)
    print("✅ Получено:", data.get("payment_status"), "| Заказ:", data.get("order_id"))
    return "OK", 200

if __name__ == "__main__":
    app.run()

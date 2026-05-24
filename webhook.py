from flask import Flask, request
import stripe
import requests

stripe.api_key = "sk_test_51TaeBvQ9L3hu9VrYM1ChOrpmO4K1k2AKLeX8IXLEaNnQZiizuleF1IA3GbfR74FjGW4XYQEgPehButBrENKw8YYN00O2cVM3Rr"
STRIPE_SECRET = "whsec_5Cn0ClI8YcYtN8MEI0Xge55dlWVfz737"
BOT_TOKEN = "8948433286:AAHX9RxtNKKF_MF25PGV6WS2d2aCrlrm3GI"
LINK_A_ENTREGAR = "https://shop1850859027.v.weidian.com/item.html?itemID=7611475251"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_SECRET
        )
    except Exception as e:
        return str(e), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        chat_id = session["client_reference_id"]

        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": LINK_A_ENTREGAR}
        )

    return "OK", 200

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)





import database as db
from flask import session, request
from datetime import datetime

def create_tier_purchase():
    purchase = {}
    purchase.setdefault("username",session["user"]["username"])
    purchase.setdefault("orderdate",datetime.utcnow())
    purchase_details = []
    cart = session["cart"]
    for key, value in cart.items():
        purchase_details.append({"code":key,
                            "name":value["name"],
                            "subtotal":value["subtotal"],
                            "paymentmethod":value["payment"]})
    purchase.setdefault("details",purchase_details)
    db.create_purchase(purchase)

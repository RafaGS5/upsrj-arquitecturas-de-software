# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: app.py
# Descripción: Backend del microservicio
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template
import requests
from common.utils import get_host
from common.vars import GATEWAY_SERVICE_URL, USER_API_URL, PRODUCT_API_URL, PURCHASES_API_URL, PURCHASE_SERVICE_URL
import requests


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/all')
def get_all():
    try:
        users_resp = requests.get(f"{USER_API_URL}/api/users")
        products_resp = requests.get(f"{PRODUCT_API_URL}/api/products")
        purchases_resp = requests.get(f"{PURCHASES_API_URL}/api/purchases")

        users = users_resp.json()
        products = products_resp.json()
        purchases = purchases_resp.json()

        product_by_id = {p['id']: p for p in products}

        users_with_purchases = []
        for u in users:
            purchased_products = []
            seen = set()
            for pr in purchases:
                if pr.get('user_id') == u.get('id'):
                    pid = pr.get('product_id')
                    prod = product_by_id.get(pid)
                    if prod and pid not in seen:
                        purchased_products.append({"id": prod["id"], "name": prod["name"]})
                        seen.add(pid)
            users_with_purchases.append({
                "user": {"id": u["id"], "name": u["name"]},
                "purchased_products": purchased_products
            })
        
        return render_template(
        "all.html",
        users=users,
        products=products,
        purchases=purchases,
        users_with_purchases=users_with_purchases,
        )



#       return render_template("all.html", users=users, products=products, purchases=purchases)

    except requests.exceptions.RequestException as e:
        return render_template("error.html", error=str(e)), 500


@app.route('/purchases/<int:user_id>', methods=['GET'])
def gw_get_purchases_by_user(user_id):
    # Proxy al servicio de compras para renderizar ahí mismo
    resp = requests.get(f"{PURCHASE_SERVICE_URL}/purchases/{user_id}")
    return (resp.text, resp.status_code, resp.headers.items())

if __name__ == '__main__':
    app.run(port=get_host(GATEWAY_SERVICE_URL))
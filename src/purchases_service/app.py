# src/purchases_service/app.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, redirect, url_for
from common.utils import load_item, save_item, get_host
from common.vars import PURCHASES_FILE, PURCHASE_SERVICE_URL, USERS_FILE, PRODUCTS_FILE
from datetime import datetime

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = load_item(PURCHASES_FILE)
    return render_template("purchases.html", purchases=purchases)

@app.route('/purchases/create', methods=['GET'])
def create_purchase_form():
    users = load_item(USERS_FILE)
    products = load_item(PRODUCTS_FILE)
    return render_template("create_purchase.html", users=users, products=products)

@app.route('/purchases', methods=['POST'])
def create_purchase():
    user_id = request.form.get("user_id")
    product_id = request.form.get("product_id")

    if not user_id:
        return "user_id", 400
    if not product_id:
        return "product_id", 400

    users = load_item(USERS_FILE)
    products = load_item(PRODUCTS_FILE)
    if int(user_id) not in [int(u["id"]) for u in users]:
        return "user_id", 400
    if int(product_id) not in [int(p["id"]) for p in products]:
        return "product_id", 400

    purchases = load_item(PURCHASES_FILE)
    purchase = {
        "id": int(len(purchases) + 1),
        "user_id": int(user_id),
        "product_id": int(product_id),
        "timestamp": datetime.now().isoformat()
    }
    purchases.append(purchase)
    save_item(PURCHASES_FILE, purchases)
    return redirect(url_for('get_purchases'))

# >>> ESTA ES LA RUTA QUE PIDE EL TEST <<<
@app.route('/purchases/<int:user_id>', methods=['GET'])
def get_purchases_by_user(user_id):
    users = load_item(USERS_FILE)
    if int(user_id) not in [int(u["id"]) for u in users]:
        # El test no prueba el caso inválido, pero es correcto devolver 400 si el usuario no existe
        return "user_id", 400

    purchases = load_item(PURCHASES_FILE)
    user_purchases = [p for p in purchases if int(p["user_id"]) == int(user_id)]
    return render_template("purchases.html", purchases=user_purchases)

if __name__ == '__main__':
    app.run(port=get_host(PURCHASE_SERVICE_URL))

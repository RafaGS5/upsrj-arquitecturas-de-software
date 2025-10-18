# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API de microservicio
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
import requests
from common.utils import get_host
from common.vars import GATEWAY_API_URL, USER_API_URL, PRODUCT_API_URL ,PURCHASES_API_URL 
import requests

app = Flask(__name__)

@app.route('/api/all')
def get_all():
    try:
        users_resp = requests.get(f"{USER_API_URL}/api/users")
        products_resp = requests.get(f"{PRODUCT_API_URL}/api/products")
        purchases_resp = requests.get(f"{PURCHASES_API_URL}/api/purchases")

        users = users_resp.json()
        products = products_resp.json()
        purchases = purchases_resp.json()

        product_by_id = {p['id']: p for p in products}

        result = []
        for u in users:
            u_purchases = [p for p in purchases if p.get('user_id') == u.get('id')]
            purchased_products = []
            seen = set()
            for p in u_purchases:
                pid = p.get('product_id')
                prod = product_by_id.get(pid)
                if prod and pid not in seen:
                    purchased_products.append({"id": prod['id'], "name": prod['name']})
                    seen.add(pid)
            result.append({
                "user": {"id": u['id'], "name": u['name']},
                "purchased_products": purchased_products
            })

#si no tienes compras se utiliza eso, evitando que se rompa
#        user_id = requests.args.get('user_id', None)
#        if user_id:
#            try:
#                uid = int(user_id)
#            except ValueError:
#                return jsonify({"error": "user_id must be integer"}), 400
#            for entry in result:
#                if entry['user']['id'] == uid:
#                    return jsonify(entry)
#            return jsonify({"error": "user not found"}), 404
#
#        return jsonify(result)

#        return jsonify({
#            "users": users,
#            "products": products,
#            "purchases": purchases
#        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Error comunicando con microservicios",
            "details": str(e)
        }), 500



if __name__ == '__main__':
    app.run(port=get_host(GATEWAY_API_URL))


    
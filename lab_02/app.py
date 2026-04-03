from flask import Flask, jsonify, request

app = Flask(__name__)

# Список продуктов (в памяти)
products = [
    {"id": 1, "name": "Milk", "price": 80, "stock": 10},
    {"id": 2, "name": "Bread", "price": 50, "stock": 20}
]

# следующий id
next_id = 3


# Получить все продукты
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})


# Получить продукт по id
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


# Создать новый продукт
@app.route('/api/products', methods=['POST'])
def create_product():
    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    new_product = {
        "id": next_id,
        "name": data.get("name"),
        "price": data.get("price"),
        "stock": data.get("stock")
    }

    products.append(new_product)

    next_id += 1

    return jsonify(new_product), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
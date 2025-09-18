from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Demo product data
products = [
    {"id": 1, "name": "T-shirt", "price": 19.99, "image": "/static/assets/images/product-1.jpg"},
    {"id": 2, "name": "Cap", "price": 9.99, "image": "/static/assets/images/product-2.jpg"},
    {"id": 3, "name": "Sneakers", "price": 49.99, "image": "/static/assets/images/product-3.jpg"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/products")
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    # 👇 switched to port 8080
    app.run(host="0.0.0.0", port=8080)


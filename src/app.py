from flask import Flask, render_template, request, redirect, url_for

from src.utilities.database import Database
from src.models.product import Product

app = Flask(__name__)
db = Database('legit')

@app.route('/')
def index():
    return redirect(url_for('products'))

@app.route('/products')
def products():
    keyword = request.args.get('search', '')
    keyword = keyword.strip().lower()

    print("Keyword:", keyword)

    rows = db.execute_query(
        "SELECT * FROM Product WHERE lower(name) LIKE ('%" + keyword + "%') ORDER BY name;"
    )

    products = []

    try:
        for row in rows:
            product = Product(row[0], row[1], row[2], row[3], row[4])
            products.append(product)
    except Exception as e:
        return "ERROR: " + str(e)

    count = len(products) if keyword else None

    return render_template('index.html', products=products, count=count, keyword=keyword)

@app.route('/products/<uid>')
def product(uid):
    rows = db.execute_query(
        "SELECT * FROM Product WHERE id = " + str(uid) + ";"
    )

    try:
        row = rows.pop(0)
        product = Product(row[0], row[1], row[2], row[3], row[4])
        return render_template('product.html', product=product)

    except Exception as e:
        return "ERROR: " + str(e)


### Entry point.

if __name__ == "__main__":
    # Switch methods for deployment.
	# app.run(host='0.0.0.0')
    app.run()

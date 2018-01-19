from flask import Flask, render_template, request, redirect, url_for, session, abort

from src.utilities.database import Database
from src.utilities.password import PasswordUtility
from src.models.product import Product
from src.models.account import Account

app = Flask(__name__)
app.secret_key = "legit-secret-key"
db = Database('legit')
pw = PasswordUtility()


### Convenience methods for session. ###

def signed_in():
    return session['signed_in'] if 'signed_in' in session else False

def admin_session() -> bool:
    return session['admin'] if 'admin' in session else False

def set_signed_in(username, email, password, admin):
    session['signed_in'] = True
    session['fresh'] = True
    session['username'] = username
    session['email'] = email
    session['password'] = password
    session['admin'] = admin


### Routes. ###

@app.route('/')
def index():
    return redirect(url_for('products'))

@app.route('/products')
def products():
    keyword = request.args.get('search', '')
    keyword = keyword.strip()

    rows = db.execute_query(
        "SELECT * FROM Product WHERE lower(name) LIKE lower('%" + keyword + "%') ORDER BY lower(name);"
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

@app.route('/products/<uid>/delete', methods=['POST'])
def delete_product(uid):
    if not admin_session():
        abort(403)
    
    db.execute_update(
        "DELETE FROM Product WHERE id = (" + uid + ");"
    )

    return redirect(url_for('products'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if signed_in():
        return redirect(url_for('account'))

    if request.method == 'GET':
        return render_template('login.html', messages=None)
    else:
        username, password = request.form['username'], request.form['password']

        username = username.strip().lower()

        rows = db.execute_query(
            "SELECT * FROM Account WHERE username = %(username)s;",
            {'username': username}
        )

        try:
            row = rows.pop(0)

            stored_hash = row[2]

            if pw.matches(password, stored_hash):
                account = Account(row[0], row[1], row[2], row[3])
                set_signed_in(account.username, account.email, account.password, account.admin)
                return redirect(url_for('account'))

            else:
                error = "Incorrect username or password."
                return render_template('login.html', messages={'error': error}, username=username)    

        except Exception as e:
            error = "Incorrect username or password."
            return render_template('login.html', messages={'error': error}, username=username)

@app.route('/logout', methods=['POST'])
def logout():
    if not signed_in():
        abort(401)
    
    session.pop('signed_in', None)
    session.pop('fresh', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('password', None)
    session.pop('admin', None)

    return redirect(url_for('login'))

@app.route('/account')
def account():
    # account = Account(session['username'], session['password'], session['admin']) if signed_in() else None
    account = None
    messages = None

    if all(key in session for key in ('username', 'email', 'password', 'admin')):
        account = Account(session['username'], session['email'], session['password'], session['admin'])

    if 'fresh' in session:
        messages = {'welcome': "Welcome!"}
    
    return render_template('account.html', account=account, messages=messages)


### Entry point.

if __name__ == "__main__":
    # Switch methods for deployment.
	# app.run(host='0.0.0.0')
    app.run()

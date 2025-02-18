from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import datetime

app = Flask(__name__)

# Secret Key for Hashing (Keep as-is, it's tuned to the database's current data)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'NateNate3.00'
app.config['MYSQL_PASSWORD'] = 'FunnyPassword321'
app.config['MYSQL_DB'] = '180_final'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def verify():
    if 'loggedin' in session:
        return redirect('/logout')
    else:
        return render_template('confirmation.html')


@app.route('/login')
def base():
    return render_template('logintemplate.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Error
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for access
        email = request.form['email']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
                # Check Count Validity
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()
                # If account exists
        if account:
            # Create session data
            session['loggedin'] = True
            session['id'] = account['userId']
            session['email'] = account['email']
            session['firstname'] = account['firstName']
            session['lastname'] = account['lastName']
            session['accountType'] = account['accountType']
            # Redirect to home page
            return redirect('/products')
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'
    return render_template('/logintemplate.html', msg=msg)


@app.route('/logout')
def logout():
    # Log Out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   session.pop('firstname', None)
   session.pop('lastname', None)
   session.pop('accountType', None)
   # Redirect to login page
   return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Error Message
    msg = ''
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        accounttype = request.form['accounttype']


                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the users table
            cursor.execute('INSERT INTO users (email, password, firstname, lastname, accounttype) VALUES (%s, %s, %s, %s, %s)', (email, password, firstname, lastname, accounttype))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('logintemplate.html', msg=msg)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('registertemplate.html', msg=msg)

@app.route('/products')
def products():

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT p.*, d.discAmt, d.duration
        FROM products p
        LEFT JOIN discounts d ON p.productId = d.productId
        WHERE p.productId NOT IN (SELECT productId FROM deleted_products)
        AND (d.duration IS NULL OR d.duration >= %s)
    ''', (current_date,))
    products = cursor.fetchall()
    return render_template('products.html', products=products)


@app.route('/vodka')
def vodka():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT p.*, d.discAmt, d.duration
        FROM products p
        LEFT JOIN discounts d ON p.productId = d.productId
        WHERE p.categoryId = 1 
        AND p.productId NOT IN (SELECT productId FROM deleted_products)
        AND (d.duration IS NULL OR d.duration >= %s)
    ''', (current_date,))
    products = cursor.fetchall()
    return render_template('vodka.html', products=products)

@app.route('/whiskey')
def whiskey():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT p.*, d.discAmt, d.duration
        FROM products p
        LEFT JOIN discounts d ON p.productId = d.productId
        WHERE p.categoryId = 2 
        AND p.productId NOT IN (SELECT productId FROM deleted_products)
        AND (d.duration IS NULL OR d.duration >= %s)
    ''', (current_date,))
    products = cursor.fetchall()
    return render_template('whiskey.html', products=products)

@app.route('/tequila')
def tequila():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT p.*, d.discAmt, d.duration
        FROM products p
        LEFT JOIN discounts d ON p.productId = d.productId
        WHERE p.categoryId = 3 
        AND p.productId NOT IN (SELECT productId FROM deleted_products)
        AND (d.duration IS NULL OR d.duration >= %s)
    ''', (current_date,))
    products = cursor.fetchall()
    return render_template('tequila.html', products=products)

@app.route('/create/', methods = ['GET', 'POST'])
def create_product():
    if request.method == 'GET':
        return render_template('add_product.html')

    if request.method == 'POST':
        userId = session['id']
        prodName = request.form['prodName']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']
        stock = request.form['stock']
        categoryId = request.form['categoryID']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO products (userId, prodName, price, prodDesc, image, stock, categoryId) VALUES (%s, %s, %s, %s, %s, %s, %s)', (userId, prodName, price, description, image, stock, categoryId))
        
        mysql.connection.commit()
        return redirect('/products')


@app.route('/drinks/<int:productId>', methods=['GET', 'POST'])
def drinks(productId):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT p.*, d.discAmt, d.duration
        FROM products p
        LEFT JOIN discounts d ON p.productId = d.productId
        WHERE p.productId = %s
        AND p.productId NOT IN (SELECT productId FROM deleted_products)
        AND (d.duration IS NULL OR d.duration >= %s)
    ''', (productId, current_date,))
    product = cursor.fetchone()
    cursor.execute('SELECT * FROM reviews WHERE productId = %s', (productId,))
    reviews = cursor.fetchall()

    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        userId = session['id']

        cursor.execute('SELECT * FROM Cart WHERE productId = %s AND userId = %s', (productId, userId))
        existing_entry = cursor.fetchone()

        if existing_entry:
            new_quantity = existing_entry['quantity'] + quantity
            cursor.execute('UPDATE Cart SET quantity = %s WHERE productId = %s AND userId = %s',
                           (new_quantity, productId, userId))
        else:
            cursor.execute('INSERT INTO Cart (productId, userId, quantity) VALUES (%s, %s, %s)',
                           (productId, userId, quantity))

        mysql.connection.commit()
        return redirect(url_for('products'))

    return render_template('drinks.html', product=product, reviews=reviews)

@app.route('/submit_review/<int:productId>', methods=['POST'])
def submit_review(productId):
    review_data = request.json  #json for requesting review data
    userId = int(review_data.get('userId'))
    name = review_data.get('name')
    rating = float(review_data.get('rating'))
    review_text = review_data.get('review')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO reviews (productId, userId, name, rating, description) VALUES (%s, %s, %s, %s, %s)',
                   (productId, userId, name, rating, review_text))
    mysql.connection.commit()
    #JSONIFY JUST SHOWS A MESSAGE SO YOU WILL HAVE TO ADD jsonify INTO the import on the first line
    return jsonify({'message': 'Review submitted successfully'}), 200


@app.route('/cart')
def shopping_cart():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = (session['id'],)
    cursor.execute('SELECT products.prodName, products.image, products.price, cart.userId, cart.productId, cart.quantity FROM cart JOIN products ON products.productId = cart.productId where cart.userId = %s', (user_id))
    cart_items = cursor.fetchall()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    product_id = request.form['product_id']
    user_id = session['id']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM cart WHERE userId = %s AND productId = %s', (user_id, product_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('shopping_cart'))



@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_id = session['id']
        
        cursor.execute('INSERT INTO orders (userId) VALUES (%s)', (user_id,))
        mysql.connection.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID() AS orderId")
        order_id = cursor.fetchone()['orderId']
        
        cursor.execute('SELECT productId FROM cart WHERE userId = %s', (user_id,))
        product_ids = cursor.fetchall()
        
        for product_id in product_ids:
            cursor.execute('INSERT INTO orderitems (orderId, productId) VALUES (%s, %s)', (order_id, product_id['productId']))
            mysql.connection.commit()
        
        cursor.close()
        return redirect(url_for('store'))
    except Exception as e:
        # Handle exceptions
        print("Error:", e)
        mysql.connection.rollback()
        return redirect(url_for('shopping_cart'))  # Redirect back to the cart page
    

@app.route('/user_order_action')
def request_action():
    return render_template('user_order_action.html')

@app.route('/useraccount/')
def profile():
    # user info
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['id']
    cursor.execute('SELECT * FROM users WHERE userID = %s', (user_id,))
    users = cursor.fetchone()

    # gets orders
    cursor.execute("SELECT * FROM orders WHERE userId = %s", (user_id,))
    orders = cursor.fetchall()

    return render_template('useraccount.html', users=users, orders=orders)



@app.route('/vendor_orders/')
def vendor_orders():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['id']
    cursor.execute('SELECT * FROM orders WHERE userID = %s', (user_id,))
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return render_template('vendor_orders.html', users=users, orders=orders)

@app.route('/update_status/', methods=['GET', 'POST'])
def update_status():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_id = session['id']
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        return render_template('vendor_orders.html', orders=orders)

    if request.method == 'POST':
        new_status = request.form['new_status']
        order_id = request.form['order_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE orders SET status = %s WHERE orderid = %s', (new_status, order_id))
        mysql.connection.commit()
        return redirect(url_for('vendor_orders'))

    return redirect(url_for('vendor_orders'))


@app.route('/vendor/claim/', methods=['GET', 'POST'])
def update_claim():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_id = session['id']
        cursor.execute('SELECT * FROM claims WHERE customerId = %s', (user_id,))
        claims = cursor.fetchall()
        return render_template('vendor_claims.html', claims = claims)

    if request.method == 'POST':
        claim_status = request.form['status']
        complaint_id = request.form['claim_id']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE claims SET status = %s WHERE complaintId = %s', (claim_status, complaint_id))
        mysql.connection.commit()
    
    return redirect(url_for('update_claim'))

@app.route('/vendor/account')
def vendor_account():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE userId = %s', (session['id'],))
    users = cursor.fetchone()
    cursor.execute('SELECT * FROM products where userId = %s AND productId NOT IN (SELECT productId FROM deleted_products)', (session['id'],))

    products = cursor.fetchall()
    return render_template('vendoraccount.html', users = users, products = products)


@app.route('/product/edit/<id>', methods = ['GET', 'POST'])
def product_edit(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM products where productId = %s', (id,))
        product = cursor.fetchone()
        return render_template('edit_product.html', product = product)
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        productId = request.form['id']
        prodName = request.form['prodName']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']
        stock = request.form['stock']
        cursor.execute('UPDATE products SET prodName = %s, price = %s, prodDesc = %s, image = %s, stock = %s WHERE productId = %s', (prodName, price, description, image, stock, productId))
        mysql.connection.commit()
        return redirect('/vendor/account')


@app.route('/product/delete/<id>')
def product_delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO deleted_products (productId) VALUES (%s)', (id))
    mysql.connection.commit()
    return redirect('/products')


@app.route('/product/add/discount/<id>', methods=['GET', 'POST'])
def add_discount(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM products WHERE productId = %s', (id,))
        product = cursor.fetchone()
        return render_template('discounts.html', product=product)
    
    elif request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        amount = request.form['amount']
        productId = request.form['id']
        duration = request.form['duration']

        cursor.execute('SELECT * FROM discounts WHERE productId = %s', (productId,))
        existing_discount = cursor.fetchone()

        if existing_discount:
            if duration:
                cursor.execute('UPDATE discounts SET discAmt=%s, duration=%s WHERE productId=%s', (amount, duration, productId))
            else:
                cursor.execute('UPDATE discounts SET discAmt=%s WHERE productId=%s', (amount, productId))
            
        else:
            if duration:
                cursor.execute('INSERT INTO discounts (discAmt, productId, duration) VALUES (%s, %s, %s)', (amount, productId, duration))
            else:
                cursor.execute('INSERT INTO discounts (discAmt, productId) VALUES (%s, %s)', (amount, productId))

        mysql.connection.commit()

        return redirect('/vendor/account')


@app.route('/acc_check/')
def header_account_check():
    if session['loggedin'] == True:
        if session['accountType'] == 'vendor':
                return redirect('/vendor/account')
        elif session['accountType'] == 'customer':
            return redirect('/useraccount')

    return redirect(url_for('products'))


if __name__ == '__main__':
    app.run(debug=True)
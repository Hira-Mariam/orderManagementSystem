from flask import Flask, request, jsonify,render_template
from flask_mysqldb import MySQL


app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def home():
    return "Welcome to the Order Management System!"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '**********'
app.config['MYSQL_DB'] = 'order_management'

mysql = MySQL(app)

# Define your routes and API logic here
# Register a user
@app.route('/registeruser', methods=['POST','GET'])
def register_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "User registered successfully"}), 201

# Get all products
@app.route('/getallproducts', methods=['GET'])
def get_all_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return jsonify(products), 200

# Add a product
@app.route('/addproduct', methods=['POST'])
def add_product():
    data = request.json
    name = data['name']
    description = data['description']
    price = data['price']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)", (name, description, price))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Product added successfully"}), 201

# Update a product
@app.route('/updateproduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data['name']
    description = data['description']
    price = data['price']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE products SET name=%s, description=%s, price=%s WHERE id=%s", (name, description, price, product_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Product updated successfully"}), 200

# Delete a product
@app.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Product deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)

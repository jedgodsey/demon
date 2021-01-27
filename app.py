from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import *
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localhost/wutang'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

#init ma
ma = Marshmallow(app)

#product Class/Model


# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# init schema
product_schema = ProductSchema() #strict=True?
products_schema = ProductSchema(many=True) #strict=True?

@app.route('/', methods=['GET'])
def get():
    return jsonify({'big': 'small'})

@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# get one product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    db.session.commit()
    return product_schema.jsonify(product)

# delete
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

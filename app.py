from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localhost/wutang'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localhost/testing'  #works kindof


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:password@host:port/dbname'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLITE:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

#init ma
ma = Marshmallow(app)

#product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

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
    # return jsonify(result.data)

# get one product
@app.route('/product/<id>', methods=['GET'])
def get_product():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    print('your result: ', result)
    return jsonify(result)
    # return jsonify(result.data)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

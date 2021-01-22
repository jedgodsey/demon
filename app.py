from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localhost/testing'
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
        self.description = descriptionse
        self.price = price
        self.qty = qty

# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# init schema
product_schema = ProductSchema() #strict=True?
products_schema = ProductSchema(many=True,) #strict=True?

@app.route('/', methods=['GET'])
def get():
    return jsonify({'big': 'small'})

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

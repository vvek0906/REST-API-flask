from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__)) #gets parent directory

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite') #The database URI that should be used for the connection. Examples:
#sqlite:////tmp/test.db
#mysql://username:password@server/db

app.config['SQLALCHEMY_TRACK_ALCHEMY'] = False

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app) #binds sqlalchemy to app and create a db. Communicates between python programs and db. Its an object relational mapping library.Most of the times, 
#this library is used as an Object Relational Mapper (ORM) tool that translates Python classes to tables on relational databases and 
#automatically converts function calls to SQL statements.

ma = Marshmallow(app) #Marshmallow is a Python library which enables us to easily sanitize and validate content according to a schema. 
#Marshmallow is an object serialization/deserialization library.Flask-Marshmallow is a thin integration layer for Flask (a Python web framework) and marshmallow.

class Product(db.Model): # create a model for our db . Inherit base class of sqlalchemy db.Model.
    # db columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        
#Define your output format with marshmallow.
class productSchema(ma.Schema): # defines how and what in our serialized response is going to be present.
    # Fields to expose
    class Meta:
        fields = ('id','name','description','price','qty')

product_schema = productSchema()
products_schema = productSchema(many=True)

#creating a product
@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#getting a product
@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

#getting a specified product
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)
    
#updating a product
@app.route('/product/<id>',methods=['PUT'])
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

#deleting a product
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

if __name__ == '__main__':
    app.run(debug=True)

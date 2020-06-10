from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os 

#init app 
app = Flask(__name__) 
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#Init db 
db = SQLAlchemy(app) 

#Init marshmallow 
ma = Marshmallow(app) 

#Product Class/Model 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name 
        self.description = description 
        self.price = price 
        self.quantity = quantity

# Product Schema 
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')

#Init Schema 
# product_schema = ProductSchema(strict=True)
# products_schema = ProductSchema(strict=True, many=True)

product_schema = ProductSchema()
products_schema = ProductSchema( many=True)

#Create a Product 
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price'] 
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#Get All Products 
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


#Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    product.name = request.json['name']
    product.description = request.json['description'] 
    product.price = request.json['price']
    product.quantity = request.json['quantity'] 

    db.session.commit()

    return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    
    db.session.delete(product)
    db.session.commit()

    message = {"Message": "The Product with ID: " + id+" was deleted!"}

    return message

#Run server 
if __name__== '__main__': 
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
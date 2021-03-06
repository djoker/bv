from datetime import datetime
from passlib.apps import custom_app_context
from bvapi import db
import json

def to_json(inst, cls):
    """
    Create a json from a register
    (from https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask/7103486)
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True, nullable=False)
    created  = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    def todict(self):
        ret = {}
        ret["id"] = self.id       
        ret["userid"] = self.userid   
        ret["name"] = self.name     
        ret["email"] = self.email    
        return ret
        
    def __repr__(self):
        return "UID: {u}".format(u=self.userid)

    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(120))
    orders = db.relationship("Order")
    created  = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)
    
    @property
    def todict(self):
        ret={}
        ret["id"] = self.id       
        ret["name"] = self.name        
        ret["email"] = self.email   
        ret["address"] = self.address 
        return ret

    def __repr__(self):
        return "Name: {n}".format(n=self.name)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, default=0.00)
    created  = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    @property
    def todict(self):
        ret = {}
        ret["id"] = self.id      
        ret["product"] = self.product 
        ret["price"] = self.price
        return ret

    def __repr__(self):
        return "Product: {p}".format(p=self.product)


class Order(db.Model):
    __tablename__ = 'orders'
    nro = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    items = db.relationship("Order_item")
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return "Order: {n}".format(n=self.nro)

    @property
    def json(self):
        return to_json(self, self.__class__)

class Order_item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_nro = db.Column(db.Integer, db.ForeignKey('orders.nro'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    amount = db.Column(db.Float, default=0.00)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    @property
    def json(self):
        return to_json(self, self.__class__)

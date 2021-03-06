from flask_restful import Api, Resource
from flask import request
import bvapi.model as m
from bvapi import app, db

api = Api(app)

class Client(Resource):
    def get(self, pid=0):
        ret = []
        if pid == 0:
            rClients = m.Client.query.all()
        else:
            rClients = m.Client.query.filter_by(id=pid).all()
        for reg in rClients:
            ret.append(reg.todict)
        rcode = 200 if len(ret) > 0 else 404
        
        return ret, rcode

    def post(self):
        reg = m.Client()
        reg.name = request.form['name']
        reg.address = request.form['address']
        reg.email = request.form['email']
        try:
            db.session.add(reg)
            db.session.commit()
            return {"msg":"Produto incluido"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}
        
    def put(self, pid):
        try:
            reg = m.Client.query.filter_by(id=pid).first()
            reg.name = request.form['name'] if 'name' in request.form.keys() else reg.name
            reg.address = request.form['address'] if 'address' in request.form.keys()  else reg.address
            reg.email = request.form['email'] if 'email' in request.form.keys() else reg.email
            db.session.add(reg)
            db.session.commit()
            return {"msg":"Produto alterado"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}, 500
        
    def delete(self, pid):
        reg = m.Client.query.filter_by(id=pid).first()
        try:
            db.session.delete(reg)
            db.session.commit()
            return {"msg":"Produto excluido"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}, 500
        
        
class Product(Resource):

    def get(self, pid=0):
        ret = []
        if pid == 0:
            rProducts = m.Product.query.all()
        else:
            rProducts = m.Product.query.filter_by(id=pid).all()
        for reg in rProducts:
            ret.append(reg.todict)
        rcode = 200 if len(ret) > 0 else 404
        
        return ret, rcode

    def post(self):
        reg = m.Product()
        reg.product = request.form['product']
        reg.price = request.form['price']

        print(reg.todict)
        try:
            db.session.add(reg)
            db.session.commit()
            return {"msg":"Produto incluido"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}
        
    def put(self, pid):
        try: 
            reg = m.Product.query.filter_by(id=pid).first()
            reg.product = request.form['product'] if 'product' in request.form.keys() else reg.product
            reg.price = request.form['price'] if 'price' in request.form.keys()  else reg.price
            db.session.add(reg)
            db.session.commit()
            return {"msg":"Produto alterado"}, 200
        except Exception as err:
            print(err)
            return {"msg":"Erro:{e}".format(e=err)}, 500
        
    def delete(self, pid):
        reg = m.Product.query.filter_by(id=pid).first()
        try:
            db.session.delete(reg)
            db.session.commit()
            return {"msg":"Cliente excluido"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}, 500
        

class Order(Resource):

    def get(self, pid=0):
        ret = []
        if pid == 0:
            return {"Msg":"Client id obrigatorio"}, 400
        else:
            rOrders = m.Order.query.filter_by(client_id=pid).all()
        for reg in rOrders:
            ret.append(reg.nro)
        rcode = 200 if len(ret) > 0 else 404
        
        return ret, rcode

    def post(self, pid):
        reg = m.Order()
        reg.client_id = pid
        try:
            db.session.add(reg)
            db.session.commit()
            return {"msg":"Ordem criada"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}
        
       
    def delete(self, pid):
        reg = m.Order.query.filter_by(nro=pid).first()
        reg2 = m.Order_item.filter_by(order_nro=pid).all()
        try:
            if len(reg2) > 0:
                db.session.delete(reg2)
                db.session.commit()
            db.session.delete(reg)
            db.session.commit()
            return {"msg":"Cliente excluido"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}, 500

class Item(Resource):

    def get(self, pid=0):
        ret = []
        if pid == 0:
            return {"Msg":"Nro Ordem obrigatorio"}, 400
        else:
            rOrders = m.Order.query.filter_by(order_nro=pid).all()
        for reg in rOrders:
            ret.append(reg.nro)
        rcode = 200 if len(ret) > 0 else 404
        
        return ret, rcode

    def post(self, pid):
        reg = m.Order_item()
        reg.
        try:
            db.session.add(reg)
            db.session.commit()
            return {"msg":"Ordem criada"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}
        
       
    def delete(self, pid):
        reg = m.Order.query.filter_by(id=pid).first()
        try:
            db.session.delete(reg)
            db.session.commit()
            return {"msg":"Cliente excluido"}, 200
        except Exception as err:
            return {"msg":"Erro:{e}".format(e=err)}, 500

        
api.add_resource(Product,"/api/product/","/api/product/<pid>")
api.add_resource(Client,"/api/client/", "/api/client/<pid>")
api.add_resource(Order,"/api/order/<pid>")
api.add_resource(Item,"/api/item/<pid>")

if __name__ == '__main__':
    app.run()

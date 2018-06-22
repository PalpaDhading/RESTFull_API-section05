from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item,SiteItemList
from site import Site, SiteList

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'Nepal'
api = Api(app)
jwt = JWT(app,authenticate, identity) #/auth

api.add_resource(Site, '/site/<string:siteName>')
api.add_resource(SiteList, '/sites')
api.add_resource(Item, '/siteitem/<string:itemName>')
api.add_resource(SiteItemList,'/siteitems')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(port = 5000, debug=True)

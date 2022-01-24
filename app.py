from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import pymysql
import secrets 
from flask_sqlalchemy import SQLAlchemy
from resources.user import UserRegister
from resources.programs import programs, programsList,programsUnivList
from resources.universities import universities, universitiesList
from security import authenticate, identity


app = Flask(__name__)
 # Connecting to MySQL server at localhost using PyMySQL DBAPI
#cin = 'mysql+pymysql://root:''@localhost/masters'
Conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)

app.config['SQLALCHEMY_DATABASE_URI'] = Conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
db = SQLAlchemy(app)
app.secret_key = 'T\xfb\xd4\xaaqJ\xfd\xdb\xd0\xabcv\x87Wi\x00/\x13`6\xd7\xa6\xf9G'
api = Api(app)



jwt = JWT(app, authenticate, identity)

api.add_resource(universities, '/universities/<string:name>') 

api.add_resource(programs, '/programs/<string:un>/<string:name>')
#api.add_resource(programs, '/programs/<string:name>')
api.add_resource(programsList, '/programs')
api.add_resource(universitiesList, '/universities') 
api.add_resource(UserRegister, '/register/<int:id>')
api.add_resource(programsUnivList, '/programs/<string:prog>')
 


if __name__ == '__main__':
    from db import db
    db.init_app(app)  
    app.run(debug=True)  

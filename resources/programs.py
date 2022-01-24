
#import sqlite3 #REMOVE 100
from xmlrpc.client import boolean
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

import os,sys

from models.universities import universitiesModel
dir_path=os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path,
os.pardir))
sys.path.insert(0, parent_dir_path)

from models.programs import programsModel

class programs(Resource):
    parser = reqparse.RequestParser()

 

    #added 101
    parser.add_argument('length',
        type=int,
        required=True,
        help="this field cannot b left blank "
    )
    
    parser.add_argument('type',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
   
    parser.add_argument('place',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('grad',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

   
 

    @jwt_required()
    def post(self,un, name):
        if programsModel.find_by_name(name)and universitiesModel.find_by_name(un):
            return {'message': "A program in this university with name '{}' already exists.".format(name)}
        if not  universitiesModel.find_by_name(un):
            return {'message': "no university was found with this name  '{}' .".format(un)},404

        data = programs.parser.parse_args()

        prog = programsModel( name,un, **data)
        
        prog.save_to_db() ##98
    

        return prog.json(), 201






    @jwt_required()
    def delete(self,un, name):

      prog = programsModel.find_by_name(name) 
      ik= universitiesModel.find_by_name(un)
      if (prog is None )or (ik  is   None): 
              return {'message': 'program not found.'}, 404
      elif (prog is not None) and (un == prog.university):
           prog.delete_from_db()
           return {'message': 'program deleted'}



       

    @jwt_required()
    def put(self, un, name):
        data = programs.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        prog = programsModel.find_by_name(name) 
        
        ik= universitiesModel.find_by_name(un)


        
        if ik is None:#university not found 
             return {'message': 'university not found.'}, 404
        if (prog is None )and (ik  is  not None): # universiy is found but program not found we create a program in this university 
         
            prog = programsModel(name,un, **data)
           
        if (prog is not None) and (un == prog.university):
            prog.length = data['length']
            prog.type = data['type']
            prog.place = data['place']
            prog.grad = data['grad']




        prog.save_to_db()
        return {'message': 'university updated successfully, here are the new corrdinates {}'.format(prog.json())},200
          

class programsList(Resource):
    def get(self):

        return {'programs': [x.json() for x in programsModel.query.all()]}
class programsUnivList(Resource):
    def get(self,prog):
        search = "%{}%".format(prog)
        possts=programsModel.query.filter(programsModel.name.like(search)).all()

        return {'programs': [x.json() for x in possts]}

from flask_restful import Resource, reqparse
from models.universities import universitiesModel
from flask_jwt import jwt_required

class universities(Resource):
    TABLE_NAME='universities'
    parser = reqparse.RequestParser()

    parser.add_argument('Location', type=str, required= True, help="This field cannot be left blank!")
    parser.add_argument('University', type=str, required= True, help="This field cannot be left blank!")
    parser.add_argument('Public', type=bool, required= True, help="This field cannot be left blank!")
    parser.add_argument('Website', type=str, required= True, help="This field cannot be left blank!")

    def get(self, name):
        uni = universitiesModel.find_by_name(name)
        if uni:
            return uni.json()
        return {'message': 'university not found'}, 404
    
    @jwt_required()
    def post(self, name):
        data = universities.parser.parse_args()
        if universitiesModel.find_by_name(name):
            return {'message': "A university with name '{}' already exists.".format(name)}, 400
        uni = universitiesModel(name,**(data))
        uni.save_to_db()
        return uni.json(), 201

    @jwt_required()
    def delete(self, name):
        uni = universitiesModel.find_by_name(name)
        if uni:
            uni.delete_from_db()

        return {'message': 'university deleted'},200

    @jwt_required()
    def put(self, name):
        data = universities.parser.parse_args()
        uni = universitiesModel.find_by_name(name)

        if uni is None:
            uni = universitiesModel(name, **data)
            uni.save_to_db()
            return {'message': 'university created successfully, here are the  coordinates {}'.format(uni.json())},201

            
        else:
            uni.Location = data['Location']
            uni.Public = data['Public']
            uni.University = data['University']
            uni.Website = data['Website']


            uni.save_to_db()
            return {'message': 'university updated successfully, here are the new coordinates {}'.format(uni.json())},200
          
    
class universitiesList(Resource):
    def get(self):
        return {'universities': list(map(lambda x: x.json(), universitiesModel.query.all()))}   

class changeWebsite(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Website', type=str, required= True, help="This field cannot be left blank!")
    @jwt_required()
    def patch(self,name):
        TABLE_NAME='universities'
        data = changeWebsite.parser.parse_args()
        uni = universitiesModel.find_by_name(name)

        if uni is None:
             return {'message': "No university  was found with the name '{}'.".format(name)}, 404
        uni.Website = data['Website']
        uni.save_to_db()
        return {'message': 'university  website updated successfully'},200
          



     


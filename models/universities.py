from db import db
from models.programs import programsModel 

class universitiesModel(db.Model): 

    __tablename__='universities'  
    id = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String(300))  
    Location = db.Column(db.String(300)) 
    University= db.Column(db.String(300)) 
    Public = db.Column(db.Boolean) 
    Website = db.Column(db.String(300)) 
    
    programs = db.relationship('programsModel', lazy='dynamic') 

    def __init__(self, mame, Location, University,Public,Website):
       
        self.Name=mame
        self.Location = Location
        self.University = University
        self.Website= Website
        self.Public= Public

    def json(self):
        return{'name':self.Name, 'Location':self.Location,'University':self.University,'Website': self.Website,'Public':self.Public,'programs': [programs.json() for programs in self.programs.all()]}




    @classmethod
    def find_by_name(self, name):
        return self.query.filter_by(Name=name).first()
     
    @classmethod
    def find_by_id(self, _id):
        return self.query.filter_by(id=_id).first()

    def save_to_db(self): 
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self): 
        db.session.delete(self)
        db.session.commit()

from db import db 

class programsModel(db.Model): 

    __tablename__='programs'  
 
#"ggg"
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(300))   
    university= db.Column(db.String, db.ForeignKey('universities.Name')) 
    universities = db.relationship('universitiesModel')
    length = db.Column(db.Integer) 
    type= db.Column(db.String(300)) 
    place= db.Column(db.String(300)) 
    grad= db.Column(db.String(300)) 


   

    def __init__(self, name, university,length,type,place,grad):
        self.name=name
        self.length = length
        self.university = university
        self.type = type
        self.place = place
        self.grad = grad

    def json(self):
        return{'name':self.name, 'university':self.university,'length':self.length,'type': self.type,'place':self.place,'grad':self.grad}


    @classmethod
    def find_by_name(self, name):

        return self.query.filter_by(name=name).first() 
  
    
   
    def save_to_db(self): 
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self): 

        db.session.delete(self)
        db.session.commit()

from sqlalchemy.orm import validates

from db import db

class EmployeeModel(db.Model):
    __tablename__ = "employees"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    salary = db.Column(db.Float)
    position = db.Column(db.String)
    id_department = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    
    department = db.relationship("DepartmentModel", back_populates="employees")
    
    @validates("name", "lastname")
    def parseName(self, key, nameOrLastname):
        return nameOrLastname.capitalize()
    
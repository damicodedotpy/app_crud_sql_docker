from sqlalchemy.orm import validates

from db import db

class DepartmentModel(db.Model):
    __tablename__ = "departments"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    leader = db.Column(db.String)
    
    employees = db.relationship("EmployeeModel", back_populates="department")
    
    @validates("name")
    def validateDepartmentName(self, key, name):
        departments = ["HR", "IT", "Finance", "Marketing", "Sales", "Development", "Accounting"]
        if name not in departments:
            raise ValueError("Department name is not valid. Please verify")
        else:
            return name
    
    @validates("leader")
    def parseName(self, key, leaderName):
        return leaderName.title()
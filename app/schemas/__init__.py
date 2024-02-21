from marshmallow import fields

from extensions import db, mw
from models.employees import EmployeeModel
from models.departments import DepartmentModel

class DepartmentSchema(mw.SQLAlchemySchema):
    class Meta:
        model: DepartmentModel
        sqla_session = db.session
        load_instance = True
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    leader = fields.String(dump_only=True)
    employees = fields.Nested("EmployeeSchema", many=True)

departmentSchema = DepartmentSchema()
departmentsSchema = DepartmentSchema(many=True)

class EmployeeSchema(mw.SQLAlchemyAutoSchema):
    class Meta:
        model: EmployeeModel
        sqla_session = db.session
        load_instance = True
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    salary = fields.Float(dump_only=True)
    lastname = fields.String(dump_only=True)
    position = fields.String(dump_only=True)
    department = fields.Nested("DepartmentSchema", only=("id", "name", "leader"), dump_only=True)

employeeSchema = EmployeeSchema()
employeesSchema = EmployeeSchema(many=True)
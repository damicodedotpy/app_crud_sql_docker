from werkzeug.exceptions import HTTPException
from psycopg2.errors import NotNullViolation
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, abort
from flask_smorest import Blueprint

from models.employees import EmployeeModel
from db import db

blp = Blueprint('Employees routes', __name__, description="Operations on employees")


@blp.route('/get/employees/<string:employeeId>', methods=['GET'])
@blp.route('/get/employees', methods=['GET'])
def getEmployees(employeeId=None):
    try:
        if employeeId:
            employee = EmployeeModel.query.get_or_404(employeeId, description=f"No employee found with the ID {employeeId}")
            return jsonify({"status": 200, "employee": {
                "id": employee.id,
                "name": employee.name,
                "lastname": employee.lastname,
                "salary": employee.salary,
                "position": employee.position,
                "id_department": employee.id_department
            }}), 200
        
        employees = EmployeeModel.query.all()
        if not employees:
            return abort(404, description="No employees found in the database. Please add some.")
        return jsonify([{
            "id": employee.id,
            "name": employee.name,
            "lastname": employee.lastname,
            "salary": employee.salary,
            "position": employee.position,
            "id_department": employee.id_department} for employee in employees]), 200
        
    except HTTPException as e:
        return jsonify({"status": e.code, "error": f"{e}"})
    except Exception as e:
        return jsonify({"status": 500, "error": f"{e}"})

@blp.route('/add/employees', methods=['POST'])
def addEmployees():
    try:
        data = request.json
        
        if not data:
            return abort(400, description="No data provided. Please send the employee data in JSON format.")
    
        employee = EmployeeModel(**data)
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({"status": 201, "entry": {
            "id": employee.id,
            "name": employee.name,
            "salary": employee.salary,
            "lastname": employee.lastname,
            "position": employee.position,
            "id_department": employee.id_department
        }})
        
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, NotNullViolation):
            return jsonify({"status": 400, "error": f"The employee information needed is incomplete. Please verify and make sure to send all the required fields."})
    except HTTPException as e:
        db.session.rollback()
        return jsonify({"status": e.code, "error": f"{e}"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": 500, "error": f"{e}"})

@blp.route('/delete/employees/<string:employeeId>', methods=['DELETE'])
@blp.route('/delete/employees', methods=['DELETE'])
def deleteEmployees(employeeId=None):
    try:
        if not employeeId:
            EmployeeModel.query.delete()
            db.session.commit()
            return jsonify({"status": 200, "message": "All employees were deleted successfully."})
        
        employee = EmployeeModel.query.get_or_404(employeeId, description=f"No employee found with the ID {employeeId}")
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"status": 200, "message": f"Employee {employee.name} with ID {employeeId} was deleted successfully."})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": 500, "error": f"{e}"})
    except HTTPException as e:
        db.session.rollback()
        return jsonify({"status": e.code, "error": f"{e}"})
    
@blp.route('/update/employees/<string:employeeId>', methods=['PUT'])
def updateEmployees(employeeId):
    try:
        data = request.json
        if not data:
            return abort(400, description="No data provided. Please send the employee data in JSON format.")
        
        update = EmployeeModel.query.filter_by(id=employeeId).update(data)
        db.session.commit()
        if not update:
            return abort(404, description=f"No employee found with the ID {employeeId}")
                
        return jsonify({
            "status": 200, 
            "message": f"Employee with ID {employeeId} was updated successfully.",
            "updated_fields": data}), 200
        
    except Exception as e:
        return jsonify({"status": 500, "error": f"{e}"})
    except HTTPException as e:
        return jsonify({"status": e.code, "error": f"{e}"})
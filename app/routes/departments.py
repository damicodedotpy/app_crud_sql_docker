from flask_smorest import Blueprint
from flask import request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from psycopg2.errors import UniqueViolation, NotNullViolation

from extensions import db
from models.departments import DepartmentModel
from schemas import departmentSchema, departmentsSchema

blp = Blueprint('Departments routes', __name__, description="Operations on departments")

@blp.route('/get/departments/<string:deptId>', methods=["GET"])
@blp.route('/get/departments', methods=["GET"])
def getDepartments(deptId=None):
    try:
        if deptId:
            department = DepartmentModel.query.get_or_404(deptId, description="No department found with that ID. Please try with another one.")
            return jsonify(departmentSchema.dump(department)), 200
        
        departments = DepartmentModel.query.all()
        if not departments:
            return abort(404, "Departments not found in the database. Please add some.")
        return jsonify(departmentsSchema.dump(departments)), 200

        
    except HTTPException as e:
        return jsonify({"status": e.code, "error": e.description})
    except Exception as e:
        return jsonify({"status": 500, "error":f"{e}"})

@blp.route('/add/departments', methods=["POST"])
def addDepartments():
    try:
        data = request.json
        if not data:
            return abort(400, description="No data provided. Please provide the required data to add a department.")
        
        department = DepartmentModel(**data)
        
        db.session.add(department)
        db.session.commit()
        
        return jsonify({
            "status": 201,
            "message": "Department added successfully",
            "entry": departmentSchema.dump(department)
            }), 201
    

    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"status": 400, "error":f"This department already exists in the database. Please verify."})
        elif isinstance(e.orig, NotNullViolation):
            return jsonify({"status": 400, "error":f"Please make sure of provide and fill in all the required fields."})
        else:
            return jsonify({"status": 400, "error":f"{e}"})
    except HTTPException as e:
        return jsonify({"status": e.code, "error": e.description})
    except Exception as e:
        return jsonify({"status": 500, "error":f"{e}"})
    
@blp.route('/update/department/<string:deptId>', methods=["PUT"])
def updateDepartment(deptId):
    try:
        data = request.json
        
        if not data:
            return abort(400, description="No data provided. Please provide the required data to update a department.")
        
        department = DepartmentModel.query.get_or_404(deptId, description="No department found with that ID. Please try with another one.")
        for key, value in data.items():
            setattr(department, key, value)
        # DepartmentModel.query.filter(DepartmentModel.id == deptId).update(data) # <-- This is another way to update the department but it doesn't trigger the @validates decorator due to this instruction interacts directly with the database
        db.session.commit()
        
        return jsonify({
            "status": 200,
            "message": "Department updated successfully",
            "entry": departmentSchema.dump(department)
        }), 200
        
    except Exception as e:
        return jsonify({"status": 500, "error":f"{e}"})
    except HTTPException as e:
        return jsonify({"status": e.code, "error": e.description})

@blp.route('/delete/departments/<string:deptId>', methods=["DELETE"])
@blp.route('/delete/departments', methods=["DELETE"])
def deleteDeparments(deptId=None):
    try:
        if not deptId:
            DepartmentModel.query.delete()
            db.session.commit()
            return jsonify({"status": 200, "message": "All departments deleted successfully"}), 200
        
        db.session.delete(DepartmentModel.query.get_or_404(deptId, description="No department found with that ID. Please try with another one."))
        db.session.commit()
        return jsonify({
            "status": 200, 
            "message": "Department deleted successfully"}), 200
        
    except Exception as e:
        return jsonify({"status": 500, "error":f"{e}"})
    except HTTPException as e:
        return jsonify({"status": e.code, "error": e.description})

import os

from flask_smorest import Api
from flask import Flask
from config import FlaskAppConfig, SwaggerConfig
from models.departments import DepartmentModel
from models.employees import EmployeeModel

from routes.departments import blp as DepartmentsBlueprint
from routes.employees import blp as EmployeesBlueprint
from db import db

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(FlaskAppConfig)
    app.config.from_object(SwaggerConfig)
    
    db.init_app(app)
    
    api = Api(app)
    
    api.register_blueprint(DepartmentsBlueprint, url_prefix=os.getenv('APP_ROUTES_PREFIX'))
    api.register_blueprint(EmployeesBlueprint, url_prefix=os.getenv('APP_ROUTES_PREFIX'))
    
    with app.app_context():
        db.create_all()
        
    return app
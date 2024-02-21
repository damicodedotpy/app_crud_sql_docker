import os

from flask import Flask
from flask_smorest import Api
from flask_marshmallow import Marshmallow
from models.employees import EmployeeModel
from models.departments import DepartmentModel
from config import FlaskAppConfig, SwaggerConfig

from extensions import db, mw
from routes.employees import blp as EmployeesBlueprint
from routes.departments import blp as DepartmentsBlueprint

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(FlaskAppConfig)
    app.config.from_object(SwaggerConfig)
    
    db.init_app(app)
    
    mw.init_app(app)
    
    api = Api(app)
    
    api.register_blueprint(DepartmentsBlueprint, url_prefix=os.getenv('APP_ROUTES_PREFIX'))
    api.register_blueprint(EmployeesBlueprint, url_prefix=os.getenv('APP_ROUTES_PREFIX'))
    
    with app.app_context():
        db.create_all()
        
    return app
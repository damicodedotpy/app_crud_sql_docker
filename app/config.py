import os

class FlaskAppConfig(object):
    # SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://postgres:{os.getenv('DOCKER_POSTGRESQL_PASSWORD')}@host.docker.internal:5432/{os.getenv('DOCKER_POSTGRESQL_DB_NAME')}'
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_POSTGRES_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class SwaggerConfig(object):
    PROPAGATE_EXCEPTIONS = True  #Esta configuracion cuando en True, hace que las excepciones o errores que ocurran en el codigo se muestren listados en la parte de arriba en la terminal.
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui" #es una configuración de la aplicación Flask que especifica la ruta a la interfaz de usuario de Swagger para visualizar la documentación generada por OpenAPI. Esta configuración se usa en conjunto con la biblioteca Flask-RESTPlus para crear una interfaz de programación de aplicaciones (API) que sea fácil de usar y documentar. Con esta configuración se puede personalizar la ruta a la interfaz de usuario de Swagger, por ejemplo, /api/swagger.
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" #es una configuración de la aplicación Flask que especifica la URL a la interfaz de usuario de Swagger para visualizar la documentación generada por OpenAPI. Esta configuración se usa en conjunto con la biblioteca Flask-RESTPlus para crear una interfaz de programación de aplicaciones (API) que sea fácil de usar y documentar. Con esta configuración se puede especificar una URL externa para acceder a la interfaz de usuario de Swagger en lugar de servirla desde la aplicación Flask.
    OPENAPI_URL_PREFIX = "/" #es una configuración de la aplicación Flask que especifica el prefijo de la URL que se usará para acceder a la documentación generada por OpenAPI. Esta configuración se usa en conjunto con la biblioteca Flask-RESTPlus para crear una interfaz de programación de aplicaciones (API) que sea fácil de usar y documentar. Con esta configuración se puede especificar la ruta base para acceder a la documentación de la API, por ejemplo, /api/docs.
    OPENAPI_VERSION = "3.0.3" #Es una configuración de la aplicación Flask que especifica la versión de OpenAPI que se usará para generar la documentación de la API
    API_VERSION = "v1" #Esta es una flask smorest configuration. Asigna un numero de version actual a la aplicacion que estamos trabajandp con fines de documentacion
    API_TITLE = 'SQL Flask CRUD ft. Docker'
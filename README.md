Set-up instructions: 

Running on local

1. Create a new virtual environment --> virtualenv venv
2. Install the project dependencies from the .txt file --> pip install -r requirements.txt
3. Create a .env file and declare the following variables:
    DB_POSTGRES_URI = postgresql+psycopg2://{postgres user}:{password}@localhost:5432/{DB name}
    APP_ROUTES_PREFIX = /api/v1 (suggestion)
4. On module config.py from the 'FlaskConfig' class uncomment the 'SQLALCHEMY_DATABASE_URI' property with value 'os.getenv('DB_POSTGRES_URI')' not the one with docker string.
5. Run API with the flask command --> flask run


Running with docker

1. Make sure to locate the prompt inside the project folder
2. Run the Docker host (Docker desktop application)
3. On module config.py from the 'FlaskConfig' class uncomment the 'SQLALCHEMY_DATABASE_URI' property with value f'postgresql+psycopg2://postgres:{os.getenv('DOCKER_POSTGRESQL_PASSWORD')}@host.docker.internal:5432/{os.getenv('DOCKER_POSTGRESQL_DB_NAME')}' not the one with postgress direct connection string.
4. Create your own image from the docker file with the command --> docker build -t {image name} .
5. Create a container based on the image with the command --> docker run -d -p 5000:5000 -e DOCKER_POSTGRESQL_PASSWORD={db password} -e DOCKER_POSTGRESQL_DB_NAME={db name} --name {container name} {image name}

A simple rest api on SQLite db and even without UI.

- Build docker:
docker build -t example-rest:v1.0 .

- Run docker:
docker run -d -p 5000:5000 --name example-rest example-rest:v1.0

- Swagger available on:
host:5000/api/ui/


To run without docker, install requirements into virtual environment and run build_database.py, then server.py

If postgres is needed as a database, follow this steps:
- Add psycopg2-binary to requirements.txt and install it
- Run a postgres docker:
  - docker pull postgres
  - mkdir -p $HOME/docker/volumes/postgres
  - docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
- change database uri in config.py to 'postgresql://postgres:docker@localhost:5432/postgres'

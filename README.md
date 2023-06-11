# Diagnosis

This is a RESTful API to utilize an internationally recognized set of diagnosis codes built with Django, DRF, Docker and Postgres as the main database.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:

   ```shell
   git clone the [project](https://github.com/jayjaychukwu/diagnosis-test.git)

2. Create a .env file in the project root directory and set the following environment variables, please adjust the values to fit your environment:

    ```shell
    SECRET_KEY=<random-secret-key>
    DEBUG=True
    DB_NAME=<a-database-name>
    DB_USER=postgres
    DB_PASSWORD=postgres

3. Spin up the project using Docker Compose:
   
   Either you use
   ```shell
   docker-compose up
   ```
   and spin up another terminal to run the next set of commands or you run it in the background using
   ```shell
   docker-compose up -d --build
   ```

4. Create a database with the same value in DB_NAME
   
   obtain the name of the database container running using the command:
   ```shell
    docker ps
    ```
    it should be something like "diagnosis_db_1".

    Then run this command to create the database
    ```shell
    docker exec -it <postgres-container-name> createdb -U postgres <db-name>
    ```

    You can ensure the database was created by running
    ```shell
    docker exec -it <my_postgres_container> psql -U postgres -c '\l'
    ```
    and check if the database name is in the list of databases.

5. Make migrations for the dx app and migrate
   ```shell
   docker-compose run web python manage.py makemigrations dx
   docker-compose run web python manage.py migrate
   ```

## Usage
- You can populate the database with DiagnosisCode records using a valid ICD-10 csv file. There is an example in the project root, testicd.csv, you can use the "createdata" command with "-f" or "--file" arguments with the path to the file. 
Example:
   ```shell
   docker-compose run web python manage.py createdata --file testicd.csv
   ```


- To create a superuser for the admin dashboard, run the following command:
    ```shell
    docker-compose run web python manage.py createsuperuser
    ```
    Follow the prompts to create a superuser account.
    Access the admin dashboard at `http://localhost:8000/admin/` and log in using your superuser credentials.


- Run tests for the project using the following command:
    ```shell
    docker-compose run web python manage.py test
    ```

## API Documentation
- Swagger Docs: `http://localhost:8000/`
- ReDoc: `http://localhost:8000/redoc/`

## Architecture
- The project follows a Django, Django REST Framework with Docker for containerization
- Caching has been implemented using Django decorators such as cache_page on list and retrieve endpoints to improve performance. 
- Utilizing the transaction.atomic() method to make a block of code occur in one transaction, therefore reducing round trips, improving performance and other benefits.


Please feel free to reach out to me or raise an Issue if you run into any problems running this project.
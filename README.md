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
The project follows a Django architecture and utilizes the Django REST Framework for building the API. Docker is used for containerization, providing an isolated and consistent environment for development and deployment.

## Caching
Caching has been implemented in the project using Django's caching mechanisms. Decorators such as cache_page have been applied to specific endpoints, such as list and retrieve operations, to improve performance by storing the response data in memory. This helps reduce the need for executing the same expensive database queries or computations repeatedly, resulting in faster response times for subsequent requests.

## Transaction Atomicity
The project leverages the transaction.atomic() method provided by Django's database API to ensure atomicity and improve performance. By encapsulating a block of code for uploading CSV files within transaction.atomic(), all database operations within that block are executed as a single transaction. This approach reduces the number of round trips between the application and the database server, leading to improved performance and efficiency. Additionally, it helps maintain data consistency and integrity by rolling back the entire transaction if any operation within the block fails, preventing partial updates and keeping the database in a consistent state.

By employing caching and utilizing transaction atomicity, the project optimizes performance, reduces database round trips, and ensures the reliability and integrity of data operations.


## Support and Feedback
Please feel free to reach out to me or raise an Issue if you run into any problems running this project.
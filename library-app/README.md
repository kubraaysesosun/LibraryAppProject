# Library App

This project is ....

## Installation

To run the project on your local machine, follow these steps:

1. Clone this repository:

    ```
    git clone https://github.com/mustafabulut34/library-app
    ```

2. Navigate to the project directory:

    ```
    cd library-app
    ```

3. Start the Docker environment:

    ```
    make up
    ```
4. Apply migrations:

    ```
    make migrate
    ```
   
5. Access the swagger:

   Go to `http://localhost:8000/api/v1/docs` in your browser.

## Commands

You can use the following commands to manage the project:

- `make up`: Starts the Docker environment.
- `make kill`: Stops the Docker environment.
- `make build`: Builds the Docker images.
- `make ps`: Shows the status of Docker containers.
- `make exec`: Executes a command inside a Docker container. `make exec args="ls app/core"`
- `make logs`: Shows Docker logs. Ex: `make logs service=app`
- `make mm`: Creates an Alembic migration revision. Ex: `make mm args='new migration'`
- `make migrate`: Performs Alembic migration.
- `make downgrade`: Performs Alembic downgrade. Ex: `make downgrade args=-1`
- `make make_user_admin`: Makes a user an admin. Ex: `make make_user_admin args=test@example.com`

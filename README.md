# Authentication System API

A RESTful authentication API built with FastAPI and PostgreSQL.

## Features

- User registration
- User authentication
- Password hashing
- JWT access tokens
- PostgreSQL database integration
- SQLAlchemy ORM
- Request validation with Pydantic

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- PyJWT
- pwdlib

## Project Status

This project is under active development.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/younes141081-cpu/auth_system.git
cd auth_system
```

### 2. Install dependencies

Install the required packages for the project.

### 3. Configure environment variables

Create a `.env` file based on `.env.example` and configure your database connection and secret keys.

### 4. Run the application

```bash
uvicorn main:app --reload
```

### 5. Open API documentation

Visit:

http://127.0.0.1:8000/docs

## Security

Never commit real passwords, database credentials, or secret keys to the repository.

## License

No license has been specified yet.

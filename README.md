## Hire1 Test Task Backend
This project is a REST API for creating and viewing sales receipts with user registration and authorization.

## Features
User Registration and Authentication

Register new users with a username, email, and password.

Authenticate users and provide JWT tokens for API access.

### Receipt Management
Create sales receipts with product details and payment information.

Calculate totals per item, overall total, and change due.

View a list of own receipts with pagination and filtering options.

Publicly accessible receipts in a text format with configurable line length.

### Filtering and Pagination
Filter receipts by creation date, total amount, and payment type.

Paginate receipt lists using skip and limit parameters.


### Technical Stack
Programming Language: Python 3.10

Framework: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy with Alembic migrations

Authentication: JWT tokens

## Installation
Docker and Docker Compose installed on your machine.

Git for cloning the repository.
```
git clone https://github.com/ArhipDolya/hire1-test-task-backend.git
cd hire1-test-task-backend
```

### Environment Variables
Create a .env file in the root directory with the following content:
```
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=postgresql
POSTGRES_PORT=5432

# Secret keys for JWT tokens
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Replace the placeholder values with your desired settings.

### Build and Run with Docker Compose

```docker compose up --build```


This command will:

Build the Docker image for the FastAPI application.

Start the PostgreSQL database service.

Run the FastAPI application on http://localhost:8000.

### Apply Database Migrations
In a new terminal window, apply the database migrations using Alembic:
```
docker compose exec backend alembic upgrade head
```

This will create the necessary tables in your PostgreSQL database.

### Accessing the API
API Documentation: Visit `http://localhost:8000/api/docs` for interactive API documentation provided by FastAPI's Swagger UI.

## Usage
### User Registration

Endpoint: POST /api/v1/register

### User Login
Endpoint: POST /api/v1/login


### Create a Receipt

Endpoint: POST /api/v1/receipts

Headers: Authorization: Bearer your_access_token

### View Own Receipts
Endpoint: GET /api/v1/receipts

Headers: Authorization: Bearer your_access_token

Query Parameters:

skip (optional): Number of records to skip for pagination.

limit (optional): Maximum number of records to return.

Filtering parameters as per ReceiptFilter model.

### View Receipt Details
Endpoint: GET /api/v1/receipts/{receipt_id}

Headers: Authorization: Bearer your_access_token

### Public Receipt View
Endpoint: GET /api/v1/receipts/{receipt_id}/view

Query Parameters:

line_length (optional): Configure the number of characters per line in the text receipt.

This endpoint is accessible without authentication.

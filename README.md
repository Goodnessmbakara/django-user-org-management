Sure! Here is the `README.md` content for your project:

---

# User and Organisation Management System

This project is a User and Organisation Management System built using Django and Django REST Framework. The application allows users to register, log in, and manage organisations. Each user can belong to multiple organisations, and each organisation can have multiple users.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Registration and Login
- JWT-based Authentication
- Organisation Management
- User and Organisation Relationship Management
- Validation and Error Handling

## Technologies

- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- Pytest

## Setup Instructions

### Prerequisites

- Python 3.x
- PostgreSQL

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory and add the following variables:

   ```plaintext
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://your_db_user:your_db_password@localhost:5432/your_db_name
   ```

5. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- **Register**: `POST /auth/register`
  - Request Body:
    ```json
    {
      "firstName": "string",
      "lastName": "string",
      "email": "string",
      "password": "string",
      "phone": "string"
    }
    ```
  - Successful Response:
    ```json
    {
      "status": "success",
      "message": "Registration successful",
      "data": {
        "accessToken": "eyJh...",
        "user": {
          "userId": "string",
          "firstName": "string",
          "lastName": "string",
          "email": "string",
          "phone": "string"
        }
      }
    }
    ```

- **Login**: `POST /auth/login`
  - Request Body:
    ```json
    {
      "email": "string",
      "password": "string"
    }
    ```
  - Successful Response:
    ```json
    {
      "status": "success",
      "message": "Login successful",
      "data": {
        "accessToken": "eyJh...",
        "user": {
          "userId": "string",
          "firstName": "string",
          "lastName": "string",
          "email": "string",
          "phone": "string"
        }
      }
    }
    ```

### Users

- **Get User**: `GET /api/users/:id`
  - Successful Response:
    ```json
    {
      "status": "success",
      "message": "<message>",
      "data": {
        "userId": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "phone": "string"
      }
    }
    ```

### Organisations

- **Get All Organisations**: `GET /api/organisations`
  - Successful Response:
    ```json
    {
      "status": "success",
      "message": "<message>",
      "data": {
        "organisations": [
          {
            "orgId": "string",
            "name": "string",
            "description": "string"
          }
        ]
      }
    }
    ```

- **Get Organisation**: `GET /api/organisations/:orgId`
  - Successful Response:
    ```json
    {
      "status": "success",
      "message": "<message>",
      "data": {
        "orgId": "string",
        "name": "string",
        "description": "string"
      }
    }
    ```

- **Create Organisation**: `POST /api/organisations`
  - Request Body:
    ```json
    {
      "name": "string",
      "description": "string"
    }
    ```
  - Successful Response:
    ```json
    {
      "status": "success",
      "message": "Organisation created successfully",
      "data": {
        "orgId": "string",
        "name": "string",
        "description": "string"
      }
    }
    ```

- **Add User to Organisation**: `POST /api/organisations/:orgId/users`
  - Request Body:
    ```json
    {
      "userId": "string"
    }
    ```
  - Successful Response:
    ```json
    {
      "status": "success",
      "message": "User added to organisation successfully"
    }
    ```

## Testing

To run the tests, use the following command:

```bash
pytest
```

### Test Scenarios

- **Token Generation**: Ensure token expires at the correct time and correct user details are found in the token.
- **Organisation Access**: Ensure users can’t see data from organisations they don’t have access to.
- **User Registration**: Verify default organisation name generation and response details.
- **User Login**: Verify response details and token generation.
- **Validation**: Ensure appropriate error messages and status codes for missing or duplicate fields.

## Contributing

We welcome contributions! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This `README.md` file provides a comprehensive overview of the project, including setup instructions, API endpoint details, testing, and contributing guidelines.
Certainly! Here is a comprehensive `DOCUMENTATION.md` for your Django REST framework project:

---

# Project Documentation

## Table of Contents
- [Introduction](#introduction)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Application Structure](#application-structure)
- [Endpoints](#endpoints)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [User Details](#user-details)
  - [Get Organisations](#get-organisations)
  - [Get Organisation by ID](#get-organisation-by-id)
  - [Create Organisation](#create-organisation)
  - [Add User to Organisation](#add-user-to-organisation)
- [Testing](#testing)
  - [Running Tests](#running-tests)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)

## Introduction

This project is a Django REST framework-based application that includes user authentication, registration, and organisation management features. Users can register, log in, and manage their organisations.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- PostgreSQL
- pip

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and Activate Virtual Environment**

   ```bash
   python3 -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Create `.env` File**

   Create a `.env` file in the root directory and add your environment variables:

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/your_db_name
   ```

2. **Update Settings**

   Update `your_project/settings.py` to use environment variables:

   ```python
   import os
   from pathlib import Path
   from dotenv import load_dotenv

   load_dotenv()

   # Build paths inside the project like this: BASE_DIR / 'subdir'.
   BASE_DIR = Path(__file__).resolve().parent.parent

   SECRET_KEY = os.getenv('SECRET_KEY')
   DEBUG = os.getenv('DEBUG') == 'True'
   ALLOWED_HOSTS = []

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.getenv('DB_NAME'),
           'USER': os.getenv('DB_USER'),
           'PASSWORD': os.getenv('DB_PASSWORD'),
           'HOST': os.getenv('DB_HOST'),
           'PORT': os.getenv('DB_PORT'),
       }
   }

   AUTH_USER_MODEL = 'my_app.CustomUser'
   ```

## Database Setup

1. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

## Application Structure

```
my_django_project/
│
├── my_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
│
├── tests/
│   ├── __init__.py
│   └── auth.spec.py
│
├── manage.py
├── requirements.txt
├── .env
├── pytest.ini
└── your_project/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Endpoints

### User Registration

**[POST] /auth/register**

Registers a new user and creates a default organisation.

**Request Body:**
```json
{
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "password": "string",
  "phone": "string"
}
```

**Success Response:**
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

### User Login

**[POST] /auth/login**

Logs in a user.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Success Response:**
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

### User Details

**[GET] /api/users/:id**

Gets a user's own record or user record in organisations they belong to or created.

**Success Response:**
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

### Get Organisations

**[GET] /api/organisations**

Gets all organisations the user belongs to or created.

**Success Response:**
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

### Get Organisation by ID

**[GET] /api/organisations/:orgId**

Gets a single organisation record.

**Success Response:**
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

### Create Organisation

**[POST] /api/organisations**

Creates a new organisation.

**Request Body:**
```json
{
  "name": "string",
  "description": "string"
}
```

**Success Response:**
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

### Add User to Organisation

**[POST] /api/organisations/:orgId/users**

Adds a user to a particular organisation.

**Request Body:**
```json
{
  "userId": "string"
}
```

**Success Response:**
```json
{
    "status": "success",
    "message": "User added to organisation successfully"
}
```

## Testing

### Running Tests

To run the tests, use the following command:

```bash
python manage.py test tests.auth.spec
```

Or if you are using `pytest`:

```bash
pytest tests/auth.spec.py
```

### Test Scenarios

#### Token Generation

- Ensure token expires at the correct time.
- Ensure correct user details are found in the token.

#### Organisation

- Ensure users can't see data from organisations they don't have access to.

#### User Registration

- It Should Register User Successfully with Default Organisation:
  - Ensure a user is registered successfully when no organisation details are provided.
  - Verify the default organisation name is correctly generated (e.g., "John's Organisation" for a user with the first name "John").
  - Check that the response contains the expected user details and access token.

- It Should Log the User in Successfully:
  - Ensure a user is logged in successfully when a valid credential is provided and fails otherwise.
  - Check that the response contains the expected user details and access token.

- It Should Fail If Required Fields Are Missing:
  - Test cases for each required field (firstName, lastName, email, password) missing.
  - Verify the response contains a status code of 422 and appropriate error messages.

- It Should Fail if there’s Duplicate Email or UserID:
  - Attempt to register two users with the same email.
  - Verify the response contains a status code of 422 and appropriate error messages.

## Usage

1. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

2. **Access the API**

   Open your browser or API client (such as Postman) and navigate to `http://127.0.0.1:8000`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

---

This `DOCUMENTATION.md` provides a comprehensive overview of the

 project, setup instructions, endpoint details, and information on testing and usage.
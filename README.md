# Django Rest Framework Client

This repository contains a collection of Python scripts designed to interact with a Django Rest Framework API. The scripts demonstrate various actions such as authentication, creating, updating, deleting, and retrieving data from the API.

## Project Status

⚠️ **Work in Progress**: This project is currently under development and is not considered complete. Some features may be incomplete or not fully implemented.

## Usage

### Scripts
1. **`basic.py`**: Demonstrates a basic GET request to the API.
2. **`create.py`**: Creates a new product using a POST request with authorization.
3. **`delete.py`**: Deletes a product by providing its ID.
4. **`detail.py`**: Retrieves details of a specific product by providing its ID.
5. **`list.py`**: Lists all products with authentication.
6. **`not_found.py`**: Attempts to retrieve details of a non-existent product to test error handling.
7. **`update.py`**: Updates the details of a product using a PUT request.


## Authentication and Permissions

### Authentication

Authentication is implemented using Token Authentication. The `TokenAuthentication` class, extending `BaseTokenAuth`, is utilized with the keyword 'Bearer' for passing the token in the request header. Tokens can be obtained through the `/auth/` endpoint using the `obtain_auth_token` view provided by Django Rest Framework's `authtoken` module.

Example:
```python
from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.authtoken.models import Token

class TokenAuthentication(BaseTokenAuth):
    keyword = 'Bearer'
```

### Permissions

Authorization is handled through the `IsStaffEditorPermission` class, a custom permission class extending `permissions.DjangoModelPermissions`. It maps HTTP methods to corresponding Django model permissions.

Example:
```python
from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
```

## Important Note

This project is intended for educational purposes and serves as a demonstration of interacting with a DRF API using Python scripts. It is not a finished product, and some features may be incomplete.

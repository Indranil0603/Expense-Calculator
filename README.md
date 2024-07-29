# Expense Calculator

This project is an expense sharing application built using Django and Django REST Framework. It allows users to create and manage expenses, split them among different users, and view their balances.

## Table of Contents
* [Installation](#installation)

* [API Documentation](#api-endpoints)

* [Running Tests](#running-tests)

## Installation
Follow these steps to get the project up and running on your local machine.

### Prerequisites
* Python 3.8+
* pip (Python package installer)
* virtualenv (optional but recommended)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/Indranil0603/Expense-Calculator.git
cd Expense-calculator
```

#### Step 2: Create and Activate a Virtual Environment
```bash
virtualenv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

####  Step 4: Set Up the Database
```bash
python manage.py migrate
```

#### Step 5: Create a Superuser
To create a superuser for accessing the Django admin panel, run:
```bash
python manage.py createsuperuser
```

#### Step 6: Run the Development Server
Start the development server with
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your web-browser to see the application


## API Endpoints

### User Endpoints

#### Create User

Endpoint : `POST http://localhost:8000/api/users/`

Description: Creates a new user.

example - 
```bash
curl -X POST http://localhost:8000/api/users/ \
    -H "Content-Type: application/json" \
    -d '{
        "email": "example.user@example.com",
        "name": "Example User",
        "mobile_number": "1234567890"
    }'

```

#### Get User Details

Endpoint: `GET http://localhost:8000/api/users/<user_id>/`

Description: Retrieves details of a specific user by their ID.

example -
```bash
curl -X GET http://localhost:8000/api/users/1/
```

### Expense Endpoints

#### Create Expense

Endpoint: `POST http://localhost:8000/api/expenses/`

Description: Creates a new expense and splits them according to split method.

* Equal split
  ```bash
  curl -X POST http://localhost:8000/api/expenses/ \
    -H "Content-Type: application/json" \
    -d '{
        "description": "Dinner",
        "total_amount": 3000,
        "split_method": "equal",
        "shares": [
            {"user": 1},
            {"user": 2},
            {"user": 3}
        ]
    }'

  ```
* Percentage Split
  ```bash
  curl -X POST http://localhost:8000/api/expenses/ \
    -H "Content-Type: application/json" \
    -d '{
        "description": "Party",
        "total_amount": 4000,
        "split_method": "percentage",
        "shares": [
            {"user": 1, "percentage": 50},
            {"user": 2, "percentage": 25},
            {"user": 3, "percentage": 25}
        ]
    }'

  ```

* Exact Split
  ```bash
  curl -X POST http://localhost:8000/api/expenses/ \
    -H "Content-Type: application/json" \
    -d '{
        "description": "Ride",
        "total_amount": 2000,
        "split_method": "exact",
        "shares": [
            {"user": 1, "amount": 1000},
            {"user": 2, "amount": 700},
            {"user": 3, "amount": 300}
        ]
    }'

  ```

#### User Expenses

Endpoint: `GET http://localhost:8000/api/expenses/user/<user_id>/`

Description: Retrieves all expenses associated with a specific user.

example:
  ```bash
  curl -X GET http://localhost:8000/api/expenses/user/1/
  ```
#### Overall Expenses

Endpoint: `GET http://localhost:8000/api/expenses/overall/`

Description: Retrieves all expenses in the system.

example:
```bash
curl -X GET http://localhost:8000/api/expenses/overall/
```
#### Download Balance Sheet

Endpoint: `GET http://localhost:8000/api/expenses/download-balance-sheet/`

Description: Downloads the balance sheet for all users.

example:
```bash
curl -X GET http://localhost:8000/api/users/download-balance-sheet/ -O balance_sheet.csv
```

## Running Tests

To run tests run the following command-
```bash
python manage.py test expenses_app.tests
```










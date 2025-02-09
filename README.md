# Airline Management API
## Project Overview

The Airline Management API allows users to manage flight schedules, reservations, and passenger information.
## Requirements

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- Postman (for API testing)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mexikali/airline-management-api.git
   cd airlineManagementAPI
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `.\venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in `airlineManagementAPI/airlineManagementAPI/` and configure the following environment variables:
   ```env
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=

   HOST=
   PORT=
   USE_TLS=
   HOST_USER=
   HOST_PASSWORD=
   ```
5. Create Database
   ```
   python manage.py init_db
   ```
6. Apply migrations:
   ```sh
   python manage.py migrate
   ```

   ## Adding Dummy Data

    You can populate the database with dummy data using the `seeder.json` file located in `airlineManagementAPI/api/fixtures/`.

    To load the dummy data, run the following command:
    ```sh
    python manage.py loaddata seeder.json
    ```

7. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Mail Configuration

To enable email functionality, update the following setting in `settings.py`:

- **Before:**
  ```python
  EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  ```
- **After:**
  ```python
  EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
  ```
## Usage

To interact with the API, use tools like Postman or cURL. Below are some example requests:

- **Retrieve all flights:**
  ```sh
  GET /api/flights/
  ```
- **Filter flights by departure, arrival location, and date:**
  ```sh
  GET /api/flights/?departure_location=NYC&arrival_location=LAX&departure_date=2025-02-10
  ```
- **Create a reservation:**
  ```sh
  POST /api/reservations/
  Content-Type: application/json
  {
      "flight": 1,
      "passenger": "John Doe",
      "email": "johndoe@example.com"
  }
  ```
- **Retrieve reservations for a flight:**
  ```sh
  GET /api/flights/1/reservations/
  ```
## API Documentation

The following endpoints are available:

### Airplanes
- `GET /api/airplanes/` - Retrieve all airplanes
- `GET /api/airplanes/{id}/` - Retrieve a specific airplane
- `POST /api/airplanes/` - Add a new airplane
- `PATCH /api/airplanes/{id}/` - Update an airplane
- `DELETE /api/airplanes/{id}/` - Delete an airplane
- `GET /api/airplanes/{id}/flights/` - Retrieve flights for a specific airplane

### Flights
- `GET /api/flights/` - Retrieve all flights
- `GET /api/flights/?destination_location={destination}&departure_date={date}` - Filter flights by destination and departure date
- `GET /api/flights/{id}/` - Retrieve a specific flight
- `POST /api/flights/` - Add a new flight
- `PATCH /api/flights/{id}/` - Update a flight
- `DELETE /api/flights/{id}/` - Delete a flight
- `GET /api/flights/{id}/reservations/` - Retrieve reservations for a specific flight

### Reservations
- `GET /api/reservations/` - Retrieve all reservations
- `GET /api/reservations/{id}/` - Retrieve a specific reservation
- `POST /api/reservations/` - Add a new reservation
- `PATCH /api/reservations/{id}/` - Update a reservation
- `DELETE /api/reservations/{id}/` - Delete a reservation

## Testing

You can test the API using Postman by importing the provided Postman collection.


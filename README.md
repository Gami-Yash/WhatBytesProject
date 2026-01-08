# Healthcare Backend (Django + DRF)

A secure REST backend for managing patients, doctors, and their assignments. It uses Django, Django REST Framework, PostgreSQL, and JWT authentication via `djangorestframework-simplejwt`.

## Features
- Email-based user registration and JWT login
- CRUD APIs for patients and doctors implemented with DRF `ModelViewSet`
- Patient-doctor assignment with conflict prevention (no duplicate pairs)
- Per-user patient visibility and authorization checks on every resource
- Environment-driven configuration (database, JWT lifetime, allowed hosts)

## Tech Stack
- Python 3.11+
- Django 5.1.1
- Django REST Framework 3.15
- djangorestframework-simplejwt 5.3
- psycopg 3

## Local Setup (no virtualenv)
1. Install dependencies globally (or manage them however you prefer):
   ```bash
   pip3 install -r requirements.txt
   ```
2. Copy the example environment file and fill in secrets:
   ```bash
   cp .env.example .env
   # update DJANGO_SECRET_KEY and PostgreSQL credentials
   ```
3. Ensure PostgreSQL is running and the database defined in `.env` exists.
4. Run migrations (this only needs database connectivity):
   ```bash
   python3 manage.py migrate
   ```
5. Create a superuser if you need Django admin access:
   ```bash
   python3 manage.py createsuperuser
   ```
6. Start the API server:
   ```bash
   python3 manage.py runserver
   ```

## Environment Variables
| Key | Description |
| --- | --- |
| `DJANGO_SECRET_KEY` | Secret key for Django |
| `DJANGO_DEBUG` | `True`/`False` toggle |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_HOST` / `POSTGRES_PORT` | Connection details |
| `JWT_ACCESS_MINUTES` | Access token lifetime (minutes) |
| `JWT_REFRESH_DAYS` | Refresh token lifetime (days) |

## API Surface
Base URL: `http://127.0.0.1:8000/api/`

### Auth
- `POST /api/auth/register/` → `{ "name", "email", "password" }`
- `POST /api/auth/login/` → `{ "email", "password" }` (returns access + refresh)
- `POST /api/auth/refresh/` → `{ "refresh" }`

### Patients (JWT required)
- `GET /api/patients/`
- `POST /api/patients/`
- `GET /api/patients/<id>/`
- `PUT /api/patients/<id>/`
- `DELETE /api/patients/<id>/`

### Doctors (JWT required)
- `GET /api/doctors/`
- `POST /api/doctors/`
- `GET /api/doctors/<id>/`
- `PUT /api/doctors/<id>/`
- `DELETE /api/doctors/<id>/`

### Patient-Doctor Mappings (JWT required)
- `GET /api/mappings/`
- `POST /api/mappings/` with `patient_id` and `doctor_id`
- `GET /api/mappings/<id>/`
- `DELETE /api/mappings/<id>/`
- `GET /api/mappings/patient/<patient_id>/` → all doctors linked to that patient (custom helper route)

```
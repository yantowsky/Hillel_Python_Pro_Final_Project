# Hillel_Python_Pro_Final_Project

Monorepo:
- `projecta_api/` — Django + DRF + JWT (Core Medical API)
- `projectb_api/` — Django + DRF + JWT (Telemed/Messaging API)
- `frontend/` — React Vite
- інтеграція: ProjectA (Celery task) → ProjectB (REST API)

## Requirements
- Docker + Docker Compose

## Setup
Create `.env` in repo root (do not commit it). You can start from `.env.example`.

Example variables:
- `POSTGRES_PASSWORD=...`
- `DJANGO_SECRET_KEY=...`
- `PROJECTB_SERVICE_PASSWORD=...` (password for ProjectB user `service_a`)

## Run

bash docker compose up --build


## Admin panels
- ProjectA admin: http://127.0.0.1:8000/admin/
- ProjectB admin: http://127.0.0.1:8001/admin/

## Create admin users inside containers

bash docker compose exec projecta_api python manage.py createsuperuser docker compose exec projectb_api python manage.py createsuperuser



## Create / update ProjectB service user (used by ProjectA integration)
Create the user `service_a` in ProjectB and set password to match `PROJECTB_SERVICE_PASSWORD`.

bash docker compose exec projectb_api python manage.py shell


In shell:
python from accounts.models import User u, _ = User.objects.get_or_create(username="service_a", defaults={"is_staff": True, "is_active": True}) u.role = User.Role.ADMIN u.is_staff = True u.is_active = True u.save()


Set password:
bash docker compose exec projectb_api python manage.py changepassword service_a


## Quick API check
- ProjectA token endpoint: `POST http://127.0.0.1:8000/api/auth/token/`
- ProjectB token endpoint: `POST http://127.0.0.1:8001/api/auth/token/`
docker compose logs --tail=200 celery_a
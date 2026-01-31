# Hillel Python Pro Final Project

## Topic
**Організація онлайн-консультацій та спілкування з пацієнтами у медичних установах**.

## Tech stack
- Backend: Django + Django REST Framework + JWT (SimpleJWT)
- Frontend: React (Vite) + Bootstrap

## Project structure
- `backend/` — Django project (API)
- `frontend/` — React (Vite) app (UI)

## Backend setup (local)
```

bash cd backend python manage.py migrate python manage.py createsuperuser python manage.py runserver``` 

Backend will be available at: `http://127.0.0.1:8000`

## Frontend setup (local)
```

bash cd frontend npm install npm run dev``` 

Frontend will be available at: `http://localhost:5173`

## API check (JWT)
### Get tokens
```

bash curl -X POST http://127.0.0.1:8000/api/token/
-H "Content-Type: application/json"
-d '{"username":"YOUR_USERNAME","password":"YOUR_PASSWORD"}'``` 

### Check current user
```
bash curl [http://127.0.0.1:8000/api/me/](http://127.0.0.1:8000/api/me/)
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
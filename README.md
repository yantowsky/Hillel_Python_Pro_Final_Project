# Medical Telemedicine Platform

## Опис проекту

Це фінальний проект для курсу Hillel Python Pro - комплексна медична платформа для організації онлайн-консультацій та спілкування з пацієнтами.

### Архітектура

**Monorepo структура:**
- `projecta_api/` — Django + DRF + JWT (Core Medical API)
- `projectb_api/` — Django + DRF + JWT (Telemed/Messaging API)  
- `frontend/` — React Vite (Web Interface)
- **Інтеграція:** ProjectA (Celery task) → ProjectB (REST API)

### Функціональність

#### ProjectA (Core Medical API)
- Управління пацієнтами та лікарями
- Запис на прийоми (appointments)
- Медичні записи та історія хвороб
- Автоматична інтеграція з ProjectB через Celery

#### ProjectB (Telemed/Messaging API)
- Створення бесід для консультацій
- Система повідомлень між пацієнтом та лікарем
- Управління телемедичними сесіями

#### Frontend (React)
- Форми автентифікації для обох API
- Інтерфейс управління прийомами
- Система повідомлень в реальному часі

### Технологічний стек

**Backend:**
- Django 4.2 + Django REST Framework
- JWT автентифікація
- PostgreSQL бази даних
- Celery + Redis для асинхронних тасків
- Docker контейнеризація

**Frontend:**
- React 18 + Vite
- HTTP клієнт для API комунікації
- Адаптивний дизайн

**DevOps:**
- Docker Compose для оркестрації
- Окремі контейнери для кожного сервісу
- Environment variables конфігурація

### Реалізовані вимоги курсу

✅ **Два Django проекти** з REST API  
✅ **Комунікація через API** між проектами  
✅ **Docker** контейнеризація  
✅ **Тести** (модульні, функціональні, інтеграційні)  
✅ **Celery** для асинхронних тасків  
✅ **Class Based Views** з наслідуванням  
✅ **Розширена модель користувача** з пермішенами  
✅ **Bootstrap** (React заміняє традиційні шаблони)

## Встановлення та запуск

### Requirements
- Docker + Docker Compose

### Налаштування
1. Створіть `.env` в корені репозиторію (не комітьте його). Можна використати `.env.example` як шаблон.

Приклад змінних:
- `POSTGRES_PASSWORD=your_secure_password`
- `DJANGO_SECRET_KEY=your_django_secret_key`
- `PROJECTB_SERVICE_PASSWORD=service_user_password` (пароль для ProjectB користувача `service_a`)

### Запуск системи
```bash
docker compose up --build
```

### Доступ до сервісів
- **Frontend:** http://127.0.0.1:5173
- **ProjectA API:** http://127.0.0.1:8000
- **ProjectB API:** http://127.0.0.1:8001
- **ProjectA Admin:** http://127.0.0.1:8000/admin/
- **ProjectB Admin:** http://127.0.0.1:8001/admin/

## Налаштування користувачів

### Створення admin користувачів
```bash
docker compose exec projecta_api python manage.py createsuperuser
docker compose exec projectb_api python manage.py createsuperuser
```

### Створення service користувача для інтеграції
Створіть користувача `service_a` в ProjectB з паролем з `PROJECTB_SERVICE_PASSWORD`:

```bash
docker compose exec projectb_api python manage.py shell
```

В shell:
```python
from accounts.models import User
u, _ = User.objects.get_or_create(
    username="service_a", 
    defaults={"is_staff": True, "is_active": True}
)
u.role = User.Role.ADMIN
u.is_staff = True
u.is_active = True
u.save()
```

Встановіть пароль:
```bash
docker compose exec projectb_api python manage.py changepassword service_a
```

## API Ендпоінти

### Авентифікація
- ProjectA token: `POST http://127.0.0.1:8000/api/auth/token/`
- ProjectB token: `POST http://127.0.0.1:8001/api/auth/token/`

### Основні ендпоінти
**ProjectA:**
- `GET /api/appointments/` - список прийомів
- `POST /api/appointments/` - створення прийому
- `GET /api/medical-records/` - медичні записи

**ProjectB:**
- `GET /api/telemed/conversations/` - список бесід
- `POST /api/telemed/conversations/` - створення бесіди
- `GET /api/telemed/conversations/{id}/messages/` - повідомлення бесіди
- `POST /api/telemed/conversations/{id}/messages/` - надіслати повідомлення
с
## Тестування

### Запуск тестів
```bash
# ProjectA тести
docker compose exec projecta_api python manage.py test

# ProjectB тести  
docker compose exec projectb_api python manage.py test
```

### Перевірка Celery
```bash
docker compose logs --tail=50 celery_a
```

## Структура проекту

```
Hillel_Python_Pro_Final_Project/
├── projecta_api/          # Core Medical API
│   ├── accounts/          # Модель користувача з ролями
│   ├── core/              # Appointments, Medical Records, Tasks
│   └── config/            # Django settings
├── projectb_api/          # Telemed/Messaging API  
│   ├── accounts/          # Модель користувача
│   ├── telemed/           # Conversations, Messages
│   └── config/            # Django settings
├── frontend/              # React Vite додаток
│   ├── src/
│   │   ├── api/          # HTTP клієнт
│   │   └── App.jsx       # Основний компонент
│   └── package.json
├── docker-compose.yml     # Оркестрація контейнерів
└── requirements.txt      # Python залежності
```

## Демонстрація роботи

1. **Створення appointment** в ProjectA автоматично створює **conversation** в ProjectB через Celery task
2. **Пацієнт** може переглядати свої прийоми та спілкуватися з лікарем
3. **Лікар** має доступ до медичних записів та може керувати прийомами
4. **Admin** має повний доступ до всіх функцій

## Ліцензія
Проект створений як фінальна робота для курсу Hillel Python Pro.
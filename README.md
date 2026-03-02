# djauthij

Reusable Django authentication app with OTP verification and optional background task support using Huey.

---

## Features

- Custom user model (email-based authentication)
- Soft delete and hard delete methods user model
- OTP verification for registration
- Email sending support
- background task with Huey

---

## Installation

```
pip install git+https://github.com/Iqbal120708/djauthij-liblary.git
pip install redis
```

## Usage

```
INSTALLED_APPS = [
    "huey.contrib.djhuey",
    "djauthij",
]
```

```python
python manage.py makemigrations
python manage.py migrate
```

```bash
redis-server
```

```python
python manage.py runserver
python manage.py run_huey
```

## Email Settings

You must configure email settings in your project if you want OTP emails to work:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_email_password"
```

## Huey Configuration

This library uses Huey for background tasks (OTP email sending).


```python
HUEY = {
    "huey_class": "huey.RedisHuey",
    "name": "djauthij",
    "connection": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
    },
    "immediate": False,
    "consumer": {
        "workers": 2,
        "worker_type": "thread",
    },
}
```

## Other Settings 

```AUTH_USER_MODEL = "djauthij.CustomUser"```

```ACCOUNTS_APP_NAME = "My Auth App"``` (Optional) default has value **Dj Auth**

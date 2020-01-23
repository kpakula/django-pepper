# OBreaker

This is an application with special offers. Offers are added by the community.
Users have the option of assessing whether they like the offer or not.
A logged member can add/change offer and also mark end of the offer.



## Development


```bash
# Run the application
python manage.py runserver

# Run the server on specific port
python manage.py runserver 8080

# Create migration
python manage.py migrate
```

## Stack
```
Django
PostgreSQL
```

## Database

```
# You need to define a connection with database in settings.py

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    }
}
```

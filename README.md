# UniOrientBackup
Human Resource Information System for Uni-Orient Travel Incorporated (Cebu) with Descriptive Analytics

1. Don't forget to install all apps in requirements.txt using pip freeze command
2. pip install -r requirements.txt

Set Database to this:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbUniOrient',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

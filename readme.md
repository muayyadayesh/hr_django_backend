# HR system:

initialization & running 

## Postgresql DB:

- install postgres
- setup database, user and auth as below:
```
  'NAME': 'hrdb',
  'USER': 'postgres',
  'PASSWORD': '1234',
```


## Django back-end app:

- clone repo
- cd parent directory
- create and activate the venv
- pip3 install requirements.txt
- pip3 manage.py makemigrations
- pip3 manage.py migrate

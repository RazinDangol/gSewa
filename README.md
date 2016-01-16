# gSewa(Greedy Sewa)
Flask program to analyze transaction/data from [eSewa](http://www.esewa.com.np) excel datasheet. 
##Requirements
- First install [Python 3.3 or newer version](https://www.python.org/downloads/)
- Install redis-server
- Install requirements via pip
```
  pip install -r requirements.txt
``` 
##Note:
Only few features works currently but don't worry all features will work soon :)
Features not working:

- ~~Uploading of excel datasheet~~
- Total Tab

##Usage
- Download excel datasheet from [eSewa](http://www.esewa.com.np)
- First start redis server 
```
redis-server
```
- Start celery worker
```
celery -A gsewa.celery worker -l info
```
- Then runserver
```
python manage.py runserver
```

Navigate to [127.0.0.1:5000/](http://127.0.0.1:5000/)



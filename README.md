# gSewa(Greedy Sewa)
Flask program to analyze transaction/data from [eSewa](http://www.esewa.com.np) excel datasheet. 
##Requirements
- First install Python 3 
- Install requirements via pip
```
  pip install -r requirements.txt
``` 

##Usage
Download excel datasheet from [eSewa](http://www.esewa.com.np) and put it in project directory
Then initiate the database
```python
python manage.py init_db <excel document>
```

For ex:
```python
python manage.py init_db esewa.xls #if your excel file named esewa.xls 
```

Then runserver:

```python 
python manage.py runserver
```

Navigate to [127.0.0.1:5000/payment/all](http://127.0.0.1:5000/payment/all)

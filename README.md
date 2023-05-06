# TheBook
Diploma project Cardiff Metropolitan University  

## Description
TheBook is a web application where people can create posts about books, share their opinions and discuss what they have read. 

## How run the project

Clone project 
```
git clone git@github.com:nat1905/TheBookDiplom.git
```
Create venv based on Python 3.10.9 
```
python -m venv venv
```
Activate venv 
```
source venv/Scripts/activate
```
Install depenndcies from requirements.txt 
```
pip install -r requirements.txt
```
Make migrations
```
python manage.py makemigrations
python manage.py migrate
```
Create superuser 
```
python manage.py createsuperuser
```
Run server 
```
python manage.py runserver
```

![master](https://github.com/nat1905/TheBookDiplom/actions/workflows/main.yml/badge.svg)

**Posts app**
=============

*URLs*
------

URLs of the app are in posts/urls.py

It is linked with project's urls.py (thebook/urls.py)

*Views*
-------

Views of the app are in posts/views.py

Views funtions are linked with urls and templates.

The Book application is built on a client-server architecture. 
First, the list of available urls is processed. 
Then a request is made to the url. 
The corresponding view function is called to process the request. 

*Models*
--------
Models of the app are in posts/models.py

Django has a tool for working with the database - Django ORM. 
The programmer creates his own classes based on models. These classes are inherited from models.Model. 
Thanks to this, they have many built-in functions with which it is easy to work with the database.


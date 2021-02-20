# Job Task

Task description is available in "Test Assignment Pyhton Developers-converted.pdf"

## Getting Started

Download all files or clone repository.

### Prerequisites

Python 3, Django 3.1, Django Rest Framework 3.12

### Installing

Run following command in project directory.

```
pip install -r requirements.txt
```
## Running Project

Run following commands 

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### Test Input

To add a tree, send  @ http://127.0.0.1:8000/category/
 post request with json format tree input. 

You can see all the categories in database @
http://127.0.0.1:8000/category/ get request.

You can see all the relations of a category  @
http://127.0.0.1:8000/category/<id> get request.
## Support

In case of any issue please contact @ ma.tahirk@gmail.com

## Authors

* **Muhammad Abdullah Tahoir** - *Initial work* - Bridge Trade International.



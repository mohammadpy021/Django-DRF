<h1>django project</h1>
Practice of django course of <a href="https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%AC%D9%86%DA%AF%D9%88-%D9%BE%DB%8C%D8%B4%D8%B1%D9%81%D8%AA%D9%87-mk1438/">Maktabkhooneh</a>


<h2> creating Virtual environment </h2>

<h3> Linux </h3>

``` console
python -m venv venv
source venv\bin\activate
```
<h3> Windows  </h3>

``` console
py  -m venv venv
venv\Script\activate
```
# install dependencies
``` console
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
# create SuperUser
``` console
python manage.py createsuperuser 
```
# Run on localhost
``` console
python manage.py runserver
```
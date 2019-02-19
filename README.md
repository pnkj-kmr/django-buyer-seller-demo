# django-buyer-seller-demo



Prerequisites
-------------
1. Python 3.6.X or higher
    > yum -y install https://centos7.iuscommunity.org/ius-release.rpm
    > yum -y install python36u
    > python3.6 -V

Installation steps
------------------
1. cd <path/to/source>
2. python3 -m venv venv
3. source venv/bin/activate
4. python --version                         # Verison should be 3.x.x
5. cd src
6. pip install -r requirement.txt
7. python manage.py makemigrations
8. python manage.py migrate                 # after setting database - settings.py
9. python manage.py createsuperuser
10. python manage.py runserver

Application will be started at http://127.0.0.1:8000/



-- Completed --




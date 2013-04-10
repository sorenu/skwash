skwash
======

## Installation

Node.js must be installed to run 'npm' command.

    $ virtualenv venv --distribute
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py initdb
    $ npm install -g coffee-script
    $ npm install -g less
    $ python manage.py runserver

After running these commands four users will have been created called: Player10, Player20, Player30 and Player40. They all have password: test1234

## Run tests

    $ python manage.py test website

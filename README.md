# uni_app
An app to keep track of tertiary courses and the students enrolled in them.

## Current features:
This app is a demonstration for content delivery, and is therefore "feature light". It has a `User` model with login/logout functionality using session cookies, and currently has one other CRUD resource: a `Course` model. Upcoming lessons will add a foreign-keyed `Student` model, and will add the `.owner` foreign-key relation. To the `Course` model.

Tests are currently mostly disabled, having made the transition from an API serving JSON to templated HTML. 

The app runs on `Flask`, using a `PostgreSQL` database via `Psycopg2` and `SQLAlchemy`. Serialization is courtesy of `Marshmallow`, templating from `Jinja2`, migrations from `Flask-Migrate` with `Alembic`, and sessions via `Flask-Login`.

## Dependencies:
* Python 3
* PostgreSQL
* virtualenv
* pip

## Setup:
### CLONE REPO:
```bash
 git clone https://github.com/Oliver-CoderAcademy/uni_app.git
 ```

### CREATE VENV:
```bash
# /uni_app/
virtualenv venv
```

### ACTIVATE VENV
```bash
# /uni_app/
source venv/bin/activate
```

### INSTALL DEPENDENCIES
```bash
# /uni_app/
pip install -r requirements.txt
```

### CREATE DATABASE AND USER
```SQL
psql postgres

>> CREATE DATABASE <db_name_here>;
>> CREATE USER <user_name_here> WITH PASSWORD '<password_here>';
>> GRANT ALL PRIVILEGES ON DATABASE <db_name_here> TO <user_name_here>;
>> \q
```

### SET ENVIRONMENT VARIABLES. 
Easiest during development is to add a `.env` file to the `/uni_app/` directory like so:
```bash
DB_USER = # value from above
DB_PASS = # value from above
DB_NAME = # value from above
DB_DOMAIN = "localhost:5432"
SECRET_KEY = # dealer's choice - a long random string is most secure
```

### CREATE/MIGRATE TABLES USING TERMINAL COMMANDS

Terminal commands for the app must be executed from the `/uni_app/uni_app/` directory. Currently available commands are:

`flask db drop` -> drops all tables 

`flask db create` -> creates all tables

**NOTE: As of Thursday 18th of November, these commands will change to accomodate `flask-migrate` functionality.** New commands will be:

`flask db-custom drop` -> drops all tables

`flask db-custom create` -> **(DEPRECATED)** creates all tables

`flask db init` -> initializes the `/migrations/` folder

`flask db migrate -m "<migration note>"` -> creates a new migration

`flask db upgrade` -> applies migrations (optional - specify a target migration)

`flask db downgrade` -> un-applies migrations (optional, specify a target migration)

### RUN APP 
```bash
# /uni_app/uni_app/
flask run
``` 


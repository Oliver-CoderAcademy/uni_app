# uni_app
An app to keep track of tertiary courses and the students enrolled in them.

## Current features:
This app is a demonstration for content delivery, and is therefore "feature light". It has a `User` model with login/logout functionality using session cookies, and currently has one other CRUD resource: a `Course` model. Upcoming lessons will add a `Student` in a many-to-one relation with `Course`, and will add the `.owner` foreign-key relation to the `Course` model.

Tests are currently mostly disabled, having made the transition from an API serving JSON to templated HTML. 

The app runs on `Flask`, using a `PostgreSQL` database via `Psycopg2` and `SQLAlchemy`. Serialization is courtesy of `Marshmallow`, templating from `Jinja2`, migrations from `Flask-Migrate` with `Alembic`, and sessions via `Flask-Login`.

Image upload and storage is handled with `boto3`, accessing an S3 bucket.


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

### CREATE S3 BUCKET WITH IAM POLICY
The user needs to have programmatic access to the bucket to perform `GetObject`, `PutObject` and `DeleteObject` actions. See Term 3 Day 17 lesson content for more details.

### SET ENVIRONMENT VARIABLES. 
Easiest during development is to add a `.env` file to the `/uni_app/` directory like so:
```bash
DB_USER = # value from above
DB_PASS = # value from above
DB_NAME = # value from above
DB_DOMAIN = "localhost:5432"
SECRET_KEY = # dealer's choice - a long random string is most secure
AWS_ACCESS_KEY_ID= # value from AWS
AWS_SECRET_ACCESS_KEY=# value from AWS
AWS_S3_BUCKET=# value from AWS
```

### CREATE/MIGRATE TABLES USING TERMINAL COMMANDS

Terminal commands for the app must be executed from the `/uni_app/uni_app/` directory. Currently available commands are:

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


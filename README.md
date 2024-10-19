# Healthcare Management System
[![django-version](https://img.shields.io/badge/django-3.2-green)](https://www.djangoproject.com)
[![python-version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org)
[![postgresql-version](https://img.shields.io/badge/postgresql-12.3-orange)](https://www.postgresql.org)

# __Setup Guidline:__
> _Make sure `git`, `python3` and `postgresql` is installed in the system._

1. ### Preparing the project
    - clone the repository `git clone git@github.com:cseshahriar/patient-management-system.git`
    - Work from the project directory as current directory using `cd patient-management-system.git`.
    - Create a virtual environment using `python`. (Test via `python -V`. Must be python 3.8+)
    - `Activate` the virtual environment. (Windows: `source venv/Scripts/activate`)
    - Install `Django` using `pip`.
    ```shell script
    mkdir <project_name> && cd $_
    python -m venv venv
    source venv/bin/activate
    # Windows: source venv/Scripts/activate
    python -m pip install --upgrade pip
    ```

2. ### Installing Dependencies
    - Install `Django` v3 using `pip` within your `venv`
    pip install -r requirements.txt
    ```
3. ### Make Database
    - Using `psql`, create a `user` with encrypted `password`.
    - Create a `database` for your project.
    - Give privileges to the `user` for the `database`.
    - Alter `user` to allow for `test database` creation.
    ```shell script
    psql -U postgres
    # psql console 
    CREATE USER <project_name>_user WITH ENCRYPTED PASSWORD '<password>';
    CREATE DATABASE <project_name>_db;
    GRANT ALL PRIVILEGES ON DATABASE <project_name>_db TO <project_name>_user;
    ALTER USER <project_name>_user CREATEDB;
    \q
    ```

4. ### Configuration of the project
    - Create folders for `logs`, and `media`.
    - Copy `local_settings.example` to `local_settings.py`.
    - Update `local_settings.py` with proper `settings`, including `database`.
    ```shell script
    mkdir -p logs && mkdir -p media/uploads
    cp examples/local_settings.example <project_name>/local_settings.py
    
    nano <project_name>/local_settings.py
    # edit local_settings.py
    DB_NAME = '<project_name>_db'
    DB_USER = '<project_name>_user'
    DB_PASS = '<password>'
    ```

5. ### Live the project
    - Run `makemigrations` and `migrate`.
    - Run `tests` and `linting` to assure nothing is broken.
    - Create superuser to access the admin panel.
    - Run django `server` to view the project or application.
    - Generate `coverage` reports locally.
    ```shell script
    python manage.py makemigrations
    python manage.py migrate
    python manage.py test && flake8
    python manage.py createsuperuser
    python manage.py runserver

    ```
   > Browse to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site. Admin site is at url [/manage](http://127.0.0.1:8000/manage) changed from default to keep the project secure. Admin url can be changed in `settings.py` --> `ADMIN_URL`_
    ```

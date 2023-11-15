A couple of utilities for tabletop role-playing games like Dark Heresy, Rogue Trader, etc.

# How to run a test build

1. install Python 3 (3.8 or newer);
2. create and run virtual environment for the application:
```commandline
python -m venv environment_name
source environment_name/bin/activate
```
3. clone the project repository and move to the project directory:
```commandline
git clone https://github.com/KCherkasov/squat-toolbox.git
cd %path_to_repository
```
4. install required packages: `pip install -r requirements.txt`
5. (optional, required to properly use interactive charsheets) ensure that all database migrations are applied:
```commandline
python manage.py makemigrations
python manage.py migrate
```
6. run Django test server: `python manage.py runserver`

As a result you'll have the application available at 127.0.0.1:8000.
To run it on a different port add port number after the `runserver` command: e.g. `python manage.py runserver 8080`
will run the application on 8080 port.
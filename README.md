# Car dealership

Car dealership - it's backend service for users, dealers, suppliers.
RESTful backend on DRF, testing with pytest and ddf

---
## Apps
- authorization (JWT auth)
- users (user profile)
- common (base models for other apps)
- cars (cars and car characteristics)
- customers (clients logic)
- marketing (comapnies marketing campaigns)
- orders (clients and suppliers offers)
- stats (customers, dealers, suppliers statistics)
- dealers (dealer company)
- suppliers (supplier company)

---
## Instalation
1. Clone the repository:

```
$ git clone git@github.com:may42day/car-dealership-backend.git
$ cd car-dealership-backend
```
2. Fill in .env file or use .env_example:
```
$ mv .env_example .env
```

3. Build docker containers:
```
$ docker-compose up -d
```
3. Run migrations:
```
$ docker exec -it car-dealership-backend-1 bash
$ python manage.py migrate
```
4. Application started. Navigate to http://127.0.0.1:8080

Follow instructions below to run only the application:

1. Repeat steps 1,2 above
2. Create a virtual environment:

```
$ pip install -U pipenv
$ pipenv shell
```

3. Install the dependencies:

```
$ pipenv install --system
```

4. Run server and navigate to http://127.0.0.1:8080

```
(venv)$ python3 manage.py runserver
```
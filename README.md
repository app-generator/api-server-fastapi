## [FastAPI (API) Server](https://github.com/app-generator/api-server-fastapi)

Simple **FastAPI Boilerplate** enhanced with `JWT` authentication, `OAuth` via **GitHub**, `SqlAlchemy`, **SQLite** persistence and deployment scripts via Docker - Provided by **[AppSeed](https://appseed.us/)**. It has all the ready-to-use bare minimum essentials and `active versioning` and [support](https://appseed.us/support/).

<br />

> Product Roadmap & `Features`:

| Status | Item | info | 
| --- | --- | --- |
| ✅ | **Up-to-date Dependencies** | - |
| ✅ | [API Definition](https://docs.appseed.us/boilerplate-code/api-unified-definition) |  the unified API structure implemented by this server |
| ✅ | `JWT Authentication` |  (login, logout, register) via `oauth2` |
| ✅ | **OAuth** | via GitHub` |
| ✅ | **Persistence** | `SQLite`, `MySql` |
| ✅ | **Docker** | - |
| ✅ | **Unitary tests** | `minimal suite` |

<br />

 ## ✨ Quick Start in `Docker`

> Get the code

```bash
$ git clone https://github.com/app-generator/api-server-fastapi.git
$ cd api-server-fastapi
```

> Start the app in Docker

```bash
$ docker-compose up --build  
```

Note: The `env.sample` file will be used to set the environment variables for the docker container. Make sure to set them as needed. 
The API server will start using the PORT `5000`.

<br />

## ✨ Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Modules](#modules)
4. [Testing](#testing)

<br />

## ✨ How to use the code

> **Step #1** - Clone the project

```bash
$ git clone https://github.com/app-generator/api-server-flask.git
$ cd api-server-flask
```

<br />

> **Step #2** - create virtual environment using python3 and activate it (keep it outside our project directory)

```bash
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
```

<br />

> **Step #3** - Install dependencies in virtualenv

```bash
$ pip install -r requirements.txt
```

<br />

> **Step #5** - Create a new `.env` file using sample `env.sample`

The meaning of each variable can be found below: 

- `DEBUG`: if `True` the app runs in develoment mode
  - For production value `False` should be used
- `SECRET_KEY`: used in assets management
- `GITHUB_CLIENT_ID`: For GitHub social login
- `GITHUB_SECRET_KEY`: For GitHub social login
- `DATABASE_HOSTNAME`: For Mysql databse
- `DATABASE_PORT`: For Mysql databse
- `DATABASE_PASSWORD`: For Mysql databse
- `DATABASE_NAME`: For Mysql databse
- `DATABASE_USERNAME`: For Mysql databse
- `ALGORITHM`: For JWT Tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES`: For JWT Tokens




<br />

> **Step #6** - start test APIs server at `localhost:5000`

```bash
$ uvicorn src.app:app
```

Use the API via `POSTMAN` or Swagger Dashboard.

![Flask API Server - Swagger Dashboard.](https://user-images.githubusercontent.com/51070104/141950891-ea315fca-24c2-4929-841c-38fb950a478d.png) 

<br />

## ✨ Project Structure

```bash
api-server-flask/
├── src
    ├── helpers
        ├── database.py
        └── utils.py
    ├── routers
        ├── users.py
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── oatuh2.py
│   └── schemas.py
├── tests
    ├── __init__.py
    ├── conftest.py
    ├── database.py
    └── test_users.py
├── Dockerfile
├── docker-compose.yaml
├── README.md
├── requirements.txt
├── run.py
```

<br />

## ✨ API

For a fast set up, use this `POSTMAN` file: [api_sample](https://github.com/app-generator/api-unified-definition/blob/main/api.postman_collection.json)

> **Register** - `api/users/register` (**POST** request)

```
POST api/users/register
Content-Type: application/json

{
    "username":"test",
    "password":"pass", 
    "email":"test@appseed.us"
}
```

<br />

> **Login** - `api/users/login` (**POST** request)

```
POST /api/users/login
Content-Type: application/json

{
    "password":"pass", 
    "email":"test@appseed.us"
}
```

<br />

> **Logout** - `api/users/logout` (**POST** request)

```
POST api/users/logout
Content-Type: application/json
authorization: JWT_TOKEN (returned by Login request)

{
    "token":"JWT_TOKEN"
}
```

<br />

## ✨ Testing

Run tests using `pytest tests.py`

<br />

---
**[FastAPI (API) Server](https://github.com/app-generator/api-server-fastapi)** - provided by [AppSeed](https://appseed.us)



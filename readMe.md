# Movie Finder - Backend
## Development - Cheat Sheet
### Run Dev-Server
The project should start automatically once the dev container gets booted up, but if you want to start it manually:
```shell
fastapi dev main.py
```

### Run Prod-Server
```shell
fastapi run
```
### Download Requirements
The requirements should get installed automatically if you start a dev-container, but just in case:

```shell
pip install -r requirements.txt
```

You also need to create a `.env` file at the project root. You'll have to set the following values:
```.env
POSTGRES_HOST=""
POSTGRES_PORT=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""

REDIS_HOST=""
REDIS_PORT=""

SECRET_KEY =""
ACCESS_TOKEN_EXPIRE_MINUTES=""
REFRESH_TOKEN_EXPIRE_DAYS=""
ALGORITHM=""
```

### Freeze Requirements
```shell
pip freeze > requirements.txt
```

### Access API-Doc
Checkout the API-Doc under this URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Import Hoppscotch-Collection
The collection with the file-name `movieFinder_backendDB.json` can be imported into Hoppscotch. There are also tests configured to check if the endpoints are according as excpected.
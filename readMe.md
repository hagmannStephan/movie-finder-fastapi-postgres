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

SECRET_KEY =""
ACCESS_TOKEN_EXPIRE_MINUTES=""
REFRESH_TOKEN_EXPIRE_DAYS=""
ALGORITHM=""

TMDB_API_KEY=""
```

### Freeze Requirements
```shell
pip freeze > requirements.txt
```

### Access API-Doc
Checkout the API-Doc under this URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Import Hoppscotch-Collection
In the file `movieFinder_backendDB.postman_collection.json` at the project root you can find the export of the endpoints from postman.
The endpoints are configured with tests. To run them properly you need to create an environment with the following variables: `$BASE_URL`, `$ACCESS_TOKEN` and `$REFRESH_TOKEN`
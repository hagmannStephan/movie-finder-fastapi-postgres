# Movie Finder - Backend
You can find the official API documentation, created with Swagger, under the following URL: [api.moviefinder.stephanhagmann.ch/docs](https://api.moviefinder.stephanhagmann.ch/docs)
## Development - Cheat Sheet
### Run the project
After you cloned the repo, you need to create a `.env` file in the project root that contains the following values:
```.env
POSTGRES_HOST="postgres"
POSTGRES_PORT="5432"
POSTGRES_USER="postgres-backend"
POSTGRES_PASSWORD=""
POSTGRES_DB="movieFinder-DB"

SECRET_KEY =""
ACCESS_TOKEN_EXPIRE_MINUTES=""
REFRESH_TOKEN_EXPIRE_DAYS=""
ALGORITHM=""

TMDB_API_KEY=""
BASE_URL="https://api.themoviedb.org/3"
```

Since all dependencies get installed on startup of the container and the app also gets started up, you just need to run this command:
```bash
docker compose up
```

### Manage requirements
If you want to download the requirements that got added since you created the container, you need to execute this command:
```bash
pip install -r requirements.txt
```

In case you installed new requirements, you need to run this command:
```shell
pip freeze > requirements.txt
```

### Use Postman Collection
The [Postman Collection](movieFinder_backendDB.postman_collection.json) helps you test if all the endpoints work properly. There are integrated tests, to check if return codes, etc. match the expected value.
To execute the requests in Postman, you need to create an Environment with the following values:

- `$BASE_URL` (probably 127.0.0.1:8000)
- `$ACCESS_TOKEN` (you can set this once you gain your access token)
- `$REFRESH_TOKEN` (you can set this once you gain your refresh token)
- `$USER_ID` (you can set this once you created a user)
- `$NAME` (you can choose this freely)
- `$EMAIL` (you can choose this freely, but it needs to be unique in the DB)
- `$PASSWORD` (you can choose this freely)
- `$MOVIE_ID` (you can set this based on the action you want to perform)
- `$GROUP_ID` (you can set this based on the action you want to perform)
- `$FRIENDSHIP_CODE` (you can set this based on the action you want to perform)
- `$MEMBER_ID` (you can set this based on the action you want to perform)
- `$KEYWORDS` (you can set this based on the action you want to perform)


# Attribution
<a href="https://www.themoviedb.org/" target="_">
<img src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_short-8e7b30f73a4020692ccca9c88bafe5dcb6f8a62a4c6bc55cd9ba82bb2cd95f6c.svg" alt="TMDB Logo" width="100px" style="margin: 10px 0 15px 0;">
</a>

**This app uses [TMDB](https://www.themoviedb.org/) and the [TMDB APIs](https://developer.themoviedb.org/docs/getting-started) but is not endorsed, certified, or otherwise approved by TMDB.**
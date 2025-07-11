from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resources.services.postgresql_service import engine
from resources.services.postgresql_service import Base
import resources.routers as routers
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

app = FastAPI(
    title="Movie Finder - Backend",
    description="""
MovieFinder Backend with FastAPi and PostgreSQL.

## Attribution

<a href="https://www.themoviedb.org/" target="_"><img src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_short-8e7b30f73a4020692ccca9c88bafe5dcb6f8a62a4c6bc55cd9ba82bb2cd95f6c.svg" alt="TMDB Logo" width="80px" style="margin: 10px 0 15px 0;"></a>
**This app uses [TMDB](https://www.themoviedb.org/) and the [TMDB APIs](https://developer.themoviedb.org/docs/getting-started) but is not endorsed, certified, or otherwise approved by TMDB.**

Some data, including streaming availability, is provided by JustWatch. Attribution is required by TMDB.
    """,
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"🔥 Unhandled Exception: {tb}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}

# `auth`-Endpoints
app.include_router(routers.auth_router)

# `user`-Endpoints
app.include_router(routers.user_router)

# `group`-Endpoints
app.include_router(routers.group_router)

# `movie`-Endpoints
app.include_router(routers.movie_router)
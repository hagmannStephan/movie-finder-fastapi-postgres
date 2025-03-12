from fastapi import FastAPI
from resources.services.postgresql_service import engine
from resources.services.postgresql_service import Base
import resources.routers as routers

 
app = FastAPI(
    title="Movie Finder - Backend",
    description="MovieFinder Backend with FastAPi and PostgreSQL",
    version="0.1.0"
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

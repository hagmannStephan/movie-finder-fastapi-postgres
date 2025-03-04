from .auth_routes import router as auth_router
from .movie_routes import router as movie_router

__all__ = ["auth_router", "movie_router"]
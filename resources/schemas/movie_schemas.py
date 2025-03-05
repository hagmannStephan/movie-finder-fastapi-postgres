from pydantic import BaseModel

class MovieBase(BaseModel):
    movie_id: int
    original_title: str
    cover_image_src: str

class Movie(MovieBase):
    pass

    class Config:
        from_attributes = True
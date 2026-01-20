from sqlmodel import SQLModel

class GamePublic(SQLModel):
    id: int
    steam_id: int
    title: str
    release_date: str
    price: float
    image_url: str
    genres: str
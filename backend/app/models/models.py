from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    steam_id: int = Field(unique=True, index=True)  
    title: str = Field(index=True)               
    release_date: Optional[str] = None
    price: float = Field(default=0.0)
    image_url: Optional[str] = None               
    genres: Optional[str] = None                   

    # Relacionamento: Um jogo pode estar na lista de vários usuários
    user_logs: List["UserGameLog"] = Relationship(back_populates="game")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

    games_logs: List["UserGameLog"] = Relationship(back_populates="user")

class UserGameLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    game_id: int = Field(foreign_key="game.id")
    list_type: str     # 'WISHLIST', 'PLAYING', 'COMPLETED'

    priority: Optional[int] = None   # Prioridade (Wishlist)
    progress: Optional[int] = None   # % Concluído (Playing)
    rating: Optional[int] = None     # Nota 1-5 (Completed)
    review: Optional[str] = None     # Texto (Completed)
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="games_logs")
    game: Game = Relationship(back_populates="user_logs")
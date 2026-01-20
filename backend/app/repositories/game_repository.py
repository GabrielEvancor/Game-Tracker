from typing import List, Optional
from sqlmodel import Session, select, col 

from app.models.models import Game
from app.repositories.base import BaseRepository

class GameRepository(BaseRepository[Game]):
    def __init__(self, session: Session):
        super().__init__(session, Game)
        
    def get_filtered(
        self,
        skip: int = 0,
        limit: int = 20,
        title_contains: Optional[str] = None,
        genre: Optional[str] = None,
        max_price: Optional[float] = None
    ) -> List[Game]:
        
        statement = select(Game)

        if title_contains:
            statement = statement.where(col(Game.title).ilike(f"%{title_contains}%"))
        
        if genre:
            statement = statement.where(col(Game.genres).ilike(f"%{genre}%"))
            
        if max_price is not None:
            statement = statement.where(Game.price <= max_price)

        statement = statement.order_by(Game.price)
        statement = statement.offset(skip).limit(limit)
        
        return self.session.exec(statement).all()
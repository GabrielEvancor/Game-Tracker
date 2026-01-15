from select import select
from typing import List, Optional

from sqlmodel import col
from backend.app.models.models import Game
from backend.app.repositories.base import BaseRepository


class GameRepository(BaseRepository[Game]):
    
    def __init__(self, session, model):
        super().__init__(session, model)
        
    def get_filtered(
        self,
        skip: int = 0,
        limit = 20,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        max_price: Optional[float] = None
    ) -> List[Game]:
        
        statement = select(Game)

        # 1. Filtros
        if title:
            statement = statement.where(col(Game.title).icontains(title))
        
        if genre:
            statement = statement.where(col(Game.genres).icontains(genre))
            
        if max_price is not None:
            statement = statement.where(Game.price <= max_price)

        #Ordenaçao por preços
        statement = statement.order_by(Game.price)
        statement = statement.offset(skip).limit(limit)
        
        return self.session.exec(statement).all()
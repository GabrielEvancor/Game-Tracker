from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlmodel import Session
from app.core.database import get_session
from app.models.models import Game
from app.schemas.game import GamePublic
from app.repositories.game_repository import GameRepository

# Cria o roteador
router = APIRouter(prefix="/games", tags=["games"])


# Pega a sessão do banco e entrega o GameRepository pronto.
def get_game_repo(session: Session = Depends(get_session)) -> GameRepository:
    return GameRepository(session)

@router.get("/", response_model=List[GamePublic])
def read_games(
    # (Query Params)
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = Query(None, description="Filtrar por nome do jogo"),
    genre: Optional[str] = Query(None, description="Filtrar por categoria"),
    max_price: Optional[float] = Query(None, description="Preço máximo desejado"),
    repo: GameRepository = Depends(get_game_repo)
):
    """
    Lista os jogos do catálogo.
    Permite filtrar por nome, gênero e preço máximo.
    Sempre retorna ordenado do mais barato para o mais caro.
    """
    # A Rota apenas "repassa" o pedido para o Repositório
    return repo.get_filtered(
        skip=skip, 
        limit=limit, 
        title_contains=search, 
        genre=genre,
        max_price=max_price
    )
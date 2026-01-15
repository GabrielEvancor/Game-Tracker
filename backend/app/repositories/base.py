from typing import Generic, TypeVar, Type, List, Optional
from sqlmodel import Session, select, SQLModel

# T é um "placeholder". Significa que essa classe aceita User, Game, ou qualquer Model.
T = TypeVar("T", bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        """Busca um item pelo ID."""
        return self.session.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Retorna todos os itens com paginação simples."""
        statement = select(self.model).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create(self, entity: T) -> T:
        """Salva um novo item no banco."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        """Atualiza um item existente."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T):
        """Remove um item do banco."""
        self.session.delete(entity)
        self.session.commit()
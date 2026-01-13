from sqlmodel import SQLModel, create_engine, Session

# Define o nome do banco de dados SQLite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False é necessário para SQLite + FastAPI
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    """Cria as tabelas no banco de dados baseadas nos modelos importados."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Gera uma sessão para ser usada nas rotas da API."""
    with Session(engine) as session:
        yield session
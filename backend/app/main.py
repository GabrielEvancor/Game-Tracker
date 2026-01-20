from fastapi import FastAPI
from app.routers import games

app = FastAPI(title="MyGameTracker API")

# 2. Conectamos o roteador ao app principal
app.include_router(games.router)

@app.get("/")
def root():
    return {"message": "API rodando! Acesse /docs para ver a documentação."}
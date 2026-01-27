from fastapi import FastAPI
# 1. Importe o Middleware de CORS
from fastapi.middleware.cors import CORSMiddleware 
from app.routers import games

app = FastAPI(title="MyGameTracker API")

# Quem pode acessar sua API
origins = [
    "http://localhost:4200",     
    "http://127.0.0.1:4200",    
    "http://localhost:3000",     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],    
)

app.include_router(games.router)

@app.get("/")
def root():
    return {"message": "API Online"}
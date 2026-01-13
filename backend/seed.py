import csv
import sys
import os
import re

# Ajuste de diretório
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.core.database import engine, create_db_and_tables
from app.models.models import Game

CSV_FILE_PATH = "app/data/games.csv"

# LISTA EXPANDIDA PARA NÃO PERDER NADA
# Cobrindo os principais termos usados na Steam
COMMON_GENRES = [
    "Action", "Adventure", "Indie", "RPG", "Strategy", "Simulation", 
    "Casual", "Sports", "Racing", "Massively Multiplayer", "Early Access",
    "Free to Play", "Violent", "Gore", "Sexual Content", "Nudity", 
    "Anime", "Horror", "Puzzle", "Platformer", "Sci-fi", "Shooter", 
    "Visual Novel", "Fantasy", "Arcade", "Fighting", "Music", "Educational",
    "Card", "Board", "Dating Sim", "Utilities", "Design", "Web Publishing"
]

def is_date(text):
    # Procura por anos entre 1900 e 2099
    # Exemplo: "Oct 21, 2008" ou apenas "2023"
    if len(text) > 30: return False # Datas não são frases longas
    return re.search(r'\b(19|20)\d{2}\b', text) is not None

def is_genre(text):
    text_lower = text.lower()
    
    # TRAVA 1: Anti-URL
    if "http" in text_lower: return False
    
    # TRAVA 2: Anti-Descrição (Crucial!)
    # Descrições de jogos são longas. Listas de gêneros são curtas (geralmente < 250 chars).
    # Se o texto for muito grande, ignoramos, pois provavelmente é o "About the game".
    if len(text) > 250: return False
    
    # TRAVA 3: Verificação de Palavras-Chave
    for g in COMMON_GENRES:
        if g.lower() in text_lower:
            return True
            
    return False

def seed_games():
    print("--- 1. Criando tabelas ---")
    create_db_and_tables()
    
    print(f"--- 2. Lendo CSV com Busca Blindada (Gêneros Seguros) ---")
    
    with Session(engine) as session:
        # Verifica se já tem dados
        if session.exec(select(Game)).first():
            print("AVISO: O banco já contém dados. Delete 'database.db' para refazer.")
            return

        try:
            with open(CSV_FILE_PATH, mode='r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                next(reader, None) # Pula cabeçalho
                
                buffer = []
                count = 0
                
                for row in reader:
                    if not row: continue

                    try:
                        # 1. Busca ID (SteamID)
                        try:
                            steam_id = int(row[0])
                        except ValueError:
                            continue 

                        title = row[1]

                        # --- BUSCA INTELIGENTE ---
                        image_url = ""
                        release_date = ""
                        genres = ""
                        
                        # Varre a linha item por item
                        for item in row:
                            item_str = str(item).strip()
                            
                            # A. Imagem (Link da Akamai)
                            if "http" in item_str and ("header" in item_str or "capsule" in item_str) and ".jpg" in item_str:
                                image_url = item_str
                            
                            # B. Data (Tem ano e é curta)
                            elif not release_date and is_date(item_str):
                                release_date = item_str
                                
                            # C. Gêneros (Tem keyword, não é URL e é curto)
                            # Verificamos 'item_str != title' para não pegar o nome do jogo como gênero
                            elif not genres and item_str != title and is_genre(item_str):
                                genres = item_str

                        # Preço (Tentativa de fallback)
                        price = 0.0
                        try:
                            if len(row) > 6:
                                val = row[6].lower()
                                if "free" in val: price = 0.0
                                else: price = float(val)
                        except:
                            price = 0.0

                        # Cria o objeto Game
                        game = Game(
                            steam_id=steam_id,
                            title=title,
                            release_date=release_date, 
                            price=price,
                            image_url=image_url,
                            genres=genres 
                        )
                        
                        buffer.append(game)
                        count += 1

                        if len(buffer) >= 1000:
                            session.add_all(buffer)
                            session.commit()
                            buffer = []
                            print(f"Processados: {count} jogos...")

                    except Exception:
                        continue

                if buffer:
                    session.add_all(buffer)
                    session.commit()

            print(f"\n--- SUCESSO! {count} jogos salvos com segurança. ---")

        except FileNotFoundError:
            print("Arquivo games.csv não encontrado na pasta data.")

if __name__ == "__main__":
    seed_games()
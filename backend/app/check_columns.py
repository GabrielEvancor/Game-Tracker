import csv

# Garanta que o nome do arquivo aqui é o mesmo que você baixou
CSV_FILE = "data/games.csv" 

try:
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader) # Pega apenas a primeira linha (cabeçalho)
        
        print("\n--- NOMES DAS COLUNAS ENCONTRADAS ---")
        for i, col in enumerate(headers):
            print(f"{i}: {col}")
            
except FileNotFoundError:
    print(f"Erro: Não encontrei o arquivo em '{CSV_FILE}'. Verifique a pasta 'data'.")
except Exception as e:
    print(f"Erro ao ler: {e}")
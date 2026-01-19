import requests
import json

# --- SUBSTITUA APENAS ESTES DOIS ---
NOTION_TOKEN = "SEU_SECRET_AQUI"
DATABASE_ID = "SEU_ID_AQUI"
# ----------------------------------

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def enviar_teste():
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": "Conexão de Sucesso do Fernando!"}}]
            }
        }
    }
    
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if res.status_code == 200:
        print("✅ FUNCIONOU! Verifique seu Notion agora.")
    else:
        print(f"❌ Erro {res.status_code}: {res.text}")

if __name__ == "__main__":
    enviar_teste()
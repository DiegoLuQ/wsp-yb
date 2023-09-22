from pathlib import Path
from dotenv import load_dotenv
from os import environ

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

class Settings:
    token = environ.get('TOKEN')
    wsp_token = environ.get('WSP_TOKEN')
    wsp_url = environ.get('WSP_URL')
    stickers = {
    "poyo_feliz": 984778742532668,
    "perro_traje": 1009219236749949,
    "perro_triste": 982264672785815,
    "pedro_pascal_love": 801721017874258,
    "pelfet": 3127736384038169,
    "anotado": 24039533498978939,
    "gato_festejando": 1736736493414401,
    "okis": 268811655677102,
    "cachetada": 275511571531644,
    "gato_juzgando": 107235069063072,
    "chicorita": 3431648470417135,
    "gato_triste": 210492141865964,
    "gato_cansado": 1021308728970759
}
    doc_url = "https://biostoragecloud.blob.core.windows.net/resource-udemy-whatsapp-node/document_whatsapp.pdf"

settings = Settings()

# print(settings.stickers.get('perro_traje'))
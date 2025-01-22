import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from pydantic import BaseModel

# Initialiseer de Firebase Admin SDK
cred = credentials.Certificate("pad/naar/jouw/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

# Verkrijg een referentie naar de Firestore-database
db = firestore.client()

app = FastAPI()

# Lijsten van landen, datums en inhoud
landen = {
    "01": "Nederland", "02": "België", "03": "Duitsland", "04": "Frankrijk", "05": "Spanje", 
    "06": "Italië", "07": "Verenigd Koninkrijk", "08": "Verenigde Staten", "09": "Canada", "10": "Australië",
    # Voeg hier de rest van de landen toe tot 99
}

datums = {str(i).zfill(3): f"{(i-1)//31+1:02d}-{(i-1)%31+1:02d}" for i in range(1, 366)}

inhoud = {
    "1": "Document", "2": "Audio", "3": "Video", "4": "Afbeelding", "5": "Tekst", 
    "6": "Spreadsheet", "7": "Software", "8": "Webpagina", "9": "Presentatie", "10": "Archief"
}

# Definieer de structuur van de verwachte data
class Data(BaseModel):
    hexCode: str

@app.post("/process_data")
async def process_data(data: Data):
    # Ontleed de hex-code
    hexCode = data.hexCode.lstrip('#')  # Verwijder de '#' aan het begin van de hex-code

    # Split de hex-code in de verschillende onderdelen
    land_code = hexCode[:2]  # Eerste 2 cijfers voor het land
    datum_code = hexCode[2:5]  # Volgende 3 cijfers voor de datum
    inhoud_code = hexCode[5:6]  # Laatste cijfer voor de inhoud

    # Verkrijg de waarden uit de lijsten
    land = landen.get(land_code, "Onbekend land")
    datum = datums.get(datum_code, "Onbekende datum")
    inhoud_item = inhoud.get(inhoud_code, "Onbekende inhoud")

    # Gegevens die naar Firestore moeten worden geüpload
    data_to_upload = {
        "land": land,
        "datum": datum,
        "inhoud": inhoud_item
    }

    # Voeg de gegevens toe aan een Firestore-collectie
    doc_ref = db.collection("container_data").add(data_to_upload)

    return {"message": "Data succesvol opgeslagen in Firestore", "data": data_to_upload}

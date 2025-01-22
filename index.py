from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Definieer de structuur van de verwachte data
class Data(BaseModel):
    hexCode: str

@app.post("/process_data")
async def process_data(data: Data):
    # Ontleed de hex-code
    hexCode = data.hexCode.lstrip('#')  # Verwijder de '#' aan het begin van de hex-code

    # Split de hex-code in de verschillende onderdelen
    land = hexCode[:2]  # Eerste 2 cijfers voor het land
    datum = hexCode[2:5]  # Volgende 3 cijfers voor de datum
    inhoud = hexCode[5:6]  # Laatste cijfer voor de inhoud

    # Print de onderdelen voor controle
    print(f"Land: {land}, Datum: {datum}, Inhoud: {inhoud}")

    # Hier kun je de data verder verwerken (bijvoorbeeld opslaan in een database)
    
    return {"message": "Data ontvangen en verwerkt", "land": land, "datum": datum, "inhoud": inhoud}

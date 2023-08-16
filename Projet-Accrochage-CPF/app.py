
from fastapi import FastAPI
from mangum import Mangum
import upload_file_certifie as fc
import xml_handler as xh
import requests
import json
import asyncio
from fastapi.encoders import jsonable_encoder


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "ok": True}

# Permet la lecture et le chargement dans bubble d'un fichier certifié
# Statut : 

@app.post('/file/certifie/')
async def upload_file_certifie(full_path: str, format: str, info_diplome: str, mode : str, authorisation : str):
    return fc.file_handler(full_path,format,info_diplome,mode,authorisation)

# Génère un fichier xml à partir de la base de données Bubble
@app.post('/file/xml/source/')
async def generate_xml(constraint : str,idFlux : str, idEmetteur : str,idCertificateur :str, idContrat: str, authorisation : str):
    return xh.generate_xml(constraint,idFlux, idEmetteur, idCertificateur, idContrat, authorisation)

# lit un accusé de traitement et envoi le résultat dans Bubble

@app.post('/file/xml/accuse_de_traitement/{xml_file}')
async def handler_accuse_de_traitement(constraint: str):
    return True

@app.post('/file/xml/accuse_de_traitement/{xml_file}')
async def handler_accuse_de_traitement(constraint: str):
    return True
@app.get('/token/')
async def get_token(email : str, password : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/wf/gettoken?"
    
    payload = {'email': email,
    'password': password}
    files=[

    ]
    headers = {
  'Authorization': 'Bearer 0112034227b4c84ccab69fa6b7b777e1'
  }
    
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    print(jsonable_encoder(response.text) )
    return jsonable_encoder(response.text)  

#asyncio.run(get_token("test1@gmail.com","Paris"))
lambda_handler = Mangum(app = app, lifespan="off")
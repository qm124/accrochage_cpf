from pydantic import BaseModel, ValidationError, validator, root_validator, parse_obj_as, Field
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)
from datetime import datetime, date
import pandera as pa
from pandera.engines.pandas_engine import PydanticModel
import requests
import pandas as pd
import io
from fastapi.encoders import jsonable_encoder
from pydantic.json import pydantic_encoder
import json


[{"Modified Date":"2023-06-16T15:41:31.523Z","Created Date":"2023-06-16T15:40:28.033Z","Created By":"admin_user_accrochagecertification_test",
  "fichier_source_custom_file_uploaded":"1686903060231x811290295024736300","accus__de_traitement_custom_file_uploaded":"1686903060231x811290295024736300",
  "id_flux1_text":"dzadzazd","nb_passage_ko_number":11,"nb_passage_ok_number":12,
  "statut_du_traitement_option_statut_fichier":"Nouveau","_id":"1686930028033x894047398629218800"}]

class couple_xml(BaseModel):
    fichier_source_custom_file_uploaded : Optional[str]
    accus__de_traitement_custom_file_uploaded : Optional[str]
    id_flux1_text : Optional[str]
    nb_passage_ko_number : Optional[int]
    nb_passage_ok_number : Optional[int]
    statut_du_traitement_option_statut_fichier : Optional[str]
    id : Optional[str] = Field(None, alias='_id',exclude=True)

def get_couple_xml(constraint : str , headers : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/couple XML?constraints=+"+ constraint 
    response = requests.get(url, headers = headers)
    urlData = response.content
    print(response.text)
    #print(urlData)
    rawData = pd.read_json(io.StringIO(urlData.decode('utf-8')),orient='index')
    print(rawData['results'].to_json())
    print(rawData)
    items = parse_obj_as(List[couple_xml], rawData['results']['response'])
    print(items)
    print(items[0].id)
    #print(rawData['results']['response'])
    return items

def post_couple_xml(data : couple_xml, headers : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/couple XML/bulk"
    data = json.dumps(data, default=pydantic_encoder, allow_nan=False).replace("[","").replace("]","").replace("}, {","}\n{")
    print(data)
    response = requests.post(url, headers = headers,data=data)
    print(response.text)
    return response

def update_couple_xml(data : couple_xml, headers : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/couple XML/"+data.id
    data = json.dumps(data, default=pydantic_encoder)
    response = requests.put(url, headers = headers,data=data)
    print(response.text)
    return response.text



myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'text/plain'
    }
#get_couple_xml('[]',myHeaders)
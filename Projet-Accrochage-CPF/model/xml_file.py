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





class xml_file(BaseModel) : 
    id : Optional[str] = Field(None, alias='_id',exclude=True)
    name_text : Optional[str]
    file_url_text : Optional[str]
    id_flux_text : Optional[str]
    #id_traitement_text : Optional[str]
    nb_passage_ko_number : Optional[int]
    nb_passage_ok_number : Optional[int]
    statut_text : Optional[str]
    type_de_fichier_option_file_type : Optional[str]
    #statut_du_traitement_option_statut_fichier : Optional[str]

def get_xml_file(constraint : str , headers : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/XML file?constraints=+"+ constraint 
    response = requests.get(url, headers = headers)
    print(response.text)
    urlData = response.content
    try :
        rawData = pd.read_json(io.StringIO(urlData.decode('utf-8')),orient='index')
        items = parse_obj_as(List[xml_file], rawData['results']['response'])
        print(items)
        return items
    except :
        print("Aucun fichier xml trouvé")
        return False

def post_xml_file(data : xml_file, headers : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/XML file/bulk"
    data = json.dumps(data, default=pydantic_encoder, allow_nan=False).replace("[","").replace("]","").replace("}, {","}\n{")
    print(data)
    response = requests.post(url, headers = headers,data=data)
    print(response.text)
    return response


def generate_constraint(key: str, constraint_type: str, value: str):
    return  "{ \"key\": \""+key+"\", \"constraint_type\": \""+constraint_type+"\", \"value\": \""+value+"\" }"

print(generate_constraint("nomFichier", "text contains", "Accusé de traitement"))

myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'text/plain'
    }

""""""
#Zone de test   
"""
constraint = "["+str(generate_constraint("idTraitement", "equals", "lnf00000-0000-0000-0000-000000000008.xml"))+"]"
constraint = "[ { \"key\": \"idTraitement\", \"constraint_type\": \"equals\", \"value\": \"1\" }]"
#print(constraint)
constraint2="["+str(generate_constraint("idTraitement", "equals", "1"))+"]"
print(constraint)
print(constraint2)

a=get_xml_file(constraint2,myHeaders)
post_xml_filetest = xml_file(name_text="test",file_url_text="test")
print(a[0])
post_xml_file(a,myHeaders)   
"""
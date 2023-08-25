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

def generate_constraint(key: str, constraint_type: str, value: str):
    return  "{ \"key\": \""+key+"\", \"constraint_type\": \""+constraint_type+"\", \"value\": \""+value+"\" }"

class certification(BaseModel):    
    code_certification_text : Optional[str]
    nature_deposant_text : Optional[str]
    titre_grade_text : Optional[str]
    type_de_certif_text : Optional[str]
    entreprise_custom_company : Optional[str]
    nom_de_la_certification_text : Optional[str]
    certificateur_text : Optional[str]
    template_list_text : Optional[List[str]]
    id : Optional[str] = Field(None, alias='_id',exclude=True)


def get_certification(constraint : str , headers : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/certification?constraints=+"+ constraint 
    response = requests.get(url, headers = headers)
    urlData = response.content
    rawData = pd.read_json(io.StringIO(urlData.decode('utf-8')),orient='index')
    items = parse_obj_as(List[certification], rawData['results']['response'])
    print(items)
    print(items[0].id)
    return items

def build_xlsx_template(certification : certification) : 
    excel_template = pd.DataFrame(columns=certification.template_list_text)
    print(excel_template)
    with pd.ExcelWriter('template '+ certification.nom_de_la_certification_text+'.xlsx') as writer:
        excel_template.to_excel(writer, sheet_name='Template',index=False)

myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'text/plain'
    }

#1692890827220x296561699555639300
a=get_certification('[{"key": "_id", "constraint_type": "in", "value": ["1692890827220x296561699555639300"]}]',myHeaders)
b=build_xlsx_template(a[0])

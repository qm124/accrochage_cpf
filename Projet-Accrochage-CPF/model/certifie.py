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

def valid_date_format(date_text):
    return True



class Certifie(BaseModel):

    idtechnique_text : Optional[str]
    urlpreuve_text : Optional[str]
    libelleoption_text : Optional[str]
    obtentioncertification_text : Optional[str]
    donneecertifiee_text : Optional[str]
    datedebutexamen_date : Optional[datetime]
    datefinexamen_date : Optional[datetime]
    modalitepassageexamen_text : Optional[str]
    codepostalcentreexamen_text : Optional[str]
    datedebutvalidite_date : Optional[datetime]
    datefinvalidite_date : Optional[datetime]
    presenceniveaulangueeuro_text : Optional[str]
    niveaulangueeuropeen_text : Optional[str]
    presenceniveaunumeriqueeuro_text : Optional[str]
    scoring_text : Optional[str]
    mentionvalidee_text : Optional[str]
    verbatim_text : Optional[str]
    modaliteacces_text : Optional[str]
    voieaccessvae_text : Optional[str]
    initiativeinscription_text : Optional[str]
    dateinscription_date : Optional[datetime]
    
    nomnaissance_text : Optional[str]
    nomusage_text : Optional[str]
    prenom1_text : Optional[str]
    prenom2_text : Optional[str]
    prenom3_text : Optional[str]
    anneenaissance_number : Optional[int]
    moisnaissance_number : Optional[int]
    journaissance_number : Optional[int]
    sexe_text : Optional[str]
    codeinsee_text : Optional[str]
    codepostal_text : Optional[str]
    libellecommunenaissance_text : Optional[str]
    codepayspaissance_text : Optional[str]
    libellepaysnaissance_text : Optional[str]

    iddossier_text : Optional[str]
    nomtitulaire_text : Optional[str]
    prenom1titulaire_text : Optional[str]
    
    validation_idtechnique_text : Optional[str]
    validation_urlpreuve_text : Optional[str]
    validation_libelleoption_text : Optional[str]
    validation_obtentioncertification_text : Optional[str]
    validation_donneecertifiee_text : Optional[str]
    validation_datedebutexamen_text : Optional[str]
    validation_datefinexamen_text : Optional[str]
    validation_modalitepassageexamen_text : Optional[str]
    validation_codepostalcentreexamen_text : Optional[str]
    validation_datedebutvalidite_text : Optional[str]
    validation_datefinvalidite_text : Optional[str]
    validation_presenceniveaulangueeuro_text : Optional[str]
    validation_niveaulangueeuropeen_text : Optional[str]
    validation_presenceniveaunumeriqueeuro_text : Optional[str]
    validation_scoring_text : Optional[str]
    validation_mentionvalidee_text : Optional[str]
    validation_verbatim_text : Optional[str]
    validation_modaliteacces_text : Optional[str]
    validation_voieaccessvae_text : Optional[str]
    validation_initiativeinscription_text : Optional[str]
    validation_dateinscription_text : Optional[str]

    validation_nomnaissance_text : Optional[str]
    validation_nomusage_text : Optional[str]
    validation_prenom1_text : Optional[str]
    validation_prenom2_text : Optional[str]
    validation_prenom3_text : Optional[str]
    validation_anneeNaissance_text : Optional[str]
    validation_moisnaissance_text : Optional[str]
    validation_journaissance_text : Optional[str]
    validation_sexe_text : Optional[str]
    validation_codeinsee_text : Optional[str]
    validation_codepostal_text : Optional[str]
    validation_libellecommunenaissance_text : Optional[str]
    validation_codepaysnaissance_text : Optional[str]
    validation_libellepaysnaissance_text : Optional[str]

    validation_iddossier_text : Optional[str]
    validation_nomtitulaire_text : Optional[str]
    validation_prenom1titulaire_text : Optional[str]


def generate_constraint(key: str, constraint_type: str, value: str):
    return  "{ \"key\": \""+key+"\", \"constraint_type\": \""+constraint_type+"\", \"value\": \""+value+"\" }"    

def get_certifie(constraint : str , headers : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/certifie?constraints=+"+ constraint 
    response = requests.get(url, headers = headers)
    print(response.text)
    urlData = response.content
    try :
        rawData = pd.read_json(io.StringIO(urlData.decode('utf-8')),orient='index')
        items = parse_obj_as(List[Certifie], rawData['results']['response'])
        print(items)
        return items
    except :
        print("Aucun fichier certifié trouvé")
        return False    


    @root_validator()
    def idtechnique_text_validator(cls, values):
        if values['idtechnique_text'] is None :
            values['validation_idtechnique_text'] = "L'id technique est obligatoire. Du moment qu'il est unique pour chaque passage de certification de l'émetteur, il n'y a pas d'autres contraintes de nommage."
            return values
        if len(values['idtechnique_text'])>255:
            values['validation_idtechnique_text'] = "L'id technique ne doit pas dépasser 255 caractères"
        return values
    
    @root_validator()
    def urlpreuve_textValidator(cls, values):
        if values['urlpreuve_text'] is None :
            return values
        if len(values['urlpreuve_text'])>255:
            values['validation_urlpreuve_text'] = "L'urlpreuve ne doit pas dépasser 255 caractères"
        return values



    @root_validator()
    def libelleoption_textValidator(cls, values):
        if values['libelleoption_text'] is None :
            return values
        if len(values['libelleoption_text'])>255:
            values['validation_libelleoption_text'] = "Le libelleoption ne doit pas dépasser 255 caractères"
        return values 


    @root_validator()
    def obtentioncertification_text_validator(cls, values):
        if values['obtentioncertification_text'] is None :
            values['validation_obtentioncertification_text'] = "L'obtentioncertification est obligatoire. L'obtention est 'PAR_ADMISSION' si le dossier et les notes du candidat sont évalués pour lui décerner la certification.L'obtention est 'PAR_scoring_text' si le candidat doit atteindre un certain score pour obtenir la certification"
            return values
        if values['obtentioncertification_text']!="PAR_ADMISSION" and values['obtentioncertification_text']!="PAR_scoring_text":
            values['validation_obtentioncertification_text'] = "L'obtentioncertification est obligatoire. L'obtention est 'PAR_ADMISSION' si le dossier et les notes du candidat sont évalués pour lui décerner la certification.L'obtention est 'PAR_scoring_text' si le candidat doit atteindre un certain score pour obtenir la certification"
        return values
    """   
    @root_validator()
    def donneecertifiee_text_validator(cls, values):
        if values['donneecertifiee_text'] is None :
            values['validation_donneecertifiee_text'] = "donneecertifiee est obligatoire. Indique si le résultat du passage de la certification est temporaire au moment de l’envoi des données à la Caisse des Dépôts (false) ou s’il est définitif (true)."
            return values
        if values['donneecertifiee_text']!="true" and values['obtentioncertification_text']!="false":
            values['validation_donneecertifiee_text'] = "donneecertifiee est obligatoire. Indique si le résultat du passage de la certification est temporaire au moment de l’envoi des données à la Caisse des Dépôts (false) ou s’il est définitif (true)."
        return values

    @root_validator()
    def modalitepassageexamen_textValidator(cls, values):
        if values['modalitepassageexamen_text'] is None :
            return values
        if values['modalitepassageexamen_text']!="A_DISTANCE" and values['modalitepassageexamen_text']!="EN_PRESENTIEL" and values['modalitepassageexamen_text']!="MIXTE":
            values['validation_modalitepassageexamen_text'] = "Facultatif, précise si l'examen a été passé en présentiel, à distance ou les deux. Les valeurs possibles sont : 'A_DISTANCE', 'EN_PRESENTIEL', 'MIXTE'"
        return values

    @root_validator()
    def codepostalcentreexamen_textValidator(cls, values):
        if values['codepostalcentreexamen_text'] is None :
            return values
        if len(values['codepostalcentreexamen_text'])>9:
            values['validation_codepostalcentreexamen_text'] = "Le codepostalcentreexamen_text ne doit pas dépasser 9 caractères"
        return values
    @root_validator()
    def presenceniveaulangueeuro_textValidator(cls, values):
        if values['presenceniveaulangueeuro_text'] is None :
            values['validation_presenceniveaulangueeuro_text'] = "Indique si le candidat a passé une certification en langue européenne. Les valeurs possibles sont : 'true', 'false'"
            return values
        if values['presenceniveaulangueeuro_text']!="true" and values['presenceniveaulangueeuro_text']!="false":
            values['validation_presenceniveaulangueeuro_text'] = "Indique si le candidat a passé une certification en langue européenne. Les valeurs possibles sont : 'true', 'false'"
        return values

    @root_validator()
    def niveaulangueeuropeen_textValidator(cls, values):
        if values['presenceniveaulangueeuro_text'] is "true":
            if values['niveaulangueeuropeen_text'] is None :
                values['validation_niveaulangueeuropeen_text'] = "Niveau européen de la langue passée par le candidat. Les valeurs possibles sont : 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'"
                return values
            if values['niveaulangueeuropeen_text']!="A1" and values['niveaulangueeuropeen_text']!="A2" and values['niveaulangueeuropeen_text']!="B1" and values['niveaulangueeuropeen_text']!="B2" and values['niveaulangueeuropeen_text']!="C1" and values['niveaulangueeuropeen_text']!="C2" and values['niveaulangueeuropeen_text']!="INSUFFISANT":
                values['validation_niveaulangueeuropeen_text'] = "Niveau européen de la langue passée par le candidat. Les valeurs possibles sont : 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'INSUFFISANT'"
            return values


    """


class CertifieSchema(pa.DataFrameModel):
    class Config:
        """Config with dataframe-level data type."""

        dtype = PydanticModel(Certifie)
        coerce = True

### Zone de Test
myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'text/plain'
    }
"""
constraint = "["+generate_constraint("IdTechnique","in","['IDTECHNIQUE']")+"]"
print(constraint)
get_certifie("[]",myHeaders)
"""
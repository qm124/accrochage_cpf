import pandas as pd
import requests
import io
import model.certifie as mc
import numpy as np
import json
from fastapi.encoders import jsonable_encoder
import xlwings as xw


# Etape 1 : récupération du fichier
# Etape 2 : récupération du type de fichier (csv, xls)
# Etape 3 : Validation des données présentes dans le fichier par rapport au containte du dictionnaire + des infos_diplome
# Etape 4 : Croisement des données avec les données déjà présentent dans Bubble
# Etape 5 : Envoi des données dans Bubble

"""
myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'text/plain'
    }
"""

def format_validation(df):
    return True

# Mode : Ignore, Replace sur doublon
def file_handler(full_path: str, format: str, info_diplome: str, mode : str, authorisation : str):

    myHeaders = {
    'Authorization':'Bearer '+authorisation,  
    'Content-type':'text/plain'
    }
    
    if format == "csv":
        df = csv_handler(full_path, authorisation)
    elif format == "xls":
        df = xls_handler(full_path,authorisation)
    else:
        return False  # Todo : return a Format error
    
    data=parser(df, info_diplome)  # Récupère les données cleans à transmettre à Bubble
    print(data.idtechnique_text)
    
    all_certifie=pd.DataFrame(jsonable_encoder(mc.get_certifie("[]",myHeaders)))
    
    if mode == "ignore" : 
        print("entre")
        data=data[~data.idtechnique_text.isin(all_certifie.idtechnique_text)]
        data = json.dumps([row.dropna().to_dict() for index,row in data.iterrows()])
        data= data.replace("[","").replace("]","").replace("}, {","}\n{")

    elif mode=="replace" : 
        print("mode replace")
    else :
        return False # Todo : return a mode error
    
    #Envoi des données dans Bubble
    try : 
        url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/certifie/bulk"
        response = requests.post(url, headers = myHeaders,data=data)
        print(response.text)
    except :
        return False

    return {'response': response.text}

    
def parser(df, info_diplome):
    # Vérificaton du template
    print(df)
    # Mise en forme des données des données pour Bubble
    df=df.fillna(np.nan).replace([np.nan], [None])
    rename={"idTechnique":"idtechnique_text","urlPreuve":"urlpreuve_text","libelleOption":"libelleoption_text","obtentionCertification":"obtentioncertification_text","donneeCertifiee":"donneecertifiee_bool","modalitePassageExamen":"modalitepassageexamen_text","codePostalCentreExamen":"codepostalcentreexamen_text","modaliteAcces":"modaliteacces_text","voieAccessVAE":"voieaccessvae_text","initiativeInscription":"initiativeinscription_text",
            "nomNaissance":"nomnaissance_text","nomUsage":"nomusage_text","prenom1":"prenom1_text","prenom2":"prenom2_text","prenom3":"prenom3_text","anneeNaissance":"anneenaissance_number","moisNaissance":"moisnaissance_text","jourNaissance":"journaissance_text","sexe":"sexe_text","codeInseeNaissance":"codeinseenaissance_text","codePostalNaissance":"codepostalnaissance_text","libelleCommuneNaissance":"libellecommunenaissance_text","codePaysNaissance":"codepaysnaissance_text","libellePaysNaissance":"libellepaysnaissance_text",
            "idDossier":"iddossier_text","nomTitulaire":"nomtitulaire_text","prenom1Titulaire":"prenom1titulaire_text"}
    rename2=["idtechnique_text","urlpreuve_text","libelleoption_text","obtentioncertification_text","donneecertifiee_bool","modalitepassageexamen_text","codepostalcentreexamen_text","modaliteacces_text","voieaccessvae_text","initiativeinscription_text",
            "nomnaissance_text","nomusage_text","prenom1_text","prenom2_text","prenom3_text","anneenaissance_number","moisnaissance_number","journaissance_number","sexe_text","codeinseenaissance_text","codepostalnaissance_text","libellecommunenaissance_text","codepaysnaissance_text","libellepaysnaissance_text",
            "iddossier_text","nomtitulaire_text","prenom1titulaire_text"]

    print(df.rename(index=str,columns=rename,inplace=True))
    print(df)
    # Vérification des données
    print(df.columns)
    
    validate_df=mc.CertifieSchema.validate(df,lazy=True)
    validate_df = validate_df[validate_df["idtechnique_text"].notnull()]

    #retypage des entiers >> à mettre dans le modèle...
    validate_df["anneenaissance_number"]=validate_df["anneenaissance_number"].astype(int)
    return validate_df
    """
    A déplacer
    data = json.dumps([row.dropna().to_dict() for index,row in validate_df.iterrows()])
    return data.replace("[","").replace("]","").replace("}, {","}\n{")
    """

def csv_handler(file_source):
    urlData = requests.get(file_source).content
    rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')),sep=";")
    return rawData

def xls_handler(file_source,authorisation):
    myHeaders = {
    'Authorization':'Bearer '+ authorisation
    }
    urlData = requests.get(file_source, myHeaders).content
    a=io.BytesIO(urlData)
    print(urlData)
    
    return pd.read_excel(a,engine='openpyxl')



#file_handler("https://a0d975d54cad9fa5226f930a81743677.cdn.bubble.io/f1686669491093x526372769085472060/Template_certifie_test.csv", "csv", "info_diplome","","")
#file_handler("https://a0d975d54cad9fa5226f930a81743677.cdn.bubble.io/f1692263531126x190347705585151680/Template_certifie_testxls%20%284%29%20%282%29.xlsx","xls","info_diplome","ignore","1692192096225x126783181523902450")
#file_handler("https://accrochagecertification.bubbleapps.io/version-test/fileupload/f1692264169559x779296096297333200/Template_certifie_testxls%20%284%29%20%282%29.xlsx","xls","info_diplome","ignore","1692261819715x923060793598225000")


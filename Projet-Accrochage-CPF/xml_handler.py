from enum import Enum

from fastapi import FastAPI
import requests
from jinja2 import Environment, FileSystemLoader
import requests
import pandas as pd
import io
import base64
import json
#import model.certifie as mc

import model.certifie as mc
import model.xml_file as xf
import model.couplexml as cx

myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'text/plain'
    }

#Etape 1 récupérer les données depuis Bubble OK
#Etape 2 générer le XML La validation des données se fait depuis une API découplée ! 
#Etape 3 Envoyer le XML sur Bubble


df_header=['_id','Modified Date','Created Date','Created By','idtechnique_text','urlpreuve_text','libelleoption_text','obtentioncertification_text','donneecertifiee_text','datedebutexamen_date','datefinexamen_date','modalitepassageexamen_text','codepostalcentreexamen_text','datedebutvalidite_date','datefinvalidite_date','presenceniveaulangueeuro_text','niveaulangueeuropeen_text','presenceniveaunumeriqueeuro_text','scoring_text','mentionvalidee_text','verbatim_text','modaliteacces_text','voieaccessvae_text','initiativeinscription_text','dateinscription_date','nomnaissance_text','nomusage_text','prenom1_text','prenom2_text','prenom3_text','anneenaissance_number','moisnaissance_number','journaissance_number','sexe_text','codeinsee_text','codepostal_text','libellecommunenaissance_text','codepayspaissance_text','libellepaysnaissance_text','iddossier_text','nomtitulaire_text','prenom1titulaire_text','validation_idtechnique_text','validation_urlpreuve_text','validation_libelleoption_text','validation_obtentioncertification_text','validation_donneecertifiee_text','validation_datedebutexamen_text','validation_datefinexamen_text','validation_modalitepassageexamen_text','validation_codepostalcentreexamen_text','validation_datedebutvalidite_text','validation_datefinvalidite_text','validation_presenceniveaulangueeuro_text','validation_niveaulangueeuropeen_text','validation_presenceniveaunumeriqueeuro_text','validation_scoring_text','validation_mentionvalidee_text','validation_verbatim_text','validation_modaliteacces_text','validation_voieaccessvae_text','validation_initiativeinscription_text','validation_dateinscription_date','validation_nomnaissance_text','validation_nomusage_text','validation_prenom1_text','validation_prenom2_text','validation_prenom3_text','validation_anneeNaissance_text','validation_moisnaissance_text','validation_journaissance_text','validation_sexe_text','validation_codeinsee_text','validation_codepostal_text','validation_libellecommunenaissance_text','validation_codepaysnaissance_text','validation_libellepaysnaissance_text','validation_iddossier_text','validation_nomtitulaire_text','validation_prenom1titulaire_text']

def get_bubble_certifie(constraint : str):
    url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/certifie?constraints=+"+ constraint 
    if constraint == "":
        url = "https://accrochagecertification.bubbleapps.io/version-test/api/1.1/obj/certifie"
    
    #myParams = '{constraints=[ { "key": "idTechnique", "constraint_type": "equals", "value": "TEST-2023-12" }]'
    response = requests.get(url, headers = myHeaders)
    urlData = response.content
    print(response.text)
    rawData = pd.read_json(io.StringIO(urlData.decode('utf-8')),orient='index')
    df=pd.DataFrame(rawData['results']['response'],columns=df_header)
    df = df.where(pd.notnull(df), None)
    print(df['Modified Date'])
    return df




def post_file(filename, bfile):
    
    url = "https://accrochagecertification.bubbleapps.io/version-test/fileupload"
    payload = {
        "name": filename,
        "contents" : bfile
    }
    myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'text/plain'

    }
    response = requests.post(url,data=payload)
    return response



def build_xml(df,idFlux,idEmetteur,idCertificateur,idContrat):    
    # Iterate over each group and create a nested dictionary
    #df['group_column'] = df['idFlux'] + df['horodatage'] + df['idEmetteur'] + df['idCertificateur'] + df['idContrat'] + df['certificationType'] + df['certificationCode'] + df['natureDeposant']
    df.fillna("", inplace=True)
    grouped = df.groupby('idtechnique_text')

    for group_name, group_df in grouped:
        print(group_name[0] + "group_name")
        nested_dict = {'idFlux': str(idFlux),
                   'horodatage': "",
                   'idEmetteur': idEmetteur,
                   'idCertificateur': idCertificateur,
                   'idContrat': idContrat,
                   'certificationType': "",
                   'certificationCode': "",
                   'natureDeposant': "",
                   'certifies': []}
        for index, row in group_df.iterrows():
            if(type(row['nomnaissance_text']) is not str or row['nomnaissance_text'] == "" ):
                nested_dict['certifies'].append({'idTechnique': str(row['idtechnique_text']),
                                         'urlPreuve': str(row['urlpreuve_text']),
                                         'libelleOption': row['libelleoption_text'],
                                         'obtentionCertification': row['obtentioncertification_text'],
                                         'donneeCertifiee': row['donneecertifiee_text'],
                                         'dateDebutExamen': row['datedebutexamen_date'],
                                         'dateFinExamen': row['datefinexamen_date'],
                                         'modalitePassageExamen': row['modalitepassageexamen_text'],
                                         'codePostalCentreExamen': str(row['codepostalcentreexamen_text']),
                                         'dateDebutValidite': str(row['datedebutvalidite_date']),
                                         'dateFinValidite': row['datefinvalidite_date'],
                                         'presenceNiveauLangueEuro': row['presenceniveaulangueeuro_text'],
                                         'niveauLangueEuropeen': row['niveaulangueeuropeen_text'],
                                         'presenceNiveauNumeriqueEuro': row['presenceniveaunumeriqueeuro_text'],
                                         'scoreGeneral': "",
                                         'niveau': "",
                                         'domaineCompetenceId': "",
                                         'competenceId': "",
                                         'scoring': row['scoring_text'],
                                         'mentionValidee': row['mentionvalidee_text'],
                                         'verbatim': row['verbatim_text'],
                                         'modaliteAcces': row['modaliteacces_text'],
                                         'voieAccessVAE': row['voieaccessvae_text'],
                                         'initiativeInscription': row['initiativeinscription_text'],
                                         'dateInscription': row['dateinscription_date'],
                                        'dossierFormation': {'idDossier': str(int(row['iddossier_text'])),
                                                              'nomTitulaire': row['nomtitulaire_text'],
                                                              'prenom1Titulaire': row['prenom1titulaire_text']}})
            else :
                nested_dict['certifies'].append({'idTechnique': row['idtechnique_text'],
                                         'urlPreuve': row['urlpreuve_text'],
                                         'libelleOption': row['libelleoption_text'],
                                         'obtentionCertification': row['obtentioncertification_text'],
                                         'donneeCertifiee': row['donneecertifiee_text'],
                                         'dateDebutExamen': row['datedebutexamen_date'],
                                         'dateFinExamen': row['datefinexamen_date'],
                                         'modalitePassageExamen': row['modalitepassageexamen_text'],
                                         'codePostalCentreExamen': str(row['codepostalcentreexamen_text']),
                                         'dateDebutValidite': str(row['datedebutvalidite_date']),
                                         'dateFinValidite': row['datefinvalidite_date'],
                                         'presenceNiveauLangueEuro': row['presenceniveaulangueeuro_text'],
                                         'niveauLangueEuropeen': row['niveaulangueeuropeen_text'],
                                         'presenceNiveauNumeriqueEuro': row['presenceniveaunumeriqueeuro_text'],
                                         'scoreGeneral': "",
                                         'niveau': "",
                                         'domaineCompetenceId': "",
                                         'competenceId': "",
                                         'scoring': row['scoring_text'],
                                         'mentionValidee': row['mentionvalidee_text'],
                                         'verbatim': row['verbatim_text'],
                                         'modaliteAcces': row['modaliteacces_text'],
                                         'voieAccessVAE': row['voieaccessvae_text'],
                                         'initiativeInscription': row['initiativeinscription_text'],
                                         'dateInscription': row['dateinscription_date'],
                                         'titulaire': {'nomNaissance': row['nomnaissance_text'],
                                                       'nomUsage': row['nomusage_text'],
                                                       'prenom1': row['prenom1_text'],
                                                       'prenom2': row['prenom2_text'],
                                                        'prenom3': row['prenom3_text'],
                                                        'anneeNaissance': int(row['anneenaissance_number']),
                                                        'moisNaissance': int(row['moisnaissance_number']),
                                                        'jourNaissance': int(row['journaissance_number']),
                                                        'codeInseeNaissance': str(row['codeinsee_text']),
                                                        'codePostalNaissance': str(row['codepostal_text']),
                                                        'codePaysNaissance': row['codepayspaissance_text'],
                                                        'libellePaysNaissance': row['libellepaysnaissance_text'],
                                                        'libelleCommuneNaissance': row['libellecommunenaissance_text'],
                                                        'sexe': row['sexe_text']}})
        print(nested_dict)
    environment = Environment(loader=FileSystemLoader("template/"))    
    template = environment.get_template("source_template_V1.xml")
    datas = [nested_dict]
    print(datas)
    directory = str(idFlux)+"_folder"
    

    for data in datas:
        filename = str(idFlux)+".xml"
        content = template.render(
            data,
            max_score=100,
            test_name="test_name"
    )
    print(content)
    return post_file(filename,base64.b64encode(bytes(content, 'utf-8')))








def generate_xml(constraint : str,idFlux : str, idEmetteur : str,idCertificateur :str, idContrat: str, authorisation : str):
    #1. Récupérer les données   
    df=get_bubble_certifie(constraint)
    print(df.columns)

    #2. Générer le XML et envoi sur Bubble
    dfile={}
    XML=build_xml(df,idFlux,idEmetteur,idCertificateur,idContrat)
    #3. Création d'un XML FILE et d'un couple XML sur Bubble 
    xmlFile=xf.xml_file(name_text=str(idFlux)+".xml",file_url_text=XML.text.replace('"',''),id_flux_text=idFlux,type_de_fichier_option_file_type="Source")
    statut_xml_file=xf.post_xml_file(xmlFile,myHeaders)
    data_xml_file=json.loads(statut_xml_file.text)
    couple_xml=cx.couple_xml(fichier_source_custom_file_uploaded=data_xml_file['id'],id_flux1_text=idFlux,statut_du_traitement_option_statut_fichier="Nouveau")
    statut_couple_xml=cx.post_couple_xml(couple_xml,myHeaders)
    return statut_couple_xml.content

"""
constraint = "[ { \"key\": \"idTechnique\", \"constraint_type\": \"equals\", \"value\": \"TEST-2023-12\" }]"
generate_xml(constraint,"azzaezez01fe3","azzaezez0fe2","azzaezfeez03","azzaezfeez04","")
"""
#post_xml()




# Import the required modules
import xmltodict
import pprint
import pandas as pd
import requests
import io
import model.couplexml as cx
import model.lien_file_certifie as lfc
import model.xml_file as xf
import model.certifie as mc
from fastapi.encoders import jsonable_encoder



myHeaders = {
    'Authorization':'Bearer 0112034227b4c84ccab69fa6b7b777e1',  
    'Content-type':'application/json',
    'accept': 'application/json'
    }



"""dict example [OrderedDict([ ('@xmlns:ns2', 'urn:cdc:cpf:pc5:rapport:schema'),
                              ( 'nomFichier',
                                'lnf00000-0000-0000-0000-000000000008.xml'),
                              ( 'idFlux',
                                'lnf00000-0000-0000-0000-000000000008'),
                              ('idTraitement', '51354'),
                              ( 'PassagesKO',
                                OrderedDict([ ( 'passage',
                                                [ OrderedDict([ ( 'idTechnique',
                                                                  '202006-2510'),
                                                                ( 'messageErreur',
                                                                  'Aucun '
                                                                  'titulaire '
                                                                  'ne '
                                                                  'correspond '
                                                                  'aux '
                                                                  'critères '
                                                                  'obligatoires')]),
                                                  OrderedDict([ ( 'idTechnique',
                                                                  '202006-294'),
                                                                ( 'messageErreur',
                                                                  'Aucun '
                                                                  'titulaire '
                                                                  'ne '
                                                                  'correspond '
                                                                  'aux '
                                                                  'critères '
                                                                  'obligatoires')]),
                                                  OrderedDict([ ( 'idTechnique',
                                                                  '202006-5759'),
                                                                ( 'messageErreur',
                                                                  'Aucun '
                                                                  'titulaire '
                                                                  'ne '
                                                                  'correspond '
                                                                  'aux '
                                                                  'critères '
                                                                  'obligatoires')]),
                                                  OrderedDict([ ( 'idTechnique',
                                                                  '202006-5966'),
                                                                ( 'messageErreur',
                                                                  'Aucun '
                                                                  'titulaire '
                                                                  'ne '
                                                                  'correspond '
                                                                  'aux '
                                                                  'critères '
                                                                  'obligatoires')]),
                                                  OrderedDict([ ( 'idTechnique',
                                                                  '202104-10523'),
                                                                ( 'messageErreur',
                                                                  'Plusieurs '
                                                                  'titulaires '
                                                                  'ont été '
                                                                  'identifiés')]),
                                                  OrderedDict([ ( 'idTechnique',
                                                                  '202006-234'),
                                                                ( 'messageErreur',
                                                                  'Aucun '
                                                                  'titulaire '
                                                                  'ne '
                                                                  'correspond '
                                                                  'aux '
                                                                  'critères '
                                                                  'obligatoires')]),
                                                  OrderedDict([ ( 'idTechnique',
                                                                  'LNF_Accrochage_349'),
                                                                ( 'messageErreur',
                                                                  'Aucun '
                                                                  'titulaire '
                                                                  'ne '
                                                                  'correspond '
                                                                  'aux '
                                                                  'critères '
                                                                  'obligatoires')])])])),
                              ( 'PassagesOK',
                                OrderedDict([ ( 'idTechnique',
                                                [ '202006-2094',
                                                  '202006-2187',
                                                  '202006-2535',
                                                  '202006-2823',
                                                  '202006-3224',
                                                  '202006-5257',
                                                  '202010-7255',
                                                  '202011-8259',
                                                  '202101-9185',
                                                  '202102-9524',
                                                  'LNF_Accrochage_21',
                                                  'LNF_Accrochage_347',
                                                  'LNF_Accrochage_619',
                                                  'LNF_Accrochage_635',
                                                  'LNF_Accrochage_656',
                                                  'LNF_Accrochage_657',
                                                  'LNF_Accrochage_668'])]))]))])

"""

# Différentes étapes de traitement de l'accusé de traitement
# 1. Récupération de l'objet file_xml
# 2. Récupération de l'idFlux et mise à jour du fichier source
# 3. Remplir lien File Certifie




def handler_accuse_de_traitement(xml_file : xf.xml_file):
    """
    Fonction qui permet de gérer l'accusé de traitement
    """
    # Récupération du fichier xml
    url=xml_file.file_url_text
    try :
        urlData = requests.get(url).content
        my_dict = xmltodict.parse(urlData)
        pprint.pprint(my_dict, indent=2) 
        # TO DO : Créer et envoyer un objet file_xml
        xml_file=xf.xml_file(name_text = my_dict['rapport']['nomFichier'],file_url_text=url,id_flux_text=my_dict['rapport']['idFlux'],nb_passage_ko_number=len(my_dict['rapport']['PassagesKO']['passage']),nb_passage_ok_number=len(my_dict['rapport']['PassagesOK']['idTechnique']),type_de_fichier_option_file_type="Accusé de traitement",id_traitement_text=my_dict['rapport']['idTraitement'])
        xf.post_xml_file(xml_file,myHeaders)
    except :
        print("Le fichier déposé n'est pas un accusé de traitement") 
        # Todo : return a Format error
        return False
    # TO DO : Rechercher le couple xml associé
    couple_xml=cx.get_couple_xml("[ { \"key\": \"id_flux\", \"constraint_type\": \"equals\", \"value\": \""+xml_file.id_flux_text+"\" }]",myHeaders)[0]
    # Nb passage Ko/OK id accusé de traitement, id Traitement, statut du traitement /// attention longueur de la liste
    couple_xml.nb_passage_ko_number=xml_file.nb_passage_ko_number
    couple_xml.nb_passage_ok_number=xml_file.nb_passage_ok_number
    couple_xml.id_traitement_text=xml_file.id_traitement_text
    
    if xml_file.nb_passage_ko_number > 0 :
        couple_xml.statut_du_traitement_option_statut_fichier="Traité avec erreurs"
    else :
      couple_xml.statut_du_traitement_option_statut_fichier="Entièrement validé"
    cx.put_couple_xml(couple_xml,myHeaders)
    # TO DO : Génération des lien file certifie >> récupérer tous les ID bubble grâce aux idTechnique
    print(mc.get_certifie("[]",myHeaders))
    all_certifie=pd.DataFrame(jsonable_encoder(mc.get_certifie("[]",myHeaders,True)))
    print(all_certifie)
    list_lien_file_certifie=[]
    for idTechnique in my_dict['rapport']['PassagesOK']['idTechnique'] :
      id_certifie=all_certifie[all_certifie.idtechnique_text==idTechnique]['_id']
      if (len(id_certifie)==0):
        id_certifie=None
      else :
        id_certifie=id_certifie[0]
      lien_file_certifie=lfc.lien_file_certifie(etatpassage_boolean=True,idflux_text=str(my_dict['rapport']['idFlux']),idtechnique_text=str(idTechnique),lien_certifie_custom_items=str(id_certifie),lien_file_custom_file_uploaded=str(couple_xml.id))
      list_lien_file_certifie.append(lien_file_certifie)
    for idTechnique in my_dict['rapport']['PassagesKO']['passage'] :
      print("entre")
      id_certifie=all_certifie[all_certifie.idtechnique_text==idTechnique['idTechnique']]['_id']
      print(id_certifie)
      if (len(id_certifie)==0):
        id_certifie=None
      else :
        id_certifie=id_certifie.iloc[0]
      lien_file_certifie=lfc.lien_file_certifie(etatpassage_boolean=False,idflux_text=str(my_dict['rapport']['idFlux']),idtechnique_text=str(idTechnique['idTechnique']),lien_certifie_custom_items=str(id_certifie),lien_file_custom_file_uploaded=str(couple_xml.id),messageerreur_passage_text=str(idTechnique['messageErreur']))
      list_lien_file_certifie.append(lien_file_certifie)
    lfc.put_lien_file_certifie_bulk(list_lien_file_certifie,myHeaders)
    
    # récupération et mise à jour du fichier  traitement

     # résume la fonction  
    
    
    #xf.get_xml_file("[ { \"key\": \"id_flux\", \"constraint_type\": \"equals\", \"value\": \""+my_dict['rapport']['idFlux']   +"\" }]",myHeaders)
    



""" 

        """
#Zone de test

#handler_accuse_de_traitement("https://a0d975d54cad9fa5226f930a81743677.cdn.bubble.io/f1689839656328x879846952703531300/Accus%C3%A9%20de%20traitement_lnf00000-0000-0000-0000-000000000004.xml_20230427.xml")
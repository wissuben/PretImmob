from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
from fastapi import FastAPI, HTTPException, Depends, status
import requests

import uvicorn
from propertyEvaluationService import InspectionInfo, LegalCompliance
from db_services.demande_pret import select_demande_pret_by_id, update_scoring_by_id, update_solvency_by_id, \
    update_property_valuation_by_id, update_decision_by_id
from db_services.client_history import select_client_history_by_id

import asyncio

response4 = None

api_Extraction_url = "http://localhost:8009/read_file"
api_EvalPropriete_url = "http://localhost:8008/EvaluateProperty"
api_CalculScore_url = "http://localhost:8003/calculate_credit_score"
api_VerifSolva_url = "http://localhost:8002/verify_solvency"
api_DecisionApprob_url = "http://localhost:8005/decision"

# Specify the directory to watch
incoming_files_directory = '../incoming_files'

token_secret_Extraction = "fdfdfdfdfdgrghth"
token_secret_EvalProp = "AHshhsdfghjklkjhgfdsdfghjkvrepdazdede"
token_secret_CalculScore = "AHshhwdfdsfgxhczcrfkrfdgsgvfkfnvrepdazde"
token_secret_VerifSolva = "AHshhxhczcrfkrfdgsgvfkfnvrepdazdede"
token_secret_DecisionApprob = "AHshhxhczxdfghjkjhgfdfghjkhgf"

headers = {
    'Content-Type': 'application/json',
}


def remplacer_variables(html_template, variables):
    for variable, valeur in variables.items():
        html_template = html_template.replace('{{' + variable + '}}', valeur)
    return html_template


def lire_template(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        contenu = fichier.read()
    return contenu


def ecrire_dans_fichier(nom_fichier, contenu):
    with open(nom_fichier, 'w') as fichier:
        fichier.write(contenu)
    print("Wrote file")


class FileHandler(FileSystemEventHandler):
    def __init__(self):
        self.processed_files = {}  # Now it's a dictionary
        self.current_id = 0

    def on_created(self, event):
        if event.is_directory:
            return

        file_name = event.src_path
        # Check if the file should be ignored
        if file_name.endswith("-checkpoint.txt"):
            return  # Ignore files starting with a dot or ending with "_checkpoint.txt"

        # Check if the file has already been processed
        if file_name not in self.processed_files:

            self.processed_files[file_name] = True
            self.current_id += 1
            print(f"New file created: {file_name}")

            try:
                headers['Authorization'] = f"Bearer {token_secret_Extraction}"
                response = requests.post(api_Extraction_url, params={'file_name': file_name}, headers=headers).json()
            except:
                print("Erreur INVALID Token !")
                return

            response = select_demande_pret_by_id(response['id_demande_pret'])
            print(response)

            client_id = response["id_client"]

            client_data = select_client_history_by_id(client_id)

            response_solvency_verification = ""
            general_info = ""

            if client_data:
                # Process the file using the corresponding data
                monthly_expenses = float(response["depenses_mensuelles"].replace('€', ''))
                monthly_income = float(response["revenu_mensuel"].replace('€', ''))
                loan_amount = float(response["montant_pret_demande"].replace('€', ''))

                try:
                    headers['Authorization'] = f"Bearer {token_secret_CalculScore}"
                    response_scoring = requests.post(api_CalculScore_url, params={'debts': int(client_data['debts']),
                                                                                  'late_payments': int(
                                                                                      client_data['late_payments']),
                                                                                  'bankruptcy': int(
                                                                                      client_data['bankruptcy'])},
                                                     headers=headers).json()
                except:
                    print("Erreur INVALID Token for scoring_service!")
                    return

                print(response_scoring)
                general_info += f"<p>Scoring: {response_scoring}</p>"

                update_scoring_by_id(response["id_demande_pret"], response_scoring)

                try:
                    headers['Authorization'] = f"Bearer {token_secret_VerifSolva}"
                    response_solvency_verification = requests.post(api_VerifSolva_url,
                                                                   params={'credit_score': float(response_scoring),
                                                                           'monthly_expenses': float(monthly_expenses),
                                                                           'loan_amount': float(loan_amount),
                                                                           'monthly_income': float(monthly_income)},
                                                                   headers=headers).json()
                except:
                    print("Erreur INVALID Token for solvency_service!")
                    return

                print(response_solvency_verification)
                general_info += f"<p>Solvabilité: {response_solvency_verification}</p>"
                update_solvency_by_id(response["id_demande_pret"], response_solvency_verification)

            else:
                print(f"Données manquantes pour le client ID : {client_id}")
                general_info += f"<p>Erreur: Données manquantes pour le client ID : {client_id}</p>"

            # third Service
            property_description = str(response["description_de_propriete"])

            RecentSalesData = 'Données du marché immobilier récentes ici'

            inspectionInfo = InspectionInfo(True, False)

            legal_compliance = LegalCompliance(False, True, True)

            try:
                headers['Authorization'] = f"Bearer {token_secret_EvalProp}"
                response3 = requests.post(api_EvalPropriete_url, params={'property_description': property_description,
                                                                         'RecentSalesData': RecentSalesData,
                                                                         'inspectionInfo': inspectionInfo,
                                                                         'legal_compliance': legal_compliance},
                                          headers=headers).json()

            except:
                print("Erreur INVALID Token for evalProperty service!")
                return

            print(f"Résultat de l'évaluation : {response3['PropertyValuation']}")
            update_property_valuation_by_id(response["id_demande_pret"], response3['PropertyValuation'])

            print(f"Résultat de l'inspection : {response3['InspectionResult']}")
            print(f"Résultat de la conformité : {response3['ComplianceResult']}")

            general_info += f"<p>Évaluation: {response3['PropertyValuation']}</p>"
            general_info += f"<p>Inspection: {response3['InspectionResult']}</p>"
            general_info += f"<p>Conformité: {response3['ComplianceResult']}</p>"

            # Add the file name to the dictionary of processed files
            try:
                headers['Authorization'] = f"Bearer {token_secret_DecisionApprob}"
                response4 = requests.post(api_DecisionApprob_url,
                                          params={'InspectionResult': response3['InspectionResult'],
                                                  'ComplianceResult': response3['ComplianceResult'],
                                                  'solvabilité': response_solvency_verification},
                                          headers=headers).json()


            except:
                print("Erreur INVALID Token for evalProperty service!")
                return

            print(response4)
            template_html = lire_template('../interface/notif.html')

            variables = {
                'decision': response4,
                'info': general_info
            }

            html_final = remplacer_variables(template_html, variables)

            ecrire_dans_fichier("../output/result.html", html_final)

            update_decision_by_id(response["id_demande_pret"], response4)


def watch_directory(directory_path):
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_path, recursive=True)  # Monitor subdirectories as well
    observer.start()
    print(f"Watching directory: {directory_path}")

    try:
        while True:
            pass

    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    # Ensure the directory exists, create it if not
    if not os.path.exists(incoming_files_directory):
        os.makedirs(incoming_files_directory)
    watch_directory(incoming_files_directory)

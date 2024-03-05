from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
from fastapi import FastAPI, HTTPException, Depends, status
import requests
from propertyEvaluationService import InspectionInfo, LegalCompliance


api_Extraction_url = "http://localhost:8001/read_file"
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
            response["id"] = self.current_id
            file_id = response["id"]

            # Load the JSON data
            with open('client_data.json', 'r') as file:
                clients_data = json.load(file)

            # Find the data corresponding to the `id` from the file
            client_data = next((client for client in clients_data if client['id'] == file_id), None)
            response_solvency_verification = ""
            if client_data:
                # Process the file using the corresponding data
                monthly_expenses = float(response["Depenses_Mensuelles"].replace('€', ''))
                monthly_income = float(response["Revenu_mensuel"].replace('€', ''))
                loan_amount = float(response["Montant_du_Pret_Demande"].replace('€', ''))

                # request = client_scoring.factory.create('CreditScoreRequest')
#                request.debts = client_data['debts']
 #               request.late_payments = client_data['late_payments']
  #              request.bankruptcy = client_data['bankruptcy']
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
                              # response_scoring = client_scoring.service.calculate_credit_score(request)
                print(response_scoring)

                '''response_solvency_verification = client_solvency_verification.service.verify_solvency(credit_score,
                                                                                                      monthly_expenses,
                                                                                                      loan_amount,
                                                                                                      monthly_income)'''
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

                #response2 = str(response_solvency_verification)
                print(f"Client ID: {file_id}, JSON:{response['id']}, Résultat: {response_solvency_verification}")

            else:
                print(f"Données JSON manquantes pour le client ID : {file_id}")

            # third Service
            property_description = str(response["description_de_propriete"])

          #  property_info = clientService3.factory.create('PropertyDescription')
           # property_info.Description = property_description

          #  market_data = clientService3.factory.create('MarketData')
            RecentSalesData = 'Données du marché immobilier récentes ici'

          #  inspection_info = clientService3.factory.create('InspectionInfo')
          #  inspection_info.InspectionVirtuelle = True  # True ou False en fonction de l'inspection
            inspectionInfo = InspectionInfo(True, False)
          #  inspection_info.InspectionSurPlace = False  # True ou False en fonction de l'inspection

           # legal_compliance = clientService3.factory.create('LegalCompliance')
           # legal_compliance.LitigesFonciersEnCours = False  # True ou False en fonction des litiges fonciers
         #   legal_compliance.ConformiteReglementsBatiment = True  # True ou False en fonction de la conformité
          #  legal_compliance.EligibilitePretImmobilier = True  # True ou False en fonction de l'éligibilité
            legal_compliance = LegalCompliance(False, True, True)

            # Call the SOAP service to process the new file and pass the property description
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
            print(f"Résultat de l'inspection : {response3['InspectionResult']}")
            print(f"Résultat de la conformité : {response3['ComplianceResult']}")

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

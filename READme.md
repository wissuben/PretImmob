#FastAPI Project
Service Web Composite d'Évaluation de Demande de Prêt Immobilier

1. Contexte du Projet

Le Service Web Composite d'Évaluation de Demande de Prêt Immobilier est conçu pour automatiser l’évaluation des demandes de prêt immobilier en orchestrant plusieurs services spécialisés. Le système permet aux clients de soumettre leurs demandes de prêt de manière simple et naturelle, tout en intégrant des processus clés tels que la vérification de solvabilité, l’évaluation de la propriété, et la prise de décision d’approbation.

2. Objectifs

Simplifier et automatiser le processus de demande de prêt immobilier.
Offrir une interface centralisée permettant aux clients de soumettre leurs demandes.
Coordonner les divers services Web requis pour évaluer les demandes.
Assurer une expérience fluide pour les clients et un traitement efficace pour les institutions financières.
3. Fonctionnalités Principales

3.1 Réception de la Demande
Acceptation des demandes de prêt immobilier exprimées en langage naturel, incluant les informations sur le client et la propriété.
3.2 Extraction d'Informations Métier
Analyse des demandes pour extraire les informations cruciales (nom, adresse, montant du prêt, etc.) à l'aide de techniques de traitement automatique du langage naturel (NLP).
3.3 Vérification de Solvabilité
Vérification de la solvabilité du client en examinant les données financières et de crédit du client via des bureaux de crédit.
3.4 Évaluation de la Propriété
Estimation de la valeur de la propriété en fonction des données du marché et des inspections virtuelles.
3.5 Décision d'Approbation
Prise de décision d'approbation ou de refus du prêt basée sur l'analyse des risques et les politiques de l'institution financière.
4. Architecture du Système

Le système est construit autour de plusieurs services Web orchestrés :

Service d’Extraction d’Informations Métier : Analyse des données soumises et extraction des informations pertinentes.
Service de Vérification de Solvabilité : Vérification de la capacité financière du client.
Service d’Évaluation de la Propriété : Estimation de la valeur de la propriété.
Service de Décision d’Approbation : Analyse des risques et prise de décision.
5. Phases de Développement

Phase 1 : Réalisation avec l’API SOAP
Mise en place initiale de l'architecture et des services en utilisant le protocole SOAP.
Phase 2 : Migration vers REST
Conversion des services vers une architecture basée sur l'API REST pour plus de flexibilité et compatibilité.
6. Technologies Utilisées

Python : Langage de programmation pour les services backend.
Flask / FastAPI : Frameworks utilisés pour le développement des services.
SOAP & REST : Protocoles utilisés pour les communications entre services.
NLP (Natural Language Processing) : Utilisé pour l'extraction d'informations métier.
Bases de données : Stockage des informations client et des demandes de prêt (ex. PostgreSQL).

# Launch all the services of API and go to the URL (http://localhost:8000) of UserCredentials service
# Use as login : 16, and password : wissuwissu
# Choose a file from incoming_files package (approved_demand to test approval for exemple) and click on upload
# Wait for results



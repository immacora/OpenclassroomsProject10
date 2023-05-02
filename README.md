# OpenclassroomsProject10
Créez une API sécurisée RESTful en utilisant Django Rest Framework

L'interface de programme d'application intègre les points de terminaison documentés sur Postman pour standardiser le traitement des données d'une application de gestion des services d'assistance sur trois plateformes (site web, applications Android et iOS).

L'authentification requise des utilisateurs de l'application, et l'appartenance des enregistrements pour modification et suppression des projets/problèmes/commentaires, implique le respect des mesures de sécurité OWASP suivies dans ce projet.

## Prérequis :
  - python 3.11.2
  - pip

## Installation (Windows 11)

  - Dans le répertoire souhaité, clonez le projet : git clone https://github.com/immacora/OpenclassroomsProject10.git
  - Dirigez-vous dans le répertoire créé : cd OpenclassroomsProject10
  - Créez l’environnement virtuel du projet : py -m venv venv
  - Activez l’environnement virtuel : venv\Scripts\activate
  - Installez les modules requis : pip install -r requirements.txt

Pour générer un rapport flake8, saisir : flake8 --format=html --htmldir=flake-report

## Documentation Postman

https://documenter.getpostman.com/view/24942161/2s93eSZFPN
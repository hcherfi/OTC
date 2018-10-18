# Barre de recherche intelligente
Description macroscopique du code de l’application

## Contents
1. [Barre de recherche intelligente](#barre-de-recherche-intelligente)
2. [Description macroscopique du code de l’application](#desciption-macroscopique-du-code-de-l-application)
  1. [Introduction](#introduction)
  2. [Service endpoint](#service-endpoint)
  3. [Error handling](#error-handling)
  4. [Search Bar query handling](#search-bar-query-handling)
    1. [Merge Ontologies](#merge-ontologies)
    2. [Add Concept](#add-concept)
    3. [Delete Concept](#delete-concept)
    4. [Update a query](#update-a-query)
    5. [Delete a query](#delete-a-query)
  5. [Déploiement en local](#deploiement-en-local)
  6. [Description du contenu du git](#description-du-contenu-du-git)
  7. [Base MongoDB](#base-mongodb)

<a name="introduction"></a>
### Introduction

Cette documentation technique est une description macroscopique de l’application de barre de recherche intelligent (ci-après appelée Search Bar).

Ce document a pour objectif de faciliter la reprise du code de la barre te recherche intelligente par une autre équipe de l’asset. Une description des modules développés ainsi que le flux de données y sont décrits.


Ensuite, la prise en main par le développeur et pour les tests des actions et appels « routes » de l’application sont décrits avec les paramètres entrants et sortants associés et des exemples d’utilisation donnés pour chaque appel/action possibles.

Cette documentation se termine par la description des données de la base de données à interroger ; ainsi qu’un descriptif des ressources sémantiques servant à l’aide à la recherche : requête intelligente.

!!! Description des données
-PIMs
-Ontologie
-Dictionnaires

!!! Dans settings parler des credentials

<a name="service-endpoint"></a>
### Service endpoint

When deployed on the Cloud, the Search Bar service endpoint is based on the location of the service instance. For example, when Search Bar is hosted in France, the base URL is https://gateway-fra.watsonplatform.net. The URL might also be different when you use IBM Cloud Dedicated
To find out which URL to use, view the service credentials by clicking the service instance. Use that URL in your requests to Search Bar.
Service endpoints should follow this pattern: [https://{Service URL}](https://<service-url>)
When deployed an example of API endpoint would look like this :

https://gateway.watsonplatform.net/discovery/api

<a name="error-handling"></a>
### Error handling

The Search Bar service uses standard HTTP response codes to indicate whether a method completed successfully. A 200 response always indicates success. A 400 type response is some sort of failure, and a 500 type response usually indicates an internal system error.  Response codes are listed with the method.

| Parameter         | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| Code <br> _integer_ | The HTTP error status code (200, 500, etc.).                     |
| Error <br> _string_ | Brief message describing the error type (success, failure, etc.) |

<a name="search-bar-query-handling"></a>
### Search Bar query handling

In order to handle queries to database, this section explains the routes and descriptions of parameters and response models.

<a name="merge-ontologies"></a>
#### Merge ontologies

Merges two graphs (i.e., knowledge bases) into one graph avoiding to duplicate concepts, properties, or instances if they have the same URI.
##### REQUEST
 >POST /ontologies

| Parameter |	Description |
| --- | --- |
| ontologies <br> _string[2]_ <br> _required_ | Ontologies to be merged. |

##### RESPONSE
###### MergeOntologiesResponse

A Knowledge base resulting of the fusion of the two KBs.


| Parameter	| Description |
| --- | --- |
| status <br> _string_ | Ontologies are merged in file _file\_fusion.owl_|

##### RESPONSE CODES

Status	| Description
--- | ---
201	| Query executed successfully.
400	| Bad request.

##### Example Request

```bash
curl -X POST \
  http://localhost:3000/ontologies \
  -H 'Content-Type: application/json' \
  -d '{
	"ontologies": ["MediaComp", "MediaClient"]
}'
```

##### Example Response
```json
{
    "status": "MediaComp and MediaClient are merged in file ./OWL/MediaComp_MediaClient_fusion.owl"
}
```

 <a name="add-concept"></a>
#### Add Concept

Adds a concept (owl:Class) to the ontology given the parent concept
> PUT /concepts/<ontology>

##### REQUEST

| Parameter |	Description |
| --- | --- |
| concept <br> _string_ <br> _required_ | Concept to be added. Give the full URI |
| parent <br> _string_ <br> _required_ | Parent Concept. Give prefix or full URI |

##### RESPONSE

###### AddConceptResponse
Parameter	| Description
--- | ---
status <br> _string_	| Created new concept.

##### Example Request
```bash
curl -X PUT \
  http://localhost:3000/concepts/MediaClient \
  -H 'Content-Type: application/json' \
  -d '{
	"concept": "http://purl.org/dc/terms/NewClass",
	"parent": "terms.Agent"
}'
```

##### Example Response
Example JSON body

```json
{
    "status": "Created new concept"
}
```

 <a name="delete-concept"></a>
#### Delete Concept

> DELETE /concepts/<ontology>


##### REQUEST

###### Queries
Parameter |	Description
--- | ---
concept <br> _string_ <br> _required_ | Concept to be deleted. Give prefix 

##### RESPONSE
No response is returned

##### Example Request
```bash
curl -X DELETE \
  http://localhost:3000/concepts/MediaClient \
  -H 'Content-Type: application/json' \
  -d '{
	"concept": "terms.ClassToDelete"
}'
```

##### RESPONSE CODES

Status	| Description
--- | ---
204	| Query executed successfully.
500	| Bad request.


Le code est architecturé en mode Model-View-Control (MVC) sous forme d’un seul micro-service, développé en Python 2.


Le contrôleur du micro-service exécute de façon synchrone les unités de traitement en mono-thread (pas en mutli-thread).

Les services instanciés doivent être liés directement dans IBM Cloud Services.
Comme le montre la Figure 1, le serveur web Flask se connecte à une base de données MongoDB et à une instance Discovery.


![Figure 1: Architecture du code de la Search bar](architecture.png)

Le serveur Flask est généré depuis le boiler plate cloud foundry (IBM Cloud). Il propose par défaut un front-end swagger (non utilisé faute de temps). Son code se trouve dans `public/swagger`
Les dépendances sont consignées dans les fichiers `server/services/application.py`, ainsi que `bar/controllers.py`.
Lors de l'installation via ```bluemix dev build``` ou ```bluemix dev run``` (voir le fichier `README`), le `DockerFile` fait appel à `requirements.txt` pour installer les modules.

### Déploiement en local

Pour un déploiement en localhost utile à la reprise par une autre équipe de développement (sans faire apple à Docker), il faut installer le modèle en langage en français de spacy avec la commande :

```bash
python -m spacy download fr
```

### Description du contenu du git

Le code du micro-service est sous le dossier : bar (cf. Figure 2). Les paramètres de configuration de l’application sont spécifiés sous : server/settings.py

Nous décrivons ci-dessous le contenu des différents répertoires du github de l’application Searchbar.


Directory / File | Descrption
--- | ---
bar	 | code MVC du micro-service
chart	| généré automatiquement par boiler plate
datasets	| Ensemble de ressources pour la construction des variations du chatbot et pour l’entraînement de spacy
notebooks	| tous les prétraitements et post-taitements des données. Ces programmes ne font pas partie de la search bar à proprement dite.
public	| front swagger
python	| environnement virtuel
server/settings.py	| spécifie les credentials de MongoDB et de Discovery (URL, nom d’hôte, mot de passe…)
server/application.py	| instancie le serveur
Dockerfile	| contient le code qui permet de générer l’image de  l’application (image est ce qui sera par déployée sur cloud)
Dockerfile-tools	| contient le code qui permet de générer l’image depuis l’interface CLI de bluemix
requirements	| contient la liste des packages nécessaires au fonctionnement de l’application
run-dev	| script de lancement du serveur
[Figure 2 : Organisation du code dans GitHub de la Search bar](#organisation-code-git)

Les autres répertoires et fichiers sont générés automatiquement par boiler plate.

**NB :** afin d’intégrer les relations et les invoquer par le moteur de requête Discovery par la méthode POST, ajouter une ligne relations dans bar/controllers.py et adapter la ligne results pour une requête générique car aujourd’hui le filtre est en dur :Person, or il doit lire les valeurs des variables entities et relations de cette même méthode POST.

### Base MongoDB

La base MongoDB contient : 

* Collection originale (raw data d’Open Food Facts)
* Collection épurée et traduite en français (cleansed products fr)
* Query (retour du serveur Flask) : Nous avons utilisé une seule base MangoDB et plusieurs collections afin de mutualiser les ressources.

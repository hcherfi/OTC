# Documentation to install/run Ontology Test Challenge (OTC)
This documentation is about REST API and Code description of the Ontology Test Challenge done by **_Hacene Cherfi_**.

## Contents
1. [Introduction](#introduction)
2. [Installation insctructions](#installation-instructions)
3. [Service endpoint description](#service-endpoint-description)
4. [Error handling](#error-handling)
5. [Query endpoint action list](#query-endpoint-action-list)
  1. [Merge Ontologies](#merge-ontologies)
  2. [Add Concept](#add-concept)
  3. [Delete Concept](#delete-concept)


<a name="introduction"></a>
## Introduction

The OTC application is based-on the Model-View-Control (MVC) paradigm and web service technology.  
There is no View part. Controllers are the actions to perform (add/delete/merge) on concepts of ontologies.  
The documentation starts wih... and ends with...



<a name="installation-instructions"></a>
## Installation instructions

the OTC application must run on **python 3.6** version or above.  I have used two main python libraries in my code:

rdflib: https://github.com/RDFLib/rdflib

owlReady2: https://bitbucket.org/jibalamy/owlready2


The following four command lines to use for windows are:

>py -m virtualenv venv
>
>.\venv\Scripts\activate
>
>pip install -r .\requirements.txt
>
>py .\manage.py run

The following four command lines to use for Linux/MacOS are:

>python3 -m virtualenv venv
>
>source venv/bin/activate
>
>pip install -r requirements.txt
>
>python manage.py run

Note: For a very strange reason, I have scripted these commands in run-prod.sh (here inclided in the git) but the commande activate seems not working when embedded within a script. Same for any windows script (not included in the git).

<a name="service-endpoint-description"></a>
### Service endpoint description

I have set-up and used a Flask server to build the REST API (https://github.com/flask-restful/flask-restful)  
When deployed (over internet or localhost), the OTC service endpoint is based on its URL usage that URL to request an OTC service.  
Service endpoint should follow this pattern: [http://{Service URL}](https://<service-url>) including the defined port number.  
When deployed locally the API endpoint would look like this :  
>http://localhost:3000/\<servicename\>

<a name="error-handling"></a>
### Error handling

The OTC service uses standard HTTP response codes to indicate whether a method completed successfully. A 200 response always indicates success. A 400 type response is some sort of failure, and a 500 type response usually indicates an internal system error.  Response codes are listed with the method.

| Parameter         | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| Code <br> _integer_ | The HTTP error status code (200, 500, etc.).                     |
| Error <br> _string_ | Brief message describing the error type (success, failure, etc.) |

<a name="query-endpoint-action-list"></a>
## Query endpoint action list

The full code of these actions can be found in the _controllers.py_ file.  
The ontologies (**MediaComp** and **MediaClient**) are located under the **/OWL** directory.

<a name="merge-ontologies"></a>
#### Merge ontologies

Merges two graphs (i.e., knowledge bases) into one graph avoiding to duplicate concepts, properties, or instances when they have the same URI.
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
| status <br> _string_ | Ontologies are merged in file fileOnto1\_fileOnto2\_fusion.owl |

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

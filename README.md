------------------------------------------------------------------------------------------------------
ATELIER API-DRIVEN INFRASTRUCTURE
------------------------------------------------------------------------------------------------------
L’idée en 30 secondes : **Orchestration de services AWS via API Gateway et Lambda dans un environnement émulé**.  
Cet atelier propose de concevoir une architecture **API-driven** dans laquelle une requête HTTP déclenche, via **API Gateway** et une **fonction Lambda**, des actions d’infrastructure sur des **instances EC2**, le tout dans un **environnement AWS simulé avec LocalStack** et exécuté dans **GitHub Codespaces**. L’objectif est de comprendre comment des services cloud serverless peuvent piloter dynamiquement des ressources d’infrastructure, indépendamment de toute console graphique.Cet atelier propose de concevoir une architecture API-driven dans laquelle une requête HTTP déclenche, via API Gateway et une fonction Lambda, des actions d’infrastructure sur des instances EC2, le tout dans un environnement AWS simulé avec LocalStack et exécuté dans GitHub Codespaces. L’objectif est de comprendre comment des services cloud serverless peuvent piloter dynamiquement des ressources d’infrastructure, indépendamment de toute console graphique.
  
-------------------------------------------------------------------------------------------------------
Séquence 1 : Codespace de Github
-------------------------------------------------------------------------------------------------------
Objectif : Création d'un Codespace Github  
Difficulté : Très facile (~5 minutes)
-------------------------------------------------------------------------------------------------------
RDV sur Codespace de Github : <a href="https://github.com/features/codespaces" target="_blank">Codespace</a> **(click droit ouvrir dans un nouvel onglet)** puis créer un nouveau Codespace qui sera connecté à votre Repository API-Driven.
  
---------------------------------------------------
Séquence 2 : Création de l'environnement AWS (LocalStack)
---------------------------------------------------
Objectif : Créer l'environnement AWS simulé avec LocalStack  
Difficulté : Simple (~5 minutes)
---------------------------------------------------

Dans le terminal du Codespace copier/coller les codes ci-dessous etape par étape :  

**Installation de l'émulateur LocalStack**  
```
sudo -i mkdir rep_localstack
```
```
sudo -i python3 -m venv ./rep_localstack
```
```
sudo -i pip install --upgrade pip && python3 -m pip install localstack && export S3_SKIP_SIGNATURE_VALIDATION=0
```
```
localstack start -d
```
**vérification des services disponibles**  
```
localstack status services
```
**Réccupération de l'API AWS Localstack** 
Votre environnement AWS (LocalStack) est prêt. Pour obtenir votre AWS_ENDPOINT cliquez sur l'onglet **[PORTS]** dans votre Codespace et rendez public votre port **4566** (Visibilité du port).
Réccupérer l'URL de ce port dans votre navigateur qui sera votre ENDPOINT AWS (c'est à dire votre environnement AWS).
Conservez bien cette URL car vous en aurez besoin par la suite.  

Pour information : IL n'y a rien dans votre navigateur et c'est normal car il s'agit d'une API AWS (Pas un développement Web type UX).

---------------------------------------------------
Séquence 3 : Exercice
---------------------------------------------------
Objectif : Piloter une instance EC2 via API Gateway
Difficulté : Moyen/Difficile (~2h)
---------------------------------------------------  
Votre mission (si vous l'acceptez) : Concevoir une architecture **API-driven** dans laquelle une requête HTTP déclenche, via **API Gateway** et une **fonction Lambda**, lancera ou stopera une **instance EC2** déposée dans **environnement AWS simulé avec LocalStack** et qui sera exécuté dans **GitHub Codespaces**. [Option] Remplacez l'instance EC2 par l'arrêt ou le lancement d'un Docker.  

**Architecture cible :** Ci-dessous, l'architecture cible souhaitée.   
  
![Screenshot Actions](API_Driven.png)   
  
---------------------------------------------------  
## Processus de travail (résumé)

1. Installation de l'environnement Localstack (Séquence 2)
2. Création de l'instance EC2
3. Création des API (+ fonction Lambda)
4. Ouverture des ports et vérification du fonctionnement

---------------------------------------------------
Séquence 4 : Documentation  
Difficulté : Facile (~30 minutes)
---------------------------------------------------
**Complétez et documentez ce fichier README.md** pour nous expliquer comment utiliser votre solution.  
Faites preuve de pédagogie et soyez clair dans vos expliquations et processus de travail.  

L'URL pour DÉMARRER le serveur (via une requête POST) :
curl -X POST -H "Content-Type: application/json" -d '{"action": "start", "instance_id": "i-4144cbf385855b166"}' https://ideal-pancake-pj5r69qppvp5c96pq-4566.app.github.dev/restapis/tmqm1tuygc/prod/_user_request_/instance

L'URL pour STOPPER le serveur :
curl -X POST -H "Content-Type: application/json" -d '{"action": "stop", "instance_id": "i-4144cbf385855b166"}' https://ideal-pancake-pj5r69qppvp5c96pq-4566.app.github.dev/restapis/tmqm1tuygc/prod/_user_request_/instance

[Bonus] L'URL pour voir le STATUS du serveur :
curl -X POST -H "Content-Type: application/json" -d '{"action": "status", "instance_id": "i-4144cbf385855b166"}' https://ideal-pancake-pj5r69qppvp5c96pq-4566.app.github.dev/restapis/tmqm1tuygc/prod/_user_request_/instance


Objectif du projet
Ce projet a pour but de créer une architecture Cloud "Serverless" permettant de contrôler l'état d'un serveur Amazon EC2 (Démarrage, Arrêt, Statut) depuis l'extérieur, de manière totalement sécurisée, via une API REST. 

Tout a été déployé et testé localement grâce à LocalStack et GitHub Codespaces.

---

Mon Processus de Travail

Pour mener à bien ce projet, j'ai adopté une démarche itérative et rigoureuse :

1. Compréhension et tests manuels : Avant de tout automatiser, j'ai d'abord tapé chaque commande awscli manuellement dans le terminal. L'objectif était de bien comprendre les dépendances strictes d'AWS : par exemple, on ne peut pas créer une fonction Lambda sans lui avoir d'abord créé un rôle IAM (sécurité), et on ne peut pas l'invoquer via une API sans lui ajouter une autorisation explicite (add-permission).
   
2. Développement de la logique (Python) : J'ai rédigé le script lambda_function.py en utilisant la librairie boto3. J'ai structuré le code pour qu'il décode l'enveloppe JSON envoyée par l'API Gateway, lise l'argument action (start, stop, status) et renvoie une réponse HTTP formatée correctement (statusCode: 200).

3. Automatisation (Infrastructure as Code) : Une fois l'architecture validée, j'ai regroupé toutes mes commandes dans un script bash (deploy.sh). Cela permet de détruire et recréer toute l'infrastructure (EC2, IAM, Lambda, API) en une seule commande, rendant le projet totalement reproductible.

---

Fonctionnement de l'architecture

Pour être clair sur la façon dont les services communiquent entre eux, voici le parcours exact d'une requête lorsque vous utilisez l'API :

* 1. Amazon API Gateway (Le point d'entrée) : L'API expose la ressource /instance. Elle est configurée avec une méthode POST, ce qui oblige l'utilisateur à envoyer des données (le JSON) pour agir. Elle bloque les simples requêtes GET des navigateurs web.
* 2. AWS Lambda (Le cerveau logique) : C'est le code Python qui est réveillé par l'API. Il n'y a pas de serveur allumé en permanence pour faire tourner ce code, il ne s'exécute qu'à la demande (principe du Serverless).
* 3. AWS IAM (La sécurité) : Par défaut, AWS bloque tout. La Lambda possède un "rôle d'exécution" qui lui donne la permission explicite et unique de communiquer avec le service EC2. Sans cela, la requête serait rejetée.
* 4. Amazon EC2 (La cible) : C'est la machine virtuelle finale qui reçoit l'ordre de s'allumer ou de s'éteindre.

---

## Guide d'Utilisation : Tester la solution

Le port 4566 est exposé publiquement sur mon Codespace. Vous pouvez exécuter ces commandes depuis n'importe quel terminal externe pour agir sur le serveur virtuel.

(Note : L'identifiant de l'instance actuelle est i-4144cbf385855b166)

### Démarrer le serveur
` ` `bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"action": "start", "instance_id": "i-4144cbf385855b166"}' \
  https://ideal-pancake-pj5r69qppvp5c96pq-4566.app.github.dev/restapis/tmqm1tuygc/prod/_user_request_/instance
` ` `

### Stopper le serveur
` ` `bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"action": "stop", "instance_id": "i-4144cbf385855b166"}' \
  https://ideal-pancake-pj5r69qppvp5c96pq-4566.app.github.dev/restapis/tmqm1tuygc/prod/_user_request_/instance
` ` `

### [BONUS] Voir le statut du serveur
` ` `bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"action": "status", "instance_id": "i-4144cbf385855b166"}' \
  https://ideal-pancake-pj5r69qppvp5c96pq-4566.app.github.dev/restapis/tmqm1tuygc/prod/_user_request_/instance
` ` `


---------------------------------------------------
Evaluation
---------------------------------------------------
Cet atelier, **noté sur 20 points**, est évalué sur la base du barème suivant :  
- Repository exécutable sans erreur majeure (4 points)
- Fonctionnement conforme au scénario annoncé (4 points)
- Degré d'automatisation du projet (utilisation de Makefile ? script ? ...) (4 points)
- Qualité du Readme (lisibilité, erreur, ...) (4 points)
- Processus travail (quantité de commits, cohérence globale, interventions externes, ...) (4 points) 

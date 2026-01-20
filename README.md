# Projet 9 – Streaming de tickets avec Redpanda et Python

## 1. Objectif

Ce projet consiste à simuler un flux de tickets clients en temps réel en utilisant **Redpanda** (Kafka-compatible) et **Python**.  
L’objectif est de produire et consommer des données de tickets pour préparer l’analyse en temps réel avec **PySpark** dans les étapes suivantes.

## 2. Prérequis

- Docker & Docker Compose  
- Python 3.8+  
- pip ou conda pour installer les packages Python nécessaires  

## 3. Lancement de Redpanda avec Docker Compose

Créez un fichier `docker-compose.yml` avec le contenu suivant :  

> Voir le fichier `docker-compose.yml` (code provenant du site de Redpanda)

Lancer Redpanda et la console :  

```bash
docker-compose up -d
```


Vérifier que Redpanda fonctionne :
```bash
docker ps
```

Le broker Redpanda écoute sur localhost:19092

La console Redpanda accessible sur http://localhost:8080


## 4. Création d’un topic

Créer un topic `client_tickets` pour stocker les tickets :
```bash
docker exec -it redpanda-0 rpk topic create client_tickets
```
Ou directement sur l'interface sur http://localhost:8080


## 5. Script Python pour produire des tickets

Exemple de script `produce.py` contenue dans le dossier `producer`


Installer les dépendances :
```bash
pip install kafka-python
```

Lancer le script :
```bash
python produce_tickets.py
```

## 6. Validation

Consommer quelques messages pour vérifier que tout fonctionne :
```bash
docker exec -it redpanda-0 rpk topic consume client_tickets -b localhost:9092 --offset earliest --limit 5
```
Ou vérifier directement dans topic que messages se sont bien importés

## 7. Conseils

- Docker Compose facilite la gestion du broker et de la console Redpanda, et évite les problèmes de configuration sur Windows.

- Tous les scripts Python peuvent être lancés directement depuis l’hôte (Windows/Linux/Mac) vers le broker Redpanda exposé sur localhost:19092.
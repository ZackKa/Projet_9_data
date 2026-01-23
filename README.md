# POC – Pipeline de gestion de tickets clients en temps réel

## Etape 1

## 1. Objectif

Ce projet consiste à simuler un flux de tickets clients en temps réel en utilisant **Redpanda** (Kafka-compatible) et **Python**.  
L’objectif est de produire et consommer des données de tickets pour préparer l’analyse en temps réel avec **PySpark** dans les étapes suivantes.
Dans le cadre de la migration de l’infrastructure d’InduTechData vers AWS et Redpanda, ce projet a pour objectif de réaliser un Proof Of Concept (POC) d’un système de gestion de tickets clients en temps réel.

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

Le topic est crée automatiquement grâce au service `redpanda-init` dans `docker-compose`


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

## Etape 2

## Architecture mise en place (Étapes 1 & 2)
🔹 Composants

Redpanda

- Ingestion des tickets clients en temps réel

- Topic Kafka : client_tickets (3 partitions)

Producteur Python

- Génération de tickets aléatoires

- Envoi des messages au format JSON vers Redpanda

Spark Structured Streaming

- Lecture des messages Kafka

- Transformation, enrichissement et agrégation

- Affichage des résultats par micro-batch

Redpanda Console

- Visualisation des topics et des messages

## Flux de données

1 - Le script Python génère 200 tickets clients

2 - Les tickets sont envoyés dans le topic client_tickets

3 - Spark lit les messages depuis Redpanda

4 - Les données JSON sont parsées en DataFrame structuré

5 - Les tickets sont enrichis avec une équipe de support

6 - Une agrégation calcule le nombre de tickets par type

7 - Les résultats sont affichés par micro-batch dans la console Spark

## Structure du projet
```kotlin
project/
│
├── docker-compose.yml
│
├── producer/
│   └── producer.py
│
├── spark/
│   └── spark_streaming.py
│
├── ivy/
│
├── data/
│   ├── checkpoints/
│   └── output/
│
└── README.md
```
## Dossiers techniques importants
- 🔹 `ivy/`

Ce dossier est utilisé par Apache Ivy, le gestionnaire de dépendances de Spark.

👉 Il a été créé manuellement afin de :

permettre à Spark de télécharger les dépendances Kafka

éviter les erreurs du type /nonexistent/.ivy2/cache

Ce dossier garantit le bon fonctionnement de l’option :

```bash
--packages org.apache.spark:spark-sql-kafka-0-10_2.12
```

- 🔹 `data/checkpoints/`

Ce dossier est utilisé par Spark Structured Streaming pour le checkpointing.

Le checkpoint permet :

de mémoriser les offsets Kafka déjà consommés

d’assurer la reprise après arrêt

d’éviter de relire plusieurs fois les mêmes messages

👉 Il est obligatoire pour un pipeline streaming fiable.


- 🔹 `data/output/`

Ce dossier est destiné à recevoir les résultats des analyses (Parquet, JSON, etc.).

📌 À ce stade du projet, il est normal qu’il soit vide, car :

les résultats sont actuellement affichés uniquement dans la console (format("console"))

l’export vers un fichier sera réalisé à l’étape 3

## Traitements réalisés avec Spark

- 🔹 Parsing JSON

Les messages Kafka (bytes) sont convertis en colonnes structurées via un schéma explicite.

- 🔹 Enrichissement

Ajout automatique d’une colonne support_team :

TECHNICAL → Tech Support

BILLING → Billing Team

ACCOUNT → Account Management

GENERAL → General Support

- 🔹 Agrégation

Calcul du nombre de tickets par type de demande, mis à jour en continu.

## Gestion des micro-batchs

Les messages sont traités en micro-batchs

Un checkpoint est utilisé pour garantir l’état du streaming

Le résultat final confirme la consommation des 200 tickets produits

## Lancement du projet

- Précision, le `docker-compose.yml` a été modifié pour intégrer Spark

```bash
docker-compose up
```

Redpanda Console est accessible à l’adresse :
```bash
http://localhost:8080
```


## Etape 3

## Architecture générale

- Redpanda : broker Kafka (ingestion temps réel)

- Kafka Producer (Python) : génération de tickets clients

- Spark Structured Streaming (Docker) :

 - lecture des messages Kafka

 - enrichissement

 - agrégation

 - export JSON final

- Docker Compose : orchestration de l’ensemble


## 📁 Structure du projet
```kotlin
Projet_9_Exercice2/
│
├── docker-compose.yml
├── producer.py
│
├── spark/
│   └── spark_streaming.py
│
├── data/
│   ├── checkpoints/
│   │   └── client_tickets/
│   └── output/
│       └── client_tickets/
│
├── ivy/
│
└── README.md
```


### 📌 Dossiers créés manuellement

- ivy/
→ utilisé par Spark pour stocker les dépendances Maven (Kafka connector)

- data/

 - checkpoints/ : nécessaire au fonctionnement de Spark Streaming

 - output/ : stockage des résultats

     - client_tickets/ : fichier JSON final



## 🔄 Étapes 2 & 3 – Traitement + Export (combinées)

#### 👉 Les étapes 2 et 3 ont été regroupées volontairement dans un seul pipeline Spark, afin de :

- traiter les données en streaming

- exporter directement le résultat final sans script supplémentaire

### Pourquoi cette approche ?

Spark Structured Streaming ne permet pas l’écriture directe en JSON avec outputMode("complete")

La solution recommandée est l’utilisation de foreachBatch

Cela permet d’avoir :

- du streaming

- un DataFrame classique par batch

- un export final maîtrisé

## 🧠 Traitement Spark (spark_streaming.py)
### Fonctions réalisées :

1. Lecture du topic Kafka client_tickets

2. Parsing JSON

3. Enrichissement :

- attribution d’une équipe support selon le type

4. Agrégation :

- nombre de tickets par type

5. Export automatique des résultats finaux en JSON

### Points techniques clés :

`startingOffsets` = earliest → reprise des 200 messages de l’étape 1

`maxOffsetsPerTrigger` = 50 → micro-batchs contrôlés

`foreachBatch` → export JSON final

`checkpointLocation` → reprise fiable du streaming

## 📦 Export des résultats (Étape 3)

Le fichier final est généré automatiquement ici :
```bash
data/output/client_tickets/
└── part-00000-xxxx.json
```

Contenu final (exemple) :
```bash
{"type":"ACCOUNT","ticket_count":52}
{"type":"BILLING","ticket_count":50}
{"type":"GENERAL","ticket_count":53}
{"type":"TECHNICAL","ticket_count":45}
```

✔ Total = 200 tickets
✔ Tous les messages ont été traités
✔ Aucune perte de données

## 🐳 Lancement du pipeline complet

Une fois les scripts prêts :
```bash
docker-compose up -d
```

Ce lancement :

- démarre Redpanda

- démarre Spark

- relit les 200 messages existants

- traite et exporte automatiquement les résultats

## ✅ Résultat final

✔ Pipeline temps réel fonctionnel

✔ Traitement Spark validé

✔ Export JSON conforme à l’étape 3

✔ Étapes 2 et 3 correctement combinées

✔ Projet entièrement reproductible avec Docker

🏁 Conclusion

Ces étapes du projet démontre la mise en œuvre complète d’un pipeline temps réel industriel, depuis l’ingestion Kafka jusqu’à l’export de données analysées, en s’appuyant sur des outils standards du Data Engineering moderne.


## Étape 4 – Contenerisation du pipeline ETL
## Objectif

Cette étape consiste à dockeriser l’ensemble du projet ETL :

- Redpanda : broker Kafka

- Producer : script générateur de tickets

- Spark Streaming : traitement en temps réel des tickets

- Docker Compose : orchestration automatique

Résultat : un pipeline complètement automatisé, traçable et reproductible.

## Structure des fichiers
```kotlin
.
├── docker-compose.yml
├── redpanda/
│   └── Dockerfile
├── producer/
│   ├── Dockerfile
│   └── producer.py
├── spark/
│   ├── Dockerfile
│   └── spark_streaming.py
├── data/
│   ├── output/
│   └── checkpoints/
└── ivy/
```

## Dockerfiles

#### Redpanda (redpanda/Dockerfile)

- Base : docker.redpanda.com/redpandadata/redpanda:v25.3.4

- Contient les commandes pour démarrer Redpanda en mode dev-container

- Ports exposés et services Kafka, RPC, Schema Registry et PandaProxy

#### Producer (producer/Dockerfile)

- Base : python:3.10-slim

- Installe kafka-python

- Lance le script producer.py pour envoyer les tickets dans Kafka

#### Spark (spark/Dockerfile)

- Base : apache/spark:3.5.8

- Copie spark_streaming.py

- Lance le script Spark avec le package Kafka intégré

## Lancer le pipeline
### 1️⃣ Nettoyage complet

Avant de relancer le pipeline, supprimer tous les conteneurs, volumes et images :
```bash
docker-compose down -v
```

Nettoyer aussi le contenu des dossiers locaux (laisser les dossiers vides) :
```bash
data/output/
data/checkpoints/
ivy/
```

⚠️ Important pour éviter :

- la reprise de vieux checkpoints Spark

- les conflits Ivy

### 2️⃣ Relance automatique

Tout le pipeline peut maintenant être lancé en une seule commande :
```bash
docker-compose up --build
```

Tout est automatisé :

- Redpanda démarre

- Le producer envoie les tickets

- Spark consomme et traite les tickets

- Le JSON final est généré dans data/output/client_tickets/

### 3️⃣ Suivi de la progression

Il y a 4 manières complémentaires de suivre ce qui se passe :

#### 🟢 A. Logs du Producer
```bash
docker logs -f producer
```

On observe des messages comme :
```bash
Ticket envoyé: {'type': 'ACCOUNT', ...}
Ticket envoyé: {'type': 'TECHNICAL', ...}
```

- Tant que ça défile → tickets en cours d’envoi

- Quand ça s’arrête → les 200 tickets ont été envoyés

#### 🟡 B. Logs de Spark Streaming
```bash
docker logs -f spark
```

Affichage typique :
```bash
-------------------------------------------
Batch: 1
-------------------------------------------
ACCOUNT | 3
...
Batch: 2
...
```

- Chaque Batch: correspond à un micro-batch Spark

- Quand les chiffres se stabilisent → plus de nouveaux messages

#### 🔵 C. Interface Redpanda Console (visuel)

Accéder à :
```bash
http://localhost:8080
```

- Voir le topic `client_tickets`

- Suivre le nombre de messages

- Observer le lag du consommateur

#### 🟣 D. Vérification du JSON final

Dans le PC, vérifier :
```bash
data/output/client_tickets/
```

Fichiers attendus :

`part-00000-*.json` → contient le résultat final agrégé

`_SUCCESS` → indique la fin du job Spark

Exemple de contenu JSON :
```bash
{"type":"ACCOUNT","ticket_count":52}
{"type":"BILLING","ticket_count":50}
{"type":"GENERAL","ticket_count":53}
{"type":"TECHNICAL","ticket_count":45}
```

## 4️⃣ Conclusion

Le pipeline ETL est entièrement automatisé avec Docker Compose :

- Les messages sont produits dans Kafka

- Ils sont consommés en streaming par Spark

- Les résultats sont exportés automatiquement au format JSON

- La progression est observable via les logs et l’interface Redpanda Console, ce qui rend le pipeline traçable et reproductible.
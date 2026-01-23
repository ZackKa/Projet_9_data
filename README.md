# POC – Pipeline temps réel de gestion de tickets clients
## Objectif

POC d’un pipeline temps réel de gestion de tickets clients dans le cadre de la migration d’InduTechData vers AWS + Redpanda.

Le pipeline permet de :

- produire des tickets clients

- les traiter en streaming avec Spark Structured Streaming

- agréger les résultats

- exporter automatiquement un JSON final

## Architecture globale

Technologies utilisées :

- Redpanda (Kafka-compatible)

- Python (producer)

- Spark Structured Streaming

- Docker & Docker Compose

Flux de données :

- Le producer génère 200 tickets clients

- Les messages sont envoyés dans le topic `client_tickets`

- Spark consomme les messages en streaming

- Parsing + enrichissement

- Agrégation par type de ticket

- Export JSON final

## Structure du projet
```kotlin
project/
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
│   ├── checkpoints/
│   └── output/
│       └── client_tickets/
├── ivy/
└── README.md
```

## Dossiers techniques importants
`ivy/`

Utilisé par Spark pour télécharger les dépendances Kafka
Évite les erreurs de type `/nonexistent/.ivy2/cache`

`data/checkpoints/`

Checkpoint Spark Streaming :

- mémorisation des offsets Kafka

- reprise après arrêt

- fiabilité du pipeline

`data/output/`

Contient les résultats finaux exportés au format JSON

## Traitements Spark

Parsing JSON avec schéma explicite

Enrichissement automatique (`support_team`)

Agrégation : nombre de tickets par type

Straming contrôlé par micro-batchs

Export JSON via `foreachBatch`

## Lancer le pipeline complet
#### Nettoyage (recommandé en cas de relance)
```bash
docker-compose down -v
```

Créer ou Vider (en cas de relance) :
```bash
data/output/
data/checkpoints/
ivy/
```
#### Lancement
```bash
docker-compose up --build
```

## Résultat final

Fichier généré :
```bash
data/output/client_tickets/part-00000-xxxx.json
```

Exemple :
```json
{"type":"ACCOUNT","ticket_count":52}
{"type":"BILLING","ticket_count":50}
{"type":"GENERAL","ticket_count":53}
{"type":"TECHNICAL","ticket_count":45}
```

✔ 200 tickets traités
✔ Aucun message perdu
✔ Pipeline 100 % reproductible

## Suivi et monitoring

Logs Producer : `docker logs -f producer` ou sur Docker Desktop

Logs Spark : `docker logs -f spark` ou sur Docker Desktop

Redpanda Console : http://localhost:8080

## Conclusion

Ce POC démontre la mise en œuvre complète d’un pipeline temps réel industriel, de l’ingestion Kafka à l’export de données agrégées, en s’appuyant sur les standards du Data Engineering moderne.
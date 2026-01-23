# import json
# import time
# import random
# from datetime import datetime
# from kafka import KafkaProducer

# # Configuration Kafka / Redpanda
# producer = KafkaProducer(
#     bootstrap_servers="localhost:19092",
#     value_serializer=lambda v: json.dumps(v).encode("utf-8")
# )

# TOPIC_NAME = "client_tickets"

# REQUEST_TYPES = ["TECHNICAL", "BILLING", "ACCOUNT", "GENERAL"]
# PRIORITIES = ["LOW", "MEDIUM", "HIGH"]
# REQUEST_MESSAGES = [
#     "Problème de connexion",
#     "Erreur de facturation",
#     "Demande de changement de compte",
#     "Question générale"
# ]

# ticket_counter = 1

# print("🚀 Producer démarré – envoi de tickets...")

# while True:
#     ticket = {
#         "ticket_id": f"TCK-{ticket_counter:05d}",
#         "client_id": f"CL-{random.randint(100, 999)}",
#         "created_at": datetime.utcnow().isoformat(),
#         "request": random.choice(REQUEST_MESSAGES),
#         "type": random.choice(REQUEST_TYPES),
#         "priority": random.choice(PRIORITIES)
#     }

#     producer.send(TOPIC_NAME, ticket)
#     producer.flush()

#     print(f"📨 Ticket envoyé : {ticket['ticket_id']}")

#     ticket_counter += 1
#     time.sleep(1)  # 1 ticket par seconde

import json  # Pour convertir des objets Python en JSON (sérialisation)
import time  # Pour gérer les pauses (sleep)
import random  # Pour générer des valeurs aléatoires
from datetime import datetime, timezone  # Pour obtenir la date et l'heure actuelles avec fuseau horaire
from kafka import KafkaProducer  # Pour produire des messages dans Kafka

# Configuration Kafka / Redpanda
producer = KafkaProducer(
    bootstrap_servers="redpanda-0:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8") # Fonction pour transformer les objets Python en JSON avant de les envoyer
)
# bootstrap_servers="localhost:19092", # Adresse du serveur Kafka ou Redpanda (ici en local sur le port 19092)


TOPIC_NAME = "client_tickets" # Nom du topic Kafka dans lequel on va envoyer les tickets

REQUEST_TYPES = ["TECHNICAL", "BILLING", "ACCOUNT", "GENERAL"] # Types de demandes possibles pour les tickets
PRIORITIES = ["LOW", "MEDIUM", "HIGH"] # Priorités possibles pour les tickets
REQUEST_MESSAGES = [ # Messages possibles pour les tickets
    "Problème de connexion",
    "Erreur de facturation",
    "Demande de changement de compte",
    "Question générale"
]

NB_TICKETS = 200          # Nombre total de tickets à générer
INTERVAL_SECONDS = 1      # Intervalle entre chaque ticket (en secondes)

print("🚀 Producer démarré – envoi de tickets...")

for ticket_counter in range(1, NB_TICKETS + 1):
    ticket = { # Création d'un dictionnaire représentant un ticket
        "ticket_id": f"TCK-{ticket_counter:05d}", # ID du ticket avec format TCK-00001, TCK-00002, ... (5 chiffres)
        "client_id": f"CL-{random.randint(100, 999)}", # ID client aléatoire entre 100 et 999, format CL-123
        "created_at": datetime.now(timezone.utc).isoformat(), # Date et heure de création en UTC, format ISO 8601
        "request": random.choice(REQUEST_MESSAGES), # Message de la demande choisi aléatoirement
        "type": random.choice(REQUEST_TYPES), # Type de demande choisi aléatoirement
        "priority": random.choice(PRIORITIES) # Priorité de la demande choisie aléatoirement
    }

    producer.send(TOPIC_NAME, ticket) # Envoi du ticket dans le topic Kafka
    producer.flush() # Forcer l'envoi immédiat (flush) pour ne pas accumuler les messages

    print(f"📨 Ticket envoyé : {ticket['ticket_id']}") # Affichage du ticket envoyé pour suivi

    time.sleep(INTERVAL_SECONDS)  # Pause avant de générer le ticket suivant pour respecter l'intervalle

producer.close() # Fermeture du producer Kafka après la fin de l'envoi
print(f"✅ Production terminée – {NB_TICKETS} tickets envoyés") # Affichage du nombre total de tickets envoyés

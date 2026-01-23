# Image de base Python légère (version 3.10)
FROM python:3.10-slim
# Définition du répertoire de travail dans le conteneur
WORKDIR /app
# Copie du script Python (producteur Kafka) dans le conteneur
COPY producer.py .
# Installation de la librairie Python kafka-python pour communiquer avec Kafka
RUN pip install kafka-python
# Commande exécutée au démarrage : lance le script Python
CMD ["python", "producer.py"]
FROM apache/spark:3.5.8
# Définition du répertoire de travail dans le conteneur
WORKDIR /opt/spark-apps
# Copie du script Spark Streaming dans le conteneur
COPY spark_streaming.py .

CMD ["/opt/spark/bin/spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "spark_streaming.py"]
 # Commande exécutée au démarrage du conteneur
 # "/opt/spark/bin/spark-submit", Lancement de Spark avec spark-submit
 # "--packages", Option pour ajouter des dépendances externes
 # "org.apache...", Connecteur Spark ↔ Kafka
 # "spark_streaming.py", Script  à exécuter
# VERSION INTEGRANT ETAPE 2 UNIQUEMENT

# from pyspark.sql import SparkSession  # Pour créer une session Spark
# from pyspark.sql.functions import (   # Fonctions utiles pour manipuler les DataFrames
#     from_json,  # Convertit une colonne JSON en colonnes structurées
#     col,       # Pour sélectionner ou manipuler une colonne
#     count,     # Pour compter le nombre de lignes
#     when       # Pour appliquer des conditions (if/else) dans les colonnes
# )
# from pyspark.sql.types import StructType, StructField, StringType  # Pour définir le schéma d’un DataFrame


# # Spark Session

# spark = SparkSession.builder \
#     .appName("ClientTicketsStreaming") \
#     .getOrCreate() # retourne la session Spark active si elle existe déjà dans le processus, sinon en crée une nouvelle avec la configuration définie avant l’appel (appName)

# spark.sparkContext.setLogLevel("WARN") # Définit le niveau de log à WARN (warnings) pour éviter trop d’informations


# # Schéma des tickets

# ticket_schema = StructType([ # On décrit la structure attendue des tickets reçus depuis Kafka
#     StructField("ticket_id", StringType()),  # ID du ticket
#     StructField("client_id", StringType()),  # ID du client
#     StructField("created_at", StringType()), # Date de création
#     StructField("request", StringType()),    # Message de la demande
#     StructField("type", StringType()),       # Type de demande (TECHNICAL, BILLING, ...)
#     StructField("priority", StringType())    # Priorité (LOW, MEDIUM, HIGH)
# ])


# # Lecture Kafka / Redpanda

# # DataFrame Spark (spécial de type “streaming”) créé avec readStream pour lire le flux de données depuis Kafka
# # Il ne contient pas toutes les données en mémoire, il va les lire en micro-batch à mesure qu’elles arrivent sur le topic.
# raw_df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "redpanda-0:9092") \
#     .option("subscribe", "client_tickets") \
#     .option("startingOffsets", "earliest") \
#     .option("maxOffsetsPerTrigger", 50) \
#     .load() # charge les données du flux Kafka dans un DataFrame Spark
# # Indique que la source est Kafka, l'adresse du broker Kafka, le topic Kafka à écouter, lecture depuis le début et la création d'un DataFrame représentant le flux de données


# # Parsing JSON

# # Kafka envoie les messages sous forme binaire dans la colonne "value"
# tickets_df = raw_df.select( # On convertit chaque message JSON en colonnes structurées selon le schéma défini
#     from_json(col("value").cast("string"), ticket_schema).alias("data") # Les messages Kafka arrivent en bytes (binaire). cast("string") convertit ces bytes en chaîne de caractères JSON. alias("data") donne un nom à la colonne résultante pour la sélection plus tard.
# ).select("data.*") # Au lieu d’avoir data.ticket_id, data.client_id… On a juste ticket_id, client_id directemen

# # "from_json(..., ticket_schema)"
# # Cette fonction prend la chaîne JSON et la transforme en colonnes structurées selon ticket_schema.
# # Résultat : une seule colonne data de type struct (comme un mini-objet contenant toutes les colonnes : ticket_id, client_id, etc.).
# # On prend chaque message on le met dans la colonne data puis on "sépare" les colonnes pour avoir ticket_id, client_id, etc.


# # Enrichissement : équipe support

# tickets_enriched_df = tickets_df.withColumn( # On ajoute une nouvelle colonne "support_team" selon le type de ticket (TECHNICAL, BILLING, ACCOUNT, GENERAL)
#     "support_team",
#     when(col("type") == "TECHNICAL", "Tech Support")
#     .when(col("type") == "BILLING", "Billing Team")
#     .when(col("type") == "ACCOUNT", "Account Management")
#     .otherwise("General Support")
# )


# # Agrégation : nombre de tickets par type

# tickets_agg_df = tickets_enriched_df.groupBy("type").agg(
#     count("*").alias("ticket_count")
# ) # On groupe les tickets par "type" et on compte combien il y a dans chaque groupe


# # Output console (debug)

# # Affiche les résultats agrégés dans la console en streaming (affichage continu des résultats)
# query = tickets_agg_df.writeStream \
#     .outputMode("complete") \
#     .format("console") \
#     .option("truncate", False) \
#     .option("checkpointLocation", "/opt/spark-data/checkpoints/client_tickets") \
#     .start()
# # Mode "complete" : affiche tout le résultat à chaque micro-batch
# # Format "console" : affiche les résultats dans la console
# # Option "truncate" :  Ne tronque pas les colonnes longues (affichage complet)
# # Start() : démarre la requête de streaming
# query.awaitTermination() # Attente infinie jusqu’à ce que le streaming soit arrêté
     

# VERSION INTEGRANT ETAPE 2 & 3     

from pyspark.sql import SparkSession                  # Import de la session Spark
from pyspark.sql.functions import from_json, col, count, when  # Fonctions Spark SQL utilisées
from pyspark.sql.types import StructType, StructField, StringType  # Types pour définir le schéma

# =====================================================
# Spark Session
# =====================================================

spark = SparkSession.builder \
    .appName("ClientTicketsStreaming") \
    .getOrCreate() # retourne la session Spark active si elle existe déjà dans le processus, sinon en crée une nouvelle avec la configuration définie avant l’appel (appName)

spark.sparkContext.setLogLevel("WARN") # Définit le niveau de log à WARN (warnings) pour éviter trop d’informations


# =====================================================
# Schéma des tickets
# =====================================================

ticket_schema = StructType([ # On décrit la structure attendue des tickets reçus depuis Kafka
    StructField("ticket_id", StringType()),  # ID du ticket
    StructField("client_id", StringType()),  # ID du client
    StructField("created_at", StringType()), # Date de création
    StructField("request", StringType()),    # Message de la demande
    StructField("type", StringType()),       # Type de demande (TECHNICAL, BILLING, ...)
    StructField("priority", StringType())    # Priorité (LOW, MEDIUM, HIGH)
])

# =====================================================
# Lecture Kafka / Redpanda (STREAMING)
# =====================================================
# On lit les messages en temps réel depuis Kafka (Redpanda). Chaque message correspond à un ticket client au format JSON.
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "redpanda-0:9092") \
    .option("subscribe", "client_tickets") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 50) \
    .load()
    # Lecture de données en streaming; Source Kafka (Redpanda compatible Kafka); Adresse du broker Kafka; Topic Kafka à consommer;
    # Lecture depuis le début du topic; Nombre max de messages par micro-batch; Chargement du flux Kafka 

# =====================================================
# Parsing JSON
# =====================================================
# Kafka envoie les messages sous forme binaire dans la colonne "value"
tickets_df = raw_df.select( # On convertit chaque message JSON en colonnes structurées selon le schéma défini
    from_json(col("value").cast("string"), ticket_schema).alias("data") # Les messages Kafka arrivent en bytes (binaire). cast("string") convertit ces bytes en chaîne de caractères JSON. alias("data") donne un nom à la colonne résultante pour la sélection plus tard.
).select("data.*")# Au lieu d’avoir data.ticket_id, data.client_id… On a juste ticket_id, client_id directemen
# "from_json(..., ticket_schema)"
# Cette fonction prend la chaîne JSON et la transforme en colonnes structurées selon ticket_schema.
# Résultat : une seule colonne data de type struct (comme un mini-objet contenant toutes les colonnes : ticket_id, client_id, etc.).
# On prend chaque message on le met dans la colonne data puis on "sépare" les colonnes pour avoir ticket_id, client_id, etc.

# =====================================================
# Enrichissement
# =====================================================

tickets_enriched_df = tickets_df.withColumn(  # On ajoute une nouvelle colonne "support_team" selon le type de ticket (TECHNICAL, BILLING, ACCOUNT, GENERAL)
    "support_team",
    when(col("type") == "TECHNICAL", "Tech Support")
    .when(col("type") == "BILLING", "Billing Team")
    .when(col("type") == "ACCOUNT", "Account Management")
    .otherwise("General Support")
)


# =====================================================
# Agrégation
# =====================================================

tickets_agg_df = tickets_enriched_df.groupBy("type").agg(
    count("*").alias("ticket_count")
) # On groupe les tickets par "type" et on compte combien il y a dans chaque groupe

# =====================================================
# EXPORT FINAL JSON (foreachBatch)
# =====================================================

def write_final_json(batch_df, batch_id): # Fonction appelée à chaque micro-batch
   
    batch_df.coalesce(1).write \
        .mode("overwrite") \
        .json("/opt/spark-data/output/client_tickets")
# Réduction à un seul fichier de sortie coalesce(1); Écrasement de l’ancienne sortie (ancien fichier); Écriture au format JSON

# =====================================================
# WriteStream
# =====================================================

query = tickets_agg_df.writeStream \
    .outputMode("complete") \
    .foreachBatch(write_final_json) \
    .option("checkpointLocation", "/opt/spark-data/checkpoints/client_tickets") \
    .start()
# Écriture du DataFrame streaming; Réécriture complète des agrégations; Appel de la fonction d’écriture;
# Dossier de checkpoint pour la tolérance aux pannes; Démarrage du streaming

query.awaitTermination()

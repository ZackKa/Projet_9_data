FROM docker.redpanda.com/redpandadata/redpanda:v25.3.4
# Commande exécutée au démarrage du conteneur : lancement de Redpanda en mode développement pour conteneur

  CMD ["redpanda", "start", "--mode", "dev-container", "--kafka-addr", "internal://0.0.0.0:9092,external://0.0.0.0:19092", "--advertise-kafka-addr", "internal://redpanda-0:9092,external://localhost:19092", "--pandaproxy-addr", "internal://0.0.0.0:8082,external://0.0.0.0:18082", "--advertise-pandaproxy-addr", "internal://redpanda-0:8082,external://localhost:18082", "--schema-registry-addr", "internal://0.0.0.0:8081,external://0.0.0.0:18081", "--rpc-addr", "redpanda-0:33145", "--advertise-rpc-addr", "redpanda-0:33145", "--smp", "1", "--default-log-level", "info"]
  # Démarrage du processus Redpanda
  # Adresse Kafka pour les connexions internes et externes
  # Adresse Kafka annoncée aux clients (différente pour dev/local)
  # Adresse du PandaProxy pour les connexions internes et externes
  # Adresse PandaProxy annoncée aux clients
  # Adresse du Schema Registry (internes/externes)
  # Adresse RPC pour la communication interne entre nœuds Redpanda
  # Adresse RPC annoncée aux autres nœuds
  # Nombre de cœurs à utiliser pour Redpanda
  # Niveau de logs par défaut
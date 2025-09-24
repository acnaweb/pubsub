import json

from google.cloud import pubsub_v1
from loguru import logger


def publish_json(project_id, topic, payload):
    try:
        topic_path = f"projects/{project_id}/topics/{topic}"
        publisher = pubsub_v1.PublisherClient()

        message_bytes = json.dumps(payload).encode("utf-8")
        future = publisher.publish(topic_path, message_bytes)
        logger.info(f"Mensagem publicada com ID: {future.result()}")
    except Exception as e:
        logger.error(str(e))


if __name__ == "__main__":
    logger.info("Preparando...")

    project_id = "my-gcp-project"
    topic = "my-topic"

    payload = {
        "evento": "movimento_judicial",
        "cliente_id": "CUST-12345",
        "processo_id": "PROC-67890",
        "valor_divida": 150000.75,
        "moeda": "BRL",
        "status": "em andamento",
        "data_ocorrencia": "2025-09-22T15:45:00Z",
        "fonte": "sistema_judicial",
        "detalhes": {
            "tribunal": "TJ-SP",
            "comarca": "São Paulo",
            "numero_processo": "0001234-56.2025.8.26.0100",
        },
    }

    publish_json(project_id, topic, payload)

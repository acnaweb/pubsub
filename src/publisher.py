import json
import os
from typing import Any, Dict

from google.cloud import pubsub_v1
from loguru import logger


def publish_json(project_id: str, topic: str, payload: Dict[str, Any]) -> None:
    """Publica um payload JSON em um tópico do Pub/Sub."""

    topic_path = f"projects/{project_id}/topics/{topic}"

    try:
        with pubsub_v1.PublisherClient() as publisher:
            message_bytes = json.dumps(payload).encode("utf-8")
            future = publisher.publish(topic_path, message_bytes)

            # Callback para log assíncrono
            future.add_done_callback(
                lambda f: logger.info(f"Mensagem publicada com ID: {f.result()}")
            )

            logger.debug(f"Payload publicado: {json.dumps(payload, indent=2)}")

    except Exception as e:
        logger.exception(f"Erro ao publicar no tópico {topic_path}: {e}")


def main() -> None:
    logger.info("Iniciando publisher...")

    # Lê config de variáveis de ambiente (com defaults)
    project_id = os.getenv("GCP_PROJECT_ID", "my-gcp-project")
    topic = os.getenv("PUBSUB_TOPIC", "my-topic")

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


if __name__ == "__main__":
    main()

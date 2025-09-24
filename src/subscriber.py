import json
import os
import signal

from google.cloud import pubsub_v1
from loguru import logger

# Flag de controle para shutdown gracioso
running = True


def shutdown_handler(sig, frame):
    global running
    logger.warning("Finalizando subscriber...")
    running = False


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    """Processa mensagens recebidas do Pub/Sub."""
    try:
        data = json.loads(message.data.decode("utf-8"))
        logger.info(f"Mensagem recebida: {json.dumps(data, indent=2)}")

        # Marcar como processada (ack)
        message.ack()
        logger.debug(f"Ack enviado para mensagem ID {message.message_id}")

    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar mensagem: {e}")
        message.nack()  # devolve para fila


def main() -> None:
    # Lê config de ambiente
    project_id = os.getenv("GCP_PROJECT_ID", "my-gcp-project")
    subscription = os.getenv("PUBSUB_SUBSCRIPTION", "my-subscription")

    subscription_path = f"projects/{project_id}/subscriptions/{subscription}"

    logger.info(f"Iniciando subscriber no projeto '{project_id}'...")
    logger.info(f"Assinando subscription: {subscription_path}")

    # Registrar handler de interrupção (Ctrl+C)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    with pubsub_v1.SubscriberClient() as subscriber:
        future = subscriber.subscribe(subscription_path, callback=callback)

        try:
            while running:
                # Bloqueia em loop até receber sinal de interrupção
                future.result(timeout=5)
        except Exception as e:
            logger.exception(f"Erro no subscriber: {e}")
        finally:
            future.cancel()
            logger.info("Subscriber encerrado com sucesso.")


if __name__ == "__main__":
    main()

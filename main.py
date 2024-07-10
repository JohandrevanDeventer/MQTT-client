import os

from dotenv import load_dotenv  # pylint: disable=import-error

from src.id_generator import id_generator
from src.mqtt import client

BROKER = "broker.emqx.io"
PORT = 1883
CLIENT_ID = "BMS Client"
TOPIC = "Rubicon/BMS/Default/Raw"
QOS = 0
CLEAN_SESSION = True
KEEP_ALIVE = 60
RECONNECT_ON_FAILURE = True
USERNAME = None
PASSWORD = None


def configure():
    """Load environment variables from the .env file."""

    load_dotenv()


def main():
    """Main function"""

    configure()

    broker = os.getenv("BROKER", BROKER)
    port = os.getenv("PORT", str(PORT))
    client_id = os.getenv("CLIENT_ID", CLIENT_ID)
    topic = os.getenv("TOPIC", TOPIC)
    qos = os.getenv("QOS", str(QOS))
    clean_session = os.getenv("CLEAN_SESSION", str(CLEAN_SESSION)) == "True"
    keep_alive = os.getenv("KEEP_ALIVE", str(KEEP_ALIVE))
    reconnect_on_failure = (
        os.getenv("RECONNECT_ON_FAILURE", str(RECONNECT_ON_FAILURE)) == "True"
    )
    username = os.getenv("USERNAME", USERNAME)
    password = os.getenv("PASSWORD", PASSWORD)

    try:
        port = int(port)
    except ValueError:
        port = PORT

    try:
        qos = int(qos)
    except ValueError:
        qos = QOS

    try:
        keep_alive = int(keep_alive)
    except ValueError:
        keep_alive = KEEP_ALIVE

    if username == "None":
        username = None

    if password == "None":
        password = None

    client_id = id_generator.generate_client_id(client_id, 9)

    client_obj = client.MQTTClient(
        broker,
        port,
        client_id,
        topic,
        qos,
        clean_session,
        keep_alive,
        reconnect_on_failure,
        username,
        password,
    )
    client_obj.connect_client()


if __name__ == "__main__":
    main()

import json
import logging
import time
import paho.mqtt.client as mqtt  # pylint: disable=import-error

RECONNECT_DELAY = 5


# pylint: disable=too-many-instance-attributes
class MQTTClient:
    """MQTT Client class"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        broker: str,
        port: int,
        client_id: str,
        topic: str,
        qos: int = 0,
        clean_session: bool = True,
        keep_alive: int = 60,
        reconnect_on_failure: bool = True,
        username: str = None,
        password: str = None,
    ):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.topic = topic
        self.qos = qos
        self.clean_session = clean_session
        self.keep_alive = keep_alive
        self.reconnect_on_failure = reconnect_on_failure
        self.username = username
        self.password = password

        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(__name__)

    def test_parameters(self):
        """Test the class parameters"""

        class_parameter_dict = {
            "broker": str,
            "port": int,
            "client_id": str,
            "topic": str,
            "qos": int,
            "clean_session": bool,
            "keep_alive": int,
            "reconnect_on_failure": bool,
            "username": str,
            "password": str,
        }

        for name, expected_type in class_parameter_dict.items():
            value = getattr(self, name)

            if not isinstance(value, expected_type):
                if not value is None:
                    raise ValueError(
                        f"[CLIENT] {name} is not of type {expected_type.__name__}. Got {type(value).__name__} instead."
                    )

    def on_connect(self, client, userdata, flags, rc):
        """on_connect callback"""

        if rc == 0:
            self.log.info(f"[CLIENT] Connected to broker with result code: {rc}")
            self.log.info(f"[CLIENT] Subscribing to topic: {self.topic}")
            client.subscribe(topic=self.topic, qos=self.qos)
        else:
            self.log.error(
                f"[CLIENT] Failed to connect to broker with result code: {rc}"
            )

    def on_disconnect(self, client, userdata, rc):
        """on_disconnect callback"""

        if rc == 0:
            self.log.info(f"[CLIENT] Disconnected from broker with result code: {rc}")
        else:
            self.log.error(f"[CLIENT] Unexpected disconnection: {rc}")

            if self.reconnect_on_failure:
                self.log.info(
                    f"[CLIENT] Reconnecting to the broker in {RECONNECT_DELAY}s..."
                )
                time.sleep(RECONNECT_DELAY)
                client.reconnect()

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """on_subscribe callback"""

        self.log.info(
            f"[CLIENT] Subscribed with mid: {mid}, granted QoS: {granted_qos}"
        )

    def on_message(self, client, userdata, message):
        """on_message callback"""

        if isinstance(message.payload, bytes):
            payload = message.payload.decode("utf-8")

        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            pass

        self.log.info(f"[MESSAGE] Message received on topic {message.topic}: {payload}")

    def on_log(self, client, userdata, level, buf):
        """on_log callback"""

        self.log.debug(f"[CLIENT] Log: {buf}")

    def connect_client(self):
        """Connect to the MQTT broker"""

        self.log.debug("[CLIENT] Connecting MQTT client.")

        self.log.debug("[CLIENT] Testing class parameters.")
        try:
            self.test_parameters()
        except ValueError as e:
            self.log.error(e)
            return

        client_obj = mqtt.Client(
            client_id=self.client_id,
            clean_session=self.clean_session,
            reconnect_on_failure=self.reconnect_on_failure,
        )

        client_obj.on_connect = self.on_connect
        client_obj.on_disconnect = self.on_disconnect
        client_obj.on_subscribe = self.on_subscribe
        client_obj.on_message = self.on_message
        client_obj.on_log = self.on_log
        client_obj.username_pw_set(self.username, self.password)

        try:
            self.log.debug(f"[CLIENT] Connecting to broker: {self.broker}:{self.port}.")
            self.log.debug(f"[CLIENT] Client ID: {self.client_id}")
            self.log.debug(f"[CLIENT] Clean session: {self.clean_session}")
            self.log.debug(f"[CLIENT] Keep alive: {self.keep_alive}")
            self.log.debug(
                f"[CLIENT] Reconnect on failure: {self.reconnect_on_failure}"
            )
            client_obj.connect(
                host=self.broker, port=self.port, keepalive=self.keep_alive
            )
            client_obj.loop_forever()
        except KeyboardInterrupt:
            self.log.debug("[CLIENT] Keyboard interrupt detected. Exiting.")
            client_obj.loop_stop()
            client_obj.disconnect()
        except Exception as e:
            self.log.error(f"[CLIENT] Error connecting to MQTT broker: {e}")
            client_obj.loop_stop()
            client_obj.disconnect()

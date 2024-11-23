import pika
import json

class RabbitMQClient:
    def __init__(self, queue_name, host='localhost'):
        self.queue_name = queue_name
        self.host = host

        # Configurar conexión
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()

        # Declarar la cola
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def publish_message(self, message):
        # Publicar mensaje en la cola
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Hacer persistente el mensaje
            )
        )
        print(f"Mensaje enviado a la cola {self.queue_name}: {message}")

    def close_connection(self):
        self.connection.close()
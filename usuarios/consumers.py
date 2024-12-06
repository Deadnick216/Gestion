import pika

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='mi_cola', durable=True)

    def callback(ch, method, properties, body):
        print(f"Mensaje recibido: {body}")

    channel.basic_consume(queue='mi_cola', on_message_callback=callback, auto_ack=True)

    print('Esperando mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()
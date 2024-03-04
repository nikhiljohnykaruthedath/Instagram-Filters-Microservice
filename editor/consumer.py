import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from edit import apply_filter;

"""
    Connects to the MongoDB instance and listens for incoming messages on the RabbitMQ queue.

    Args:
        None

    Returns:
        None

    Raises:
        pika.exceptions.ConnectionClosed: If the connection to RabbitMQ is lost
"""
def main():
    client = MongoClient("host.minikube.internal", 27017)

    db_images = client.images
    db_edited_images = client.edited_images

    # gridfs
    fs_images = gridfs.GridFS(db_images)
    fs_edited_images = gridfs.GridFS(db_edited_images)

    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    """
        Callback function for RabbitMQ messages.

        Args:
            ch (pika.channel.Channel): The RabbitMQ channel
            method (pika.spec.Basic.Deliver): The message delivery information
            properties (pika.spec.BasicProperties): The message properties
            body (bytes): The message body

        Returns:
            None

        Raises:
            ValueError: If the message body cannot be decoded as JSON
            KeyError: If the message body does not contain the required keys
            NotImplementedError: If the message type is not supported
    """
    def callback(ch, method, properties, body):
        err = apply_filter.start(body, fs_images, fs_edited_images, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("IMAGES_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

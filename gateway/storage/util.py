import pika, json, os

"""
    Add a image file to the system and send a message to the image queue.

    Args:
        f (File): the image file to be uploaded
        fs (GridFS): the GridFS instance used to store the file
        filter_type (str): the filter type to apply to the image
        channel (pika.channel.Channel): the RabbitMQ channel used to send the message
        access (dict): the user's access credentials

    Returns:
        tuple: a tuple containing a string indicating the status of the upload and an integer indicating the HTTP status code

    Raises:
        Exception: if an error occurs during the upload or message sending
"""
def upload(f, fs, filter_type, channel, access):
    # add the file to mongodb
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error", 500

    # send the message to the image queue
    message = {
        "image_fid": str(fid),
        "edited_image_fid": None,
        "username": access["username"],
        "filter_type": filter_type,
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("IMAGES_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        # delete the file if an error occurs
        fs.delete(fid)
        return "internal server error", 500

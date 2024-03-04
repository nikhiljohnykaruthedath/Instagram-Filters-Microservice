import pika, json, tempfile, os
from bson.objectid import ObjectId

from PIL import Image
import pilgram2

"""
    This function is the entry point of the worker.
    It receives a message from the queue, applies the filter to the image,
    saves the filtered image to the file system, and publishes the message back to the queue.

    Args:
        message (str): The message received from the queue.
        fs_images (GridFS): The GridFS instance for storing images.
        fs_edited_images (GridFS): The GridFS instance for storing edited images.
        channel (pika.channel.Channel): The RabbitMQ channel used for publishing messages.

    Returns:
        str: A status message indicating whether the message was published successfully or not.
"""
def start(message, fs_images, fs_edited_images, channel):
    message = json.loads(message)

    # empty temp file
    tf = tempfile.NamedTemporaryFile()
    # image contents
    out = fs_images.get(ObjectId(message["image_fid"]))
    filter_type = message["filter_type"]
    # add images contents to empty file
    tf.write(out.read())
    # open image file
    im = Image.open(tf.name)
    tf.close()

    # get image save path
    tf_path = tempfile.gettempdir() + f"/{message['image_fid']}.jpg"
    
    # apply filter
    edit_image(im, tf_path, filter_type)
    
    # save file to mongodb
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_edited_images.put(data)
    f.close()
    os.remove(tf_path)

    message["edited_image_fid"] = str(fid)

    # publish message to rabbitmq
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("EDITED_IMAGES_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # delete file from mongo if error occurs
        fs_edited_images.delete(fid)
        return "failed to publish message"

"""
    Applies a filter to an image and saves the edited image to the specified path.

    Args:
        im (Image): The image to be edited.
        tf_path (str): The path where the edited image should be saved.
        filter_type (str): The type of filter to be applied.
"""
def edit_image(im, tf_path, filter_type):
    match filter_type:
        case "1977":
            pilgram2._1977(im).save(tf_path)
        case "aden":
            pilgram2.aden(im).save(tf_path)
        case "ashby":
            pilgram2.ashby(im).save(tf_path)
        case "amaro":
            pilgram2.amaro(im).save(tf_path)
        case "brannan":
            pilgram2.brannan(im).save(tf_path)
        case "brooklyn":
            pilgram2.brooklyn(im).save(tf_path)
        case "charmes":
            pilgram2.charmes(im).save(tf_path)
        case "clarendon":
            pilgram2.clarendon(im).save(tf_path)
        case "crema":
            pilgram2.crema(im).save(tf_path)
        case "dogpatch":
            pilgram2.dogpatch(im).save(tf_path)
        case "earlybird":
            pilgram2.earlybird(im).save(tf_path)
        case "gingham":
            pilgram2.gingham(im).save(tf_path)
        case "ginza":
            pilgram2.ginza(im).save(tf_path)
        case "hefe":
            pilgram2.hefe(im).save(tf_path)
        case "helena":
            pilgram2.helena(im).save(tf_path)
        case "hudson":
            pilgram2.hudson(im).save(tf_path)
        case "inkwell":
            pilgram2.inkwell(im).save(tf_path)
        case "juno":
            pilgram2.juno(im).save(tf_path)
        case "kelvin":
            pilgram2.kelvin(im).save(tf_path)
        case "lark":
            pilgram2.lark(im).save(tf_path)
        case "lofi":
            pilgram2.lofi(im).save(tf_path)
        case "ludwig":
            pilgram2.ludwig(im).save(tf_path)
        case "maven":
            pilgram2.maven(im).save(tf_path)
        case "mayfair":
            pilgram2.mayfair(im).save(tf_path)
        case "moon":
            pilgram2.moon(im).save(tf_path)
        case "nashville":
            pilgram2.nashville(im).save(tf_path)
        case "perpetua":
            pilgram2.perpetua(im).save(tf_path)
        case "poprocket":
            pilgram2.poprocket(im).save(tf_path)
        case "reyes":
            pilgram2.reyes(im).save(tf_path)
        case "rise":
            pilgram2.rise(im).save(tf_path)
        case "sierra":
            pilgram2.sierra(im).save(tf_path)
        case "skyline":
            pilgram2.skyline(im).save(tf_path)
        case "slumber":
            pilgram2.slumber(im).save(tf_path)
        case "stinson":
            pilgram2.stinson(im).save(tf_path)
        case "sutro":
            pilgram2.sutro(im).save(tf_path)
        case "toaster":
            pilgram2.toaster(im).save(tf_path)
        case "valencia":
            pilgram2.valencia(im).save(tf_path)
        case "walden":
            pilgram2.walden(im).save(tf_path)
        case "willow":
            pilgram2.willow(im).save(tf_path)
        case "xpro2":
            pilgram2.xpro2(im).save(tf_path)
        case _:
            pilgram2.aden(im).save(tf_path)
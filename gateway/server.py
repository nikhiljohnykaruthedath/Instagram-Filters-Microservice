import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)

mongo_images = PyMongo(server, uri="mongodb://host.minikube.internal:27017/images")

mongo_edited_images = PyMongo(server, uri="mongodb://host.minikube.internal:27017/edited_images")

fs_images = gridfs.GridFS(mongo_images.db)
fs_edited_images = gridfs.GridFS(mongo_edited_images.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

"""
    This function provides the API to handle user authentication.

    Args:
        request (Request): The incoming request.

    Returns:
        (str, int): A JSON Web Token and an error code.
"""
@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

"""
    This function provides the API to handle image uploads.

    Args:
        request (Request): The incoming request.

    Returns:
        (str, int): A message and status code.
"""
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    filter_type = request.args.get("filter_type")
    if not filter_type:
        return "filter type is required", 400
    
    # only admin users can upload images
    if access["admin"]:
        for _, f in request.files.items():
            err = util.upload(f, fs_images, filter_type, channel, access)

            if err:
                return err

        return "success!", 200
    else:
        return "not authorized", 401

"""
    This function provides the API to handle image downloads.

    Args:
        request (Request): The incoming request.

    Returns:
        (Response): The image data.
"""
@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    # only admin users can upload images
    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400

        try:
            out = fs_edited_images.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.jpg")
        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)

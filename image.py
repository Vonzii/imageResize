
import os
import tempfile

import pyrebase
from google.auth import jwt
from wand.image import Image


config = {
    "databaseURL": "https://carbide-ego-367216-default-rtdb.europe-west1.firebasedatabase.app/",
    "apiKey": "AIzaSyC2zPWX_-MEBd9qCAOQ4V7qjMWV2-fyMMw",
    "authDomain": "minireddit-c45c6.firebaseapp.com",
    "projectId": "minireddit-c45c6",
    "storageBucket": "minireddit-c45c6.appspot.com",
    "messagingSenderId": "911213281913",
    "appId": "1:911213281913:web:1ec0ceecbaf8f27dac4aa8"
}

def resize_images(data, id_token, claims):
    file_data = data

    file_name = file_data["name"]


    return __resize_image(file_name, id_token, claims)



def __resize_image(file_name, id_token, claims):
    sep = '.'
    firebase = pyrebase.initialize_app(config)
    localId = claims['user_id']
    print(f"{localId}\n")
    storage = firebase.storage()
    filename = file_name.split(sep, 1)[0]
    print(f"{filename}\n")
    _, temp_local_filename = tempfile.mkstemp()
    #path = storage.child(f"{localId}/{file_name}").get_url(id_token)
    #print(f"{path}\n")
    sep = "/"
    temp_filename = temp_local_filename.split(sep,2)[2]
    print(f"{temp_filename}\n")
    storage.child(f"{localId}/{file_name}").download(path = f"{localId}/{file_name}", filename = f"{temp_local_filename}")
    #storage.child(f"images/{file_name}").download(path = f"images/{file_name}", filename = f"{temp_local_filename}")

    print(f"Image {file_name} was downloaded to {temp_local_filename}.")

    # Blur the image using ImageMagick.
    with Image(filename=temp_local_filename) as image:
        image.format= 'jpg'
        image.resize(120, 160)
        image.save(filename=temp_local_filename)

    print(f"Image {file_name} was resized.")

    # Upload result to a second bucket, to avoid re-triggering the function.
    # You could instead re-upload it to the same bucket + tell your function
    # to ignore files marked as blurred (e.g. those with a "blurred" prefix)

    storage.child(f"{localId}/{filename}.jpg").put(temp_local_filename, id_token)
 
    #storage.delete(f"{file_name}", id_token)
    # Delete the temporary file.
    os.remove(temp_local_filename)


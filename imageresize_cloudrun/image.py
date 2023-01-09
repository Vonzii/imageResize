
import os
import tempfile

import pyrebase
from google.auth import jwt
from wand.image import Image


config = {
  "apiKey": "AIzaSyCgXzxKEx9aX8X3W5RcW12ogBtOp2mn_Fg",
  "authDomain": "carbide-ego-367216.firebaseapp.com",
  "projectId": "carbide-ego-367216",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "carbide-ego-367216.appspot.com",
  "messagingSenderId": "521778265240",
  "appId": "1:521778265240:web:a2995a7d779269ea8fa4ed",
  "measurementId": "G-NE4CH1FRYV"
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

    storage.child(f"{localId}/{filename}2.jpg").put(temp_local_filename, id_token)
 
    #storage.delete(f"{file_name}", id_token)
    # Delete the temporary file.
    os.remove(temp_local_filename)


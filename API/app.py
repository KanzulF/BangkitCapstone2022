# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json

from keras_preprocessing import image
import numpy
from tensorflow import keras


# inisiasi object flask
app = Flask(__name__)

# inisiasi object flask-restful
api = Api(app)

# inisiasi object flask-cors
CORS(app)

# database
with open('data.json') as f:
  data = json.load(f)

labels = []
for i in data:
    labels.append(i)


class MyResource(Resource):
    # metode get dan post
    def get(self):
        response = data
        return response

    def post(self):
        file = request.files['image'].read()
        # load model
        model = keras.models.load_model('Modelnew.h5')
        
        for ft in file.keys():
            pathtest = ft
            img = image.load_img(pathtest, target_size= (224, 224))
            xtest = image.img_to_array(img)
            xtest = numpy.expand_dims(xtest, axis=0)

            file_image = numpy.vstack([xtest])
            prediction_class = model.predict(file_image, batch_size=10)

            output = prediction_class[0].argmax()

            for i in data:
                if i == output:
                    response = data[i]
            break

        return response,


# setup resource
api.add_resource(MyResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=8080)
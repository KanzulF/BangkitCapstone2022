# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json
from PIL import Image
from keras_preprocessing import image
import numpy
from tensorflow import keras
from io import BytesIO


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
        # print(file)
        # load model
        model = keras.models.load_model('Modelnew.h5')

        img = Image.open(BytesIO(file))
        img = img.convert('RGB')
        img = img.resize((224, 224), Image.NEAREST)
        
        # for ft in file.keys():
        #    pathtest = ft
        #    img = image.load_img(pathtest, target_size= (224, 224))
        xtest = image.img_to_array(img)
        xtest = numpy.expand_dims(xtest, axis=0)

        file_image = numpy.vstack([xtest])
        prediction_class = model.predict(file_image, batch_size=10)

        output = prediction_class[0].argmax()

        response = {}

        response = data[list(data.keys())[output]]

        # for i in range(len(data) - 1):
            # if i == output:
                # response = data[output]

        return response,


# setup resource
api.add_resource(MyResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")

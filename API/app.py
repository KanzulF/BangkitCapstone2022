# import library
from urllib import response
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# inisiasi object flask
app = Flask(__name__)

# inisiasi object flask-restful
api = Api(app)

# inisiasi object flask-cors
CORS(app)

# database
data = {}

# membuat class Resource
class MyResource(Resource):
    # metode get dan post
    def get(self):
        # response = {"msg" : "hallo"}
        response = data
        return response

    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]

        # memasukkan data
        data["nama"] = nama
        data["umur"] = umur

        response = {"msg" : "data berhasil dimasukkan"}
        return response


# setup resource
api.add_resource(MyResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)
import codigo

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'about':'Hola mundo'}

    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}

class Codigo(Resource):
    def get(self,correo):
        return {'codigo':codigo.generarCodigo(correo)}
        #return {'you sent': num}

class Multi(Resource):
    def get(self,num):
        return {'result': num*10}

api.add_resource(HelloWorld,'/')
api.add_resource(Multi,'/multi/<int:num>')

api.add_resource(Codigo,'/codigo/<string:correo>')

if __name__ == '__main__':
    app.run(debug=True)

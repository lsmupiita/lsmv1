import dataBase

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

class HelloWorld(Resource):
    def get(self):
        return {'about':'Hola mundo'}

    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}
    
class Codigo(Resource):
    def post(self):
            parser.add_argument('correo', type=str)
            args = parser.parse_args()
            return { 'codigo':dataBase.generarCodigo(args['correo']) }

class EntrarClase(Resource):
    def post(self):
            parser.add_argument('codigo', type=str)
            args = parser.parse_args()
            return { 'mensaje':dataBase.comprobarExistencia(args['codigo']) }

class Registro(Resource):
    def post(self):
        parser.add_argument('correo',type=str)  
        args = parser.parse_args()
        return {'mensaje':dataBase.nuevoregistro(args['correo'])}          


api.add_resource(HelloWorld,'/')

api.add_resource(Codigo,'/codigo')
api.add_resource(Registro,'/registro')
api.add_resource(EntrarClase,'/entrarClase')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    #app.run(debug=True, host='10.0.0.4', port=5000)

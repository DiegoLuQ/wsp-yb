from flask import Flask, request
from config import settings as sett
import services


app = Flask(__name__)

@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return "Hola mundo"

@app.route('/webhook', methods=['GET'])
def verify_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None and token != None:
            return challenge
        else:
            return 'Token incorrecto'


    except Exception as e:
        return e, 403

@app.route('/webhook', methods=['POST'])
def recibir_mensaje():
    try:
        body = request.get_json()
        print(body)
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)
        services.administrar_chatbot(text, number, messageId, name)
        return 'EVENT_RECEIVED'
    except Exception as e:
        return e


if __name__ == '__main__':
    print(sett.token)
    app.run(host='0.0.0.0', debug=True, port=152)
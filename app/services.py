import requests
import json
import time
from config import settings as sett


def obtener_Mensaje_whatsapp(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == "button":
        text = message["button"]["text"]
    elif typeMessage == "interactive" and message['interactive']['type'] == 'list_reply':
        text = message['interactive']["list_reply"]["title"]
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no reconocido'
    return text


def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.wsp_token
        whatsapp_url = sett.wsp_url

        headers = {'Content-Type':'application/json', 'Authorization':'Bearer ' + 'EAAEYQH3aS0wBOwtU1y9qzZBieZBRiFwEgwAwhVRxuFlV9cfhLAmROEkufYVkZACS7q0UphtqcTrJDVdqhZBr3KiAerx36Mo6erq9UIZAWRHQMNbXbEsBRGHRJdyVHPZCjpfxyzxe2nSB7kccWUl5vtuxTspv85LpbFCsFONJf1WS4LFPIF9lZBQZCZBt7h9ZBilKX00hSXs0wvlXCYwsb7'}
        response = requests.post('https://graph.facebook.com/v17.0/133381839854669/messages', headers=headers, data=data)

        if response.status_code == 200:
            print("mensaje enviado")
            return 'mensaje enviado', 200
        else:
            print("mensaje no enviado", response.status_code)
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e, 403


def text_Message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data


def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []

    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data


def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data


def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data


def sticker_Message(number, sticker_id):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "sticker",
        "sticker": {
            "id": sticker_id
        }
    })
    return data


def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
        print(media_id)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id


def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data


def replyText_Message(number, messageId, text):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "context": {
            "message_id": messageId
        },
        "type": "text",
        "text": {
            "preview_url": false,
            "body": text
        }
    })
    return data

def markRead_Message(messageId):
    data =json.dumps({
        "messaging_product":"whatsapp",
        "status":"read",
        "message_id":messageId
        
    })
    return data




def administrar_chatbot(text, number, messageId, name):
    text = text.lower()
    print("mensaje del usuario: ",text)
    list_for = []
    markRead = markRead_Message(messageId)
    list_for.append(markRead)
    time.sleep(2)

    try:
        if "hola" in text:
            body = "¡Hola! 👋 Bienvenido a SF. ¿Cómo podemos ayudarte hoy?"
            # datamsg = text_Message(number, body)
            footer = "Equipo SF"
            options = ["✅ productos", "📅 agendar cita"]
            replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
            replyReaction = replyReaction_Message(number, messageId, "😁")
            list_for.append(replyReaction)
            list_for.append(replyButtonData)
            # list_for.append(datamsg)
        elif "productos" in text:
            body = "Aqui te envio las categorias de nuestros productos. ¿Cuál de estas categorias te gustaria explorar?"
            footer = "Equipo SF"
            options = ["Filtro de Aire", "Filtro dee Aceite", "Filtro de Combustible"]

            listReplyData = listReply_Message(number, options, body, footer, "sed2", messageId)
            sticker = sticker_Message(number, get_media_id('perro_traje', 'sticker'))

            list_for.append(listReplyData)
            list_for.append(sticker)
        
        elif "filtro de aire" in text:
            body = "Buenísima elección. ¿Te gustaria que te enviara un documento PDF con los filtros que tenemos?"
            footer = "Equipo SF"
            options = ["✅Si, envia el PDF", "❌No, gracias"]

            replyButtonData = buttonReply_Message(number, options, body, footer, "sed3", messageId)
            
            list_for.append(replyButtonData)

        elif "si, envia el pdf" in text:
            sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
            textMessage = text_Message(number, "Buenarda elección. En breve nos comunicaremos con usted")

            enviar_Mensaje_whatsapp(sticker)
            enviar_Mensaje_whatsapp(textMessage)
            time.sleep(3)

            document = document_Message(number, sett.doc_url, "✌ Listo", "SF-Filtros de Aire")
            enviar_Mensaje_whatsapp(document)
            time.sleep(3)

            body = "¿Te gustaría programar una reunion con uno de nuestros especialistas para discutir estos servicios mas a fondo?"
            footer = "Equipo SF"
            options = ["✅Si, agenda una reunión", "No, gracias"]

            replyButtonData = buttonReply_Message(number, options, body, footer, "sed4", messageId)

            list_for.append(replyButtonData)

        elif "sí, agenda una reunión" in text:
            body = "Estupendo. Por favor, seleccione una fecha y hora para la reunion:"
            footer = "Equipo SF"
            options = ["📅 25-09-23 09:00", "📅 25-09-23 10:00", "📅 25-09-23 11:00"]

            listReply = listReply_Message(number, options, body, footer, "sed5", messageId)

            list_for.append(listReply)
        
        elif "25-09-23 09:00" in text:
            body = "Excelente, has seleccionado la reunion para el 25 de septiembre a las 9am. Te enviare un recordatorio un día antes. ¿Necesitas ayuda con algo mas hoy?"
            footer = "Equipo SF"
            options = ["✅Si, por favor", "No, gracias"]

            buttonReply = buttonReply_Message(number, options, body, footer, "sed6", messageId)
            list_for.append(buttonReply)
        elif "no, gracias" in text:
            msg = "Perfect! No dudes en contactarnos si tienes más preguntas. Recuerda que tambien ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😁"
            textMessage = text_Message(number, msg)
            list_for.append(textMessage)
        else:
            body = "Hola. ¿Quieres que te ayude con alguna de estas opciones?"
            footer = "Equipo SF"
            options = ["✅ productos", "📅 agendar cita"]
            list_for.append(body)
            replyButtonData = buttonReply_Message(number, options, body, footer, "sed7", messageId)
            list_for.append(replyButtonData)
        print(len(list_for))
        for item in list_for:
            enviar_Mensaje_whatsapp(item)

    except Exception as e:
        raise e
    
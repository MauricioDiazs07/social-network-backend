from flask import Blueprint, jsonify, request
from src.models.ChatModel import ChatModel
from src.models.entities.chat.Chat import Chat

main = Blueprint('chat_blueprint', __name__)

@main.route('/send', methods = ['POST'])
def send_message():
    try:
        sender_id = request.json['sender_id']
        receiver_id = request.json['receiver_id']
        text = request.json['text']
        chat = Chat(sender_id,receiver_id,text)
        affected_row = ChatModel.create_chat(chat)

        if affected_row > 0:
            return jsonify({
                'message': 'Mensaje enviado'
            })
        else:
            return jsonify({
                'message': 'Error al mandar el mensaje'
            }), 500
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/', methods = ['POST'])
def list_messages():
    try:
        sender_id = request.json['sender_id']
        receiver_id = request.json['receiver_id']
        chats = ChatModel.list_chats(sender_id, receiver_id)
        print(chats)
        return jsonify({
            "chats": chats
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/show', methods = ['POST'])
def show_chats():
    try:
        sender_id = request.json['sender_id']
        chats = ChatModel.show_chats(sender_id)

        persons = []
        message= []
        send = []
        for chat in chats:
            print(chat)
            if chat['sender_id'] != sender_id:
                if chat['sender_id'] not in persons:
                    persons.append(chat['sender_id'])
                    message.append(chat['message'])
                    send.append(False)
            else:
                if chat['receiver_id'] not in persons:
                    persons.append(chat['receiver_id'])
                    message.append(chat['message'])
                    send.append(True)

        show_chats = []
        for i, person in enumerate(persons):
            for chat in chats:
                if person == chat['sender_id']:
                    chat['message'] = message[i]
                    chat['send'] = send[i]
                    show_chats.append(chat)
                    break
        return jsonify({
            "active_chats": show_chats
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
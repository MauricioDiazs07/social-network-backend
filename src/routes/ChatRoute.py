from flask import Blueprint, jsonify, request
from src.models.ChatModel import ChatModel
from src.models.entities.chat.Chat import Chat
from src.models.ProfileModel import ProfileModel

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
        active_chats = []
        for chat in chats:
            if chat['sender_id'] != sender_id:
                if chat['sender_id'] not in persons:
                    data = {
                        'name': chat['name'],
                        'receiver_id': chat['sender_id'],
                        'message': chat['message'],
                        'time': chat['time'],
                        'imageUrl': chat['imageUrl'],
                        'pending': 0,
                        'send': False
                    }
                    active_chats.append(data)
                    persons.append(chat['sender_id'])
            else:
                if chat['receiver_id'] not in persons:
                    data = ProfileModel.get_profile_data(chat['receiver_id'])
                    print('data', data)
                    data = {
                        'name': data['name'],
                        'receiver_id': chat['receiver_id'],
                        'message': chat['message'],
                        'time': chat['time'],
                        'imageUrl': data['profile_photo'],
                        'pending': 0,
                        'send': True
                    }
                    active_chats.append(data)
                    persons.append(chat['receiver_id'])
            
        return jsonify({
            "active_chats": active_chats
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
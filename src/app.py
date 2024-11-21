from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from flask_cors import CORS

# Criar uma instância do Flask
app = Flask(__name__)
CORS(app)  # Adiciona CORS ao app Flask
socketio = SocketIO(app, cors_allowed_origins="*")  # Permite qualquer origem

# Lista para armazenar usuários conectados
connected_users = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    username = request.args.get('username', 'Anonimo')  # Atribui "Anonimo" se não houver nome
    connected_users.append(username)  # Adiciona o usuário à lista
    print(f"Usuário {username} se conectou!")
    # Envia a lista de usuários conectados para todos os clientes
    send({'type': 'user_list', 'users': connected_users}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = request.args.get('username', 'Anonimo')  # Garantir que o usuário seja "Anonimo" se não houver nome
    if username in connected_users:
        connected_users.remove(username)  # Remove o usuário da lista
    print(f"Usuário {username} se desconectou!")
    # Enviar lista atualizada para todos os clientes conectados
    send({'type': 'user_list', 'users': connected_users}, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    print(f'Mensagem recebida de {msg["username"]}: {msg["message"]}')
    # Envia a mensagem para todos os clientes conectados
    send({
        'username': msg['username'],
        'message': msg['message']
    }, broadcast=True)

@socketio.on('next_user')
def handle_next_user():
    send("Troca de usuário", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

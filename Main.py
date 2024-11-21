from src.app import app, socketio

if __name__ == '__main__':
    # Rodar o app com SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)

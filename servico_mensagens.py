from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta_super_segura'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def conectar_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="db_autenticacao"
    )

@app.route('/historico/<destinatario>', methods=['GET'])
def obter_historico(destinatario):
    remetente = request.args.get('remetente')
    try:
        conexao = conectar_db()
        cursor = conexao.cursor(dictionary=True)
        
        if destinatario == 'grupo':
            sql = "SELECT remetente, destinatario, mensagem, DATE_FORMAT(data_envio, '%H:%i') as hora FROM mensagens WHERE destinatario = 'grupo' ORDER BY data_envio ASC"
            cursor.execute(sql)
        else:
            sql = "SELECT remetente, destinatario, mensagem, DATE_FORMAT(data_envio, '%H:%i') as hora FROM mensagens WHERE (remetente = %s AND destinatario = %s) OR (remetente = %s AND destinatario = %s) ORDER BY data_envio ASC"
            cursor.execute(sql, (remetente, destinatario, destinatario, remetente))
            
        resultado = cursor.fetchall()
        return jsonify(resultado), 200
    except mysql.connector.Error as err:
        return jsonify({"erro": str(err)}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

@socketio.on('conectar_usuario')
def handle_conectar(dados):
    usuario = dados['usuario']
    join_room(usuario) 
    print(f"Usuário {usuario} conectou e entrou na sala privada.")
    
    # NOVO: Avisa a todos que estão online que esse usuário entrou
    emit('novo_usuario_online', {'usuario': usuario}, broadcast=True)

@socketio.on('enviar_mensagem')
def handle_mensagem(dados):
    remetente = dados['remetente']
    destinatario = dados.get('destinatario', 'grupo')
    mensagem = dados['mensagem']

    # 1. Salva no Banco de Dados
    try:
        conexao = conectar_db()
        cursor = conexao.cursor()
        sql = "INSERT INTO mensagens (remetente, destinatario, mensagem) VALUES (%s, %s, %s)"
        cursor.execute(sql, (remetente, destinatario, mensagem))
        conexao.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao salvar: {err}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

    # 2. Transmissão Segura
    dados_resposta = {'remetente': remetente, 'mensagem': mensagem, 'destinatario': destinatario}
    
    if destinatario == 'grupo':
        # Envia para todos
        emit('receber_mensagem', dados_resposta, broadcast=True)
    else:
        # Envia EXCLUSIVAMENTE para a sala do destinatário e para a sala do remetente
        emit('receber_mensagem', dados_resposta, room=destinatario)
        emit('receber_mensagem', dados_resposta, room=remetente)

if __name__ == '__main__':
    socketio.run(app, port=8001, debug=True)
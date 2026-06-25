from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuração de conexão com o banco de dados do WAMP
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Usuário padrão do WAMP
        password="",        # Senha padrão do WAMP (vazia)
        database="db_autenticacao"
    )

@app.route('/registrar', methods=['POST'])
def registrar():
    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')

    if not usuario or not senha:
        return jsonify({"erro": "Usuario e senha sao obrigatorios!"}), 400

    try:
        conexao = conectar_db()
        cursor = conexao.cursor()
        
        # Insere os dados na tabela que você criou
        sql = "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)"
        valores = (usuario, senha)
        cursor.execute(sql, valores)
        conexao.commit()
        
        return jsonify({"mensagem": "Usuario registrado com sucesso!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"erro": f"Erro no banco de dados: {err}"}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')

    try:
        conexao = conectar_db()
        cursor = conexao.cursor(dictionary=True)
        
        # Verifica se o usuário e a senha existem e batem
        sql = "SELECT * FROM usuarios WHERE usuario = %s AND senha = %s"
        valores = (usuario, senha)
        cursor.execute(sql, valores)
        resultado = cursor.fetchone()

        if resultado:
            return jsonify({"mensagem": "Login aprovado!", "usuario": resultado['usuario']}), 200
        else:
            return jsonify({"erro": "Usuario ou senha incorretos!"}), 401
    except mysql.connector.Error as err:
        return jsonify({"erro": f"Erro no banco de dados: {err}"}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        conexao = conectar_db()
        cursor = conexao.cursor(dictionary=True)
        # Busca apenas o nome do usuário, sem a senha!
        cursor.execute("SELECT usuario FROM usuarios")
        resultado = cursor.fetchall()
        return jsonify(resultado), 200
    except mysql.connector.Error as err:
        return jsonify({"erro": f"Erro no banco: {err}"}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

if __name__ == '__main__':
    # Rodando o serviço de autenticação na porta 8000
    app.run(port=8000, debug=True)
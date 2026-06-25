# 💬 Sistema de Chat Distribuído

Este repositório contém a implementação de um Sistema de Chat Distribuído, desenvolvido como Trabalho Prático Final da disciplina de Sistemas Distribuídos do CEFET-MG. O sistema é uma plataforma de comunicação em tempo real baseada em uma arquitetura de microsserviços.

## 👩‍💻 Autora

Ana Clara Cunha Lopes - Estudante de Engenharia de Computação - CEFET-MG

## 🚀 Funcionalidades

- **Comunicação em Tempo Real:** Troca de mensagens instantâneas utilizando WebSockets de baixa latência.
- **Tipos de Chat:** Suporte nativo a conversas privadas (1:1) e para múltiplos destinatários no Grupo Geral (1:N).
- **Microsserviços Independentes:** Serviços separados para Autenticação e Mensagens, garantindo alta disponibilidade.
- **Persistência de Dados:** Histórico de conversas e credenciais de usuários salvos em banco de dados relacional.
- **Interface Responsiva:** Front-end simples, moderno e intuitivo, que se comunica de forma assíncrona com as APIs.

## 🛠️ Arquitetura e Tecnologias Utilizadas

- **Front-end:** HTML5, CSS3, JavaScript Vanilla e Socket.IO-client.
- **Back-end (Microsserviços):** Python 3 com as bibliotecas Flask e Flask-SocketIO.
- **Banco de Dados:** MySQL (utilizando WAMP Server no ambiente de desenvolvimento).
- **Comunicação:** REST (para login/registro) e WebSockets (para o chat).

## 📋 Pré-requisitos

Para rodar este projeto localmente, você precisará ter instalado em sua máquina:
- [Python 3.x](https://www.python.org/downloads/)
- Um servidor MySQL local (como [WAMP Server](https://www.wampserver.com/en/) ou XAMPP)

## ⚙️ Instalação e Configuração

### 1. Banco de Dados
Inicie o seu servidor MySQL e crie o banco de dados e as tabelas executando o script SQL abaixo (pode ser executado via phpMyAdmin):

```sql
CREATE DATABASE db_autenticacao;
USE db_autenticacao;

-- Tabela de Usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Tabela de Mensagens
CREATE TABLE mensagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    remetente VARCHAR(50) NOT NULL,
    destinatario VARCHAR(50) NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Dependências do Python
Abra o terminal na pasta do projeto e instale as bibliotecas necessárias utilizando o pip:

```pip install flask flask-cors flask-socketio eventlet mysql-connector-python```

## ▶️ Como Executar o Projeto

Como o sistema é distribuído em microsserviços, você precisará rodar cada serviço em um terminal independente.

### Terminal 1 - Serviço de Autenticação:
```python servico_autenticacao.py```

### Terminal 2 - Serviço de Mensagens (WebSockets):
```python servico_mensagens.py```

### Front-end (Cliente):
Com os dois terminais rodando, basta abrir o arquivo index.html diretamente no seu navegador web preferido para acessar o sistema.

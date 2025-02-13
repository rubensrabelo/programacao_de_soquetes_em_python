# Trabalho de Redes - Sistema de Gerenciamento de Contas  

Este é um sistema de gerenciamento de contas desenvolvido para a disciplina de Redes. O projeto consiste em um servidor e um cliente, com suporte para autenticação e múltiplos clientes simultâneos.  

## 🚀 Tecnologias Utilizadas  
- **Linguagem**: Python 🐍  
- **Armazenamento**: Arquivos CSV para guardar as informações das contas e usuários  
- **Bibliotecas**:  
  - [bcrypt](https://pypi.org/project/bcrypt/) - Hash de senhas  
  - [numpy](https://numpy.org/) - Operações matemáticas  
  - [pandas](https://pandas.pydata.org/) - Manipulação de dados  
  - [python-dateutil](https://dateutil.readthedocs.io/en/stable/) - Gerenciamento de datas  
  - [pytz](https://pypi.org/project/pytz/) - Fuso horário  
  - [six](https://pypi.org/project/six/) - Compatibilidade entre versões do Python  
  - [tzdata](https://pypi.org/project/tzdata/) - Banco de dados de fusos horários  

## 📌 Funcionalidades  
- Autenticação de usuários  
- Gerenciamento de contas (adicionar, editar e excluir)  
- Simulação de financiamento/parcelamento com juros seguindo regras de mercado  
- Descoberta automática do servidor na rede local  

## 📂 Estrutura de Pastas  

```bash
📂 SistemaGerenciamentoContas/
├── 📂 server/
│   ├── server.py  # Servidor e descoberta automática do IP  
│   ├── 📂 services/
│   │   ├── financial_manager.py  # Gerencia contas e simulação de financiamento  
│   │   ├── handle_client.py  # Lida com requisições do cliente  
│   │   ├── user_manager.py  # Criação e autenticação de usuários  
│
├── 📂 client/
│   ├── client.py  # Lida com requisições do cliente e descoberta do servidor  
│   ├── 📂 screen/
│   │   ├── display.py  # Interface para exibição e entrada de dados  
│
├── requirements.txt  # Lista de dependências do projeto
```

## Instalação

Siga os passos abaixo para configurar o projeto:

### 1. Clone o repositório

Clone o repositório do projeto no seu diretório local:

```bash
git clone https://github.com/rubensrabelo/programacao_de_soquetes_em_python.git
```


Para rodar a aplicação localmente, siga os passos abaixo:

### 1. Criar o Ambiente Virtual

Ative o ambiente virtual para isolar as dependências do projeto. No terminal, execute o seguinte comando:

```bash
python -m venv venv
```

### 2. Ativar o Ambiente Virtual

Ative o ambiente virtual para isolar as dependências do projeto. No terminal, execute o seguinte comando:

```bash
source .venv/bin/activate  # Comando para o Linux
```

### 3. Instalar as Dependências
Com o ambiente virtual ativado, instale as dependências listadas no arquivo requirements.txt, utilizando o gerenciador de dependências `pip`:

```bash
pip install -r requirements.txt
```
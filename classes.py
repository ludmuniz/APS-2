import base64
from cryptography.fernet import Fernet
import pickle
import os

def gerar_chave():
    return Fernet.generate_key()

def criptografar_mensagem(mensagem, chave):
    f = Fernet(chave)
    return f.encrypt(mensagem.encode())

# Função para descriptografar uma mensagem
def descriptografar_mensagem(mensagem_encriptada, chave):
    f = Fernet(chave)
    return f.decrypt(mensagem_encriptada).decode()

class Usuario:
    """Classe base para usuários do sistema."""
    def __init__(self, nome, identificacao, senha):
        self.nome = nome
        self.identificacao = identificacao
        self.senha = senha  # Armazena a senha

class Tripulante(Usuario):
    """Classe representando um tripulante."""
    def acessar_menu(self):
        print(f"Bem-vindo, Tripulante {self.nome}")
        while True:
            if not self.menu_tripulante():
                break

    def menu_tripulante(self):
        print("\nMenu Tripulante:")
        print("1. Ver informações")
        print("2. Navio autorizado para viagem")
        print("3. Navio não autorizado para viagem")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print(f"Tripulante: {self.nome}, Identificação: {self.identificacao}")
        elif opcao == "2":
            print("O navio está autorizado para viagem.")
        elif opcao == "3":
            print("O navio não está autorizado para viagem.")
        elif opcao == "4":
            return False
        else:
            print("Opção inválida.")
        return True


class Inspetor(Usuario):
    """Classe representando um inspetor."""

    def __init__(self, nome, identificacao, autorizado, senha, trajado=False):
        super().__init__(nome, identificacao, senha)
        self.autorizado = autorizado
        self.trajado = trajado
        self.mensagens = []  # Lista para armazenar mensagens recebidas

    def acessar_menu(self, lista_inspetores, status_navio):
        print(f"Bem-vindo, Inspetor {self.nome}")
        while True:
            if not self.menu_inspetor(lista_inspetores, status_navio):
                break

    def menu_inspetor(self, lista_inspetores, status_navio):
        print("\nMenu Inspetor:")
        print("1. Verificar roupas de proteção")
        print("2. Verificar acesso ao navio")
        print("3. Ver status do navio (Apenas se trajado)")
        print("4. Enviar mensagem criptografada")
        print("5. Ver mensagens")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            self.trajado = self.verificar_roupas_de_protecao()
        elif opcao == "2":
            self.verificar_acesso_navio()
        elif opcao == "3":
            self.verificar_status_navio(status_navio)
        elif opcao == "4":
            self.enviar_mensagem(lista_inspetores)
        elif opcao == "5":
            self.ver_mensagens()  # Chama o método para ver mensagens
        elif opcao == "6":
            print("Saindo do menu.")
            return False
        else:
            print("Opção inválida.")
        return True

    def verificar_roupas_de_protecao(self):
        resposta = input("Você está usando roupas de proteção adequadas (s/n)? ").lower()
        if resposta == 's':
            print(f"Inspetor {self.nome} está trajado corretamente.")
            return True
        else:
            print(f"Inspetor {self.nome} não está trajado corretamente.")
            return False

    def verificar_acesso_navio(self):
        status = "autorizado" if self.autorizado else "não autorizado"
        print(f"Inspetor {self.nome} está {status} a acessar o navio.")

    def verificar_status_navio(self, status_navio):
        if self.trajado:
            print(f"Status do navio: {status_navio}")
        else:
            print("Acesso negado. Você precisa estar trajado com roupas de proteção para acessar o status do navio.")

    def enviar_mensagem(self, lista_inspetores):
        mensagem = input("Digite a mensagem a ser enviada: ")
        chave = gerar_chave()  # Gerar chave para cada mensagem
        mensagem_encriptada = criptografar_mensagem(mensagem, chave)

        destinatario_id = input("Informe a identificação do inspetor destinatário: ")
        for inspetor in lista_inspetores:
            if inspetor.identificacao == destinatario_id:
                inspetor.receber_mensagem(mensagem_encriptada, chave)
                print("Mensagem enviada com sucesso!")
                return
        print("Destinatário não encontrado.")

    def receber_mensagem(self, mensagem_encriptada, chave):
        self.mensagens.append((mensagem_encriptada, chave))
        print("Mensagem criptografada recebida.")

    def ver_mensagens(self):
        if not self.mensagens:
            print("Nenhuma mensagem recebida.")
        else:
            print("Mensagens recebidas:")
            for mensagem_encriptada, chave in self.mensagens:
                mensagem = descriptografar_mensagem(mensagem_encriptada, chave)
                print(f"- {mensagem}")

    def salvar_dados(lista, nome_arquivo):
        with open(nome_arquivo, 'wb') as arquivo:
            pickle.dump(lista, arquivo)

class Admin(Usuario):
    """Classe representando um administrador."""

    def acessar_menu(self, lista_inspetores, lista_tripulantes):
        print(f"Bem-vindo, Admin {self.nome}")
        while True:
            if not self.menu_admin(lista_inspetores, lista_tripulantes):
                print("Saindo do menu admin.")  # Para verificar a saída do loop
                break

    def menu_admin(self, lista_inspetores, lista_tripulantes):
        print("\nMenu Admin:")
        print("1. Criar inspetor")
        print("2. Listar inspetores")
        print("3. Editar inspetor")
        print("4. Excluir inspetor")
        print("5. Criar tripulante")
        print("6. Listar tripulantes")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_inspetor(lista_inspetores)
        elif opcao == "2":
            listar_inspetores(lista_inspetores)
        elif opcao == "3":
            editar_inspetor(lista_inspetores)
        elif opcao == "4":
            excluir_inspetor(lista_inspetores)
        elif opcao == "5":
            criar_tripulante(lista_tripulantes)
        elif opcao == "6":
            listar_tripulantes(lista_tripulantes)
        elif opcao == "7":
            return False
        else:
            print("Opção inválida.")
        return True

# Funções CRUD para inspetores
def criar_inspetor(lista_inspetores):
    nome = input("Nome do inspetor: ")
    identificacao = input("Identificação do inspetor: ")
    autorizado = input("Autorizado (s/n)? ").lower() == 's'
    senha = input("Senha do inspetor: ")

    inspetor = Inspetor(nome, identificacao, autorizado, senha)
    lista_inspetores.append(inspetor)
    print(f"Inspetor {nome} criado com sucesso!")
    salvar_dados(lista_inspetores, 'inspetores.pkl')

def listar_inspetores(lista_inspetores):
    if not lista_inspetores:
        print("Nenhum inspetor cadastrado.")
    else:
        for i, inspetor in enumerate(lista_inspetores, 1):
            status = "Autorizado" if inspetor.autorizado else "Não autorizado"
            print(f"{i}. {inspetor.nome} - {inspetor.identificacao} ({status})")

def editar_inspetor(lista_inspetores):
    listar_inspetores(lista_inspetores)
    try:
        indice = int(input("Selecione o inspetor pelo número: ")) - 1
        if 0 <= indice < len(lista_inspetores):
            inspetor = lista_inspetores[indice]
            inspetor.nome = input(f"Nome atual: {inspetor.nome}. Novo nome (ou Enter para manter): ") or inspetor.nome
            inspetor.identificacao = input(
                f"Identificação atual: {inspetor.identificacao}. Nova (ou Enter para manter): ") or inspetor.identificacao
            autorizado = input(f"Autorizado atualmente ({'s' if inspetor.autorizado else 'n'}). Alterar? (s/n): ").lower()
            inspetor.autorizado = autorizado == 's'
            print("Inspetor atualizado com sucesso!")
            salvar_dados(lista_inspetores, 'inspetores.pkl')
        else:
            print("Inspetor não encontrado.")
    except ValueError:
        print("Por favor, insira um número válido.")

def excluir_inspetor(lista_inspetores):
    listar_inspetores(lista_inspetores)
    try:
        indice = int(input("Selecione o inspetor pelo número para excluir: ")) - 1
        if 0 <= indice < len(lista_inspetores):
            excluido = lista_inspetores.pop(indice)
            print(f"Inspetor {excluido.nome} excluído com sucesso!")
            salvar_dados(lista_inspetores, 'inspetores.pkl')
        else:
            print("Inspetor não encontrado.")
    except ValueError:
        print("Por favor, insira um número válido.")

# Funções CRUD para tripulantes
def criar_tripulante(lista_tripulantes):
    nome = input("Nome do tripulante: ")
    identificacao = input("Identificação do tripulante: ")
    senha = input("Senha do tripulante: ")
    tripulante = Tripulante(nome, identificacao, senha)
    lista_tripulantes.append(tripulante)
    print(f"Tripulante {nome} criado com sucesso!")
    salvar_dados(lista_tripulantes, 'tripulantes.pkl')

def listar_tripulantes(lista_tripulantes):
    if not lista_tripulantes:
        print("Nenhum tripulante cadastrado.")
    else:
        for i, tripulante in enumerate(lista_tripulantes, 1):
            print(f"{i}. {tripulante.nome} - {tripulante.identificacao}")

def salvar_dados(lista, nome_arquivo):
    with open(nome_arquivo, 'wb') as arquivo:
        pickle.dump(lista, arquivo)

def carregar_dados(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'rb') as arquivo:
            return pickle.load(arquivo)
    return []
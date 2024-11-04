import base64
from cryptography.fernet import Fernet
import pickle
import os

# Funções de criptografia e geração de chave
def gerar_chave():
    return Fernet.generate_key()

def criptografar_mensagem(mensagem, chave):
    f = Fernet(chave)
    return f.encrypt(mensagem.encode())

def descriptografar_mensagem(mensagem_encriptada, chave):
    f = Fernet(chave)
    return f.decrypt(mensagem_encriptada).decode()

# Classe base para usuários
class Usuario:
    def __init__(self, nome, identificacao, senha):
        self.nome = nome
        self.identificacao = identificacao
        self.senha = senha

# Classe para informações do Navio
class Navio:
    def __init__(self, nome, lixo, eh_toxico, distancia_costa):
        self.nome = nome
        self.lixo = lixo
        self.eh_toxico = eh_toxico
        self.distancia_costa = distancia_costa

    def mostrar_informacoes(self):
        print(f"\nNome do Navio: {self.nome}")
        print(f"Tipo de Lixo: {self.lixo}")
        if self.eh_toxico:
            print("Atenção: Lixo Tóxico - Exigido uso de roupas específicas.")
        print(f"Distância da Costa: {self.distancia_costa} km")
        
        if self.distancia_costa < 50:
            print("Atenção: Contato somente via helicópteros.")
            if self.distancia_costa < 10:
                print("Isolamento necessário em um raio de 10 km.")
            else:
                print("Isolamento adequado não confirmado.")
        else:
            print("Distância segura da costa.")

# Classe para Tripulante
class Tripulante(Usuario):
    def acessar_menu(self):
        print(f"\nBem-vindo, Tripulante {self.nome}")
        while True:
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
                break
            else:
                print("Opção inválida.")

# Classe para Inspetor
class Inspetor(Usuario):
    def __init__(self, nome, identificacao, autorizado, senha):
        super().__init__(nome, identificacao, senha)
        self.autorizado = autorizado
        self.trajado = False
        self.mensagens = []

    def acessar_menu(self, lista_inspetores, status_navio):
        print(f"\nBem-vindo, Inspetor {self.nome}")
        while True:
            print("\nMenu Inspetor:")
            print("1. Verificar roupas de proteção")
            print("2. Verificar acesso ao navio")
            print("3. Ver status do navio")
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
                self.ver_mensagens()
            elif opcao == "6":
                break
            else:
                print("Opção inválida.")

    def verificar_roupas_de_protecao(self):
        resposta = input("Você está usando roupas de proteção (s/n)? ").lower()
        self.trajado = resposta == 's'
        return self.trajado

    def verificar_acesso_navio(self):
        status = "autorizado" if self.autorizado else "não autorizado"
        print(f"Inspetor {self.nome} está {status} para acessar o navio.")

    def verificar_status_navio(self, status_navio):
        if self.trajado:
            print(f"Status do navio: {status_navio}")
        else:
            print("Acesso negado. Utilize roupas de proteção para ver o status.")

    def enviar_mensagem(self, lista_inspetores):
        mensagem = input("Digite a mensagem: ")
        chave = gerar_chave()
        mensagem_encriptada = criptografar_mensagem(mensagem, chave)

        destinatario_id = input("Informe a identificação do destinatário: ")
        destinatario = next((i for i in lista_inspetores if i.identificacao == destinatario_id), None)
        if destinatario:
            destinatario.receber_mensagem(mensagem_encriptada, chave)
            print("Mensagem enviada com sucesso.")
        else:
            print("Destinatário não encontrado.")

    def receber_mensagem(self, mensagem_encriptada, chave):
        self.mensagens.append((mensagem_encriptada, chave))
        print("Mensagem recebida.")

    def ver_mensagens(self):
        if not self.mensagens:
            print("Nenhuma mensagem recebida.")
        else:
            print("Mensagens recebidas:")
            for msg, chave in self.mensagens:
                print(f"- {descriptografar_mensagem(msg, chave)}")

# Classe para Administrador
class Admin(Usuario):
    def acessar_menu(self, lista_inspetores, lista_tripulantes, lista_navios):
        print(f"\nBem-vindo, Admin {self.nome}")
        while True:
            print("\nMenu Admin:")
            print("1. Criar inspetor")
            print("2. Listar inspetores")
            print("3. Editar inspetor")
            print("4. Excluir inspetor")
            print("5. Criar tripulante")
            print("6. Listar tripulantes")
            print("7. Cadastrar informações do navio")
            print("8. Mostrar informações do navio")
            print("9. Sair")
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
                cadastrar_navio(lista_navios)
            elif opcao == "8":
                mostrar_informacoes_navio(lista_navios)
            elif opcao == "9":
                break
            else:
                print("Opção inválida.")

# Funções para Navio
def cadastrar_navio(lista_navios):
    nome = input("Nome do Navio: ")
    lixo = input("Tipo de lixo que está levando como (chumbo, uranio, mercurio): ")
    eh_toxico = lixo.lower() in ["chumbo", "uranio", "mercurio"]
    if eh_toxico:
        print("Atenção: Lixo tóxico - Exigido uso de roupas específicas.")
    distancia_costa = float(input("Distância do navio até a costa (km): "))

    navio = Navio(nome, lixo, eh_toxico, distancia_costa)
    lista_navios.append(navio)
    print("Informações do navio cadastradas com sucesso.")

def mostrar_informacoes_navio(lista_navios):
    if not lista_navios:
        print("Nenhuma informação de navio cadastrada.")
    else:
        for navio in lista_navios:
            navio.mostrar_informacoes()

# Funções CRUD para Inspetores e Tripulantes
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, 'rb') as f:
            return pickle.load(f)
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, 'wb') as f:
        pickle.dump(dados, f)

def criar_inspetor(lista_inspetores):
    nome = input("Nome do Inspetor: ")
    identificacao = input("Identificação: ")
    senha = input("Senha: ")
    autorizado = input("Está autorizado (s/n)? ").lower() == 's'
    inspetor = Inspetor(nome, identificacao, autorizado, senha)
    lista_inspetores.append(inspetor)
    salvar_dados('inspetores.pkl', lista_inspetores)
    print("Inspetor criado com sucesso.")

def listar_inspetores(lista_inspetores):
    if not lista_inspetores:
        print("Nenhum inspetor cadastrado.")
    else:
        print("Inspetores cadastrados:")
        for inspetor in lista_inspetores:
            print(f"{inspetor.nome} - {inspetor.identificacao}")

def editar_inspetor(lista_inspetores):
    identificacao = input("Identificação do inspetor a ser editado: ")
    inspetor = next((i for i in lista_inspetores if i.identificacao == identificacao), None)
    if inspetor:
        novo_nome = input("Novo nome (deixe em branco para não alterar): ")
        if novo_nome:
            inspetor.nome = novo_nome
        nova_senha = input("Nova senha (deixe em branco para não alterar): ")
        if nova_senha:
            inspetor.senha = nova_senha
        novo_autorizado = input("Novo status de autorização (s/n, deixe em branco para não alterar): ")
        if novo_autorizado:
            inspetor.autorizado = novo_autorizado.lower() == 's'
        salvar_dados('inspetores.pkl', lista_inspetores)
        print("Inspetor editado com sucesso.")
    else:
        print("Inspetor não encontrado.")

def excluir_inspetor(lista_inspetores):
    identificacao = input("Identificação do inspetor a ser excluído: ")
    inspetor = next((i for i in lista_inspetores if i.identificacao == identificacao), None)
    if inspetor:
        lista_inspetores.remove(inspetor)
        salvar_dados('inspetores.pkl', lista_inspetores)
        print("Inspetor excluído com sucesso.")
    else:
        print("Inspetor não encontrado.")

def criar_tripulante(lista_tripulantes):
    nome = input("Nome do Tripulante: ")
    identificacao = input("Identificação: ")
    senha = input("Senha: ")
    tripulante = Tripulante(nome, identificacao, senha)
    lista_tripulantes.append(tripulante)
    salvar_dados('tripulantes.pkl', lista_tripulantes)
    print("Tripulante criado com sucesso.")

def listar_tripulantes(lista_tripulantes):
    if not lista_tripulantes:
        print("Nenhum tripulante cadastrado.")
    else:
        print("Tripulantes cadastrados:")
        for tripulante in lista_tripulantes:
            print(f"{tripulante.nome} - {tripulante.identificacao}")

# Função principal
def main():
    lista_inspetores = carregar_dados('inspetores.pkl')
    lista_tripulantes = carregar_dados('tripulantes.pkl')
    lista_navios = []
    admin = Admin("Admin", "admin", "senha123")

    while True:
        print("\nLogin do Sistema")
        identificacao = input("Identificação: ")
        senha = input("Senha: ")

        if identificacao == admin.identificacao and senha == admin.senha:
            admin.acessar_menu(lista_inspetores, lista_tripulantes, lista_navios)
        else:
            usuario = next((u for u in lista_inspetores + lista_tripulantes if u.identificacao == identificacao and u.senha == senha), None)
            if usuario:
                if isinstance(usuario, Inspetor):
                    usuario.acessar_menu(lista_inspetores, "Autorizado para viagem")
                elif isinstance(usuario, Tripulante):
                    usuario.acessar_menu()
            else:
                print("Usuário ou senha inválidos.")

if __name__ == "__main__":
    main()

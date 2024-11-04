import base64
from cryptography.fernet import Fernet
import pickle
import os

from classes import Admin, Inspetor, Tripulante, carregar_dados 



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

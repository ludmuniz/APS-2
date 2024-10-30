from classes import carregar_dados, Admin


def main():
    lista_inspetores = carregar_dados('inspetores.pkl')
    lista_tripulantes = carregar_dados('tripulantes.pkl')

    while True:
        print("\nMenu Principal:")
        print("1. Acessar como Admin")
        print("2. Acessar como Inspetor")
        print("3. Acessar como Tripulante")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            admin = Admin("Admin", "admin", "senha_admin")  # Admin fixo para teste
            admin.acessar_menu(lista_inspetores, lista_tripulantes)
        elif opcao == "2":
            identificacao = input("Digite sua identificação: ")
            senha = input("Digite sua senha: ")
            inspetor = next((i for i in lista_inspetores if i.identificacao == identificacao and i.senha == senha), None)
            if inspetor:
                inspetor.acessar_menu(lista_inspetores, "Navio está a caminho.")
            else:
                print("Identificação ou senha inválidos.")
        elif opcao == "3":
            identificacao = input("Digite sua identificação: ")
            senha = input("Digite sua senha: ")
            tripulante = next((t for t in lista_tripulantes if t.identificacao == identificacao and t.senha == senha), None)
            if tripulante:
                tripulante.acessar_menu()
            else:
                print("Identificação ou senha inválidos.")
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
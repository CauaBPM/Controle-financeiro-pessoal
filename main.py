from database import criar_banco
from operations import (
    adicionar_transacao,
    listar_transacoes,
    calcular_saldo,
    remover_transacao,
    relatorio_categorias,
    exportar_csv,
    resumo_financeiro,
    filtrar_transacoes,
    editar_transacao,
)
from reports import gerar_grafico_categorias
from colorama import init, Fore, Style

init(autoreset=True) 

criar_banco()

while True:
    print(Fore.RED + "\n╔══════════════════════════════╗")
    print(Fore.WHITE + "║     CONTROLE FINANCEIRO      ║")
    print(Fore.RED + "╚══════════════════════════════╝")
    print(Fore.BLUE + "  1 - Adicionar transação")
    print(Fore.BLUE + "  2 - Listar transações")
    print(Fore.BLUE + "  3 - Mostrar saldo")
    print(Fore.BLUE + "  4 - Remover transação")
    print(Fore.BLUE + "  5 - Relatório por categoria")
    print(Fore.BLUE + "  6 - Exportar CSV")
    print(Fore.BLUE + "  7 - Gerar gráfico")
    print(Fore.BLUE + "  8 - Resumo financeiro")
    print(Fore.BLUE + "  9 - Filtrar transações")
    print(Fore.BLUE + "  10 - Editar transação")
    print(Fore.BLUE + "  11 - Metas de gastos")   
    print(Fore.BLUE + "  12 - Sair")   
    opcao = input(Fore.WHITE + "\nEscolha uma opção: ")

    if opcao == "1":
        tipo = input("Tipo (receita/despesa): ").lower()
        if tipo not in ["receita", "despesa"]:
            print(Fore.RED + "Tipo inválido! Use 'receita' ou 'despesa'.")
            continue

        try:
            valor = float(input("Valor: "))
        except ValueError:
            print(Fore.RED + "Digite um número válido!")
            continue

        categoria = input("Categoria: ")
        descricao = input("Descrição: ")
        data = input("Data (AAAA-MM-DD): ")
        adicionar_transacao(tipo, valor, categoria, descricao, data)
        print(Fore.GREEN + "Transação adicionada com sucesso!")

    elif opcao == "2":
        transacoes = listar_transacoes()
        if not transacoes:
            print(Fore.YELLOW + "\n  Nenhuma transação cadastrada.")
        else:
            print(Fore.CYAN + "\n===== TRANSAÇÕES =====")
            for t in transacoes:
                cor = Fore.GREEN if t[1] == "receita" else Fore.RED
                print(Fore.WHITE + f"\nID: {t[0]}")
                print(cor + f"Tipo: {t[1].upper()}")
                print(Fore.WHITE + f"Valor:     R$ {t[2]:.2f}")
                print(Fore.WHITE + f"Categoria: {t[3]}")
                print(Fore.WHITE + f"Descrição: {t[4]}")
                print(Fore.WHITE + f"Data:      {t[5]}")
                print(Fore.WHITE + "─" * 30)

    elif opcao == "3":
        saldo = calcular_saldo()
        cor = Fore.GREEN if saldo >= 0 else Fore.RED
        print(cor + f"\nSaldo atual: R$ {saldo:.2f}")

    elif opcao == "4":
        try:
            id_transacao = int(input("Digite o ID da transação que deseja remover: "))
        except ValueError:
            print(Fore.RED + "ID inválido!")
            continue
        remover_transacao(id_transacao)
        print(Fore.GREEN + "Transação removida com sucesso!")

    elif opcao == "5":
        dados = relatorio_categorias()
        if not dados:
            print(Fore.YELLOW + "\n Nenhuma despesa cadastrada.")
        else:
            print(Fore.CYAN + "\n===== GASTOS POR CATEGORIA =====")
            for categoria, total in dados:
                print(Fore.WHITE + f"  {categoria}: " + Fore.RED + f"R$ {total:.2f}")

    elif opcao == "6":
        exportar_csv()
        print(Fore.GREEN + "Arquivo CSV exportado com sucesso!")

    elif opcao == "7":
        gerar_grafico_categorias()

    elif opcao == "8":
        receitas, despesas, saldo = resumo_financeiro()
        print(Fore.CYAN + "\n╔══════════════════════════════╗")
        print(Fore.CYAN + "║       RESUMO FINANCEIRO      ║")
        print(Fore.CYAN + "╚══════════════════════════════╝")
        print(Fore.GREEN + f"Receitas:  R$ {receitas:.2f}")
        print(Fore.RED   + f"Despesas:  R$ {despesas:.2f}")
        cor_saldo = Fore.GREEN if saldo >= 0 else Fore.RED
        print(cor_saldo  + f"Saldo:     R$ {saldo:.2f}")
        print(Fore.WHITE + "─" * 32)

    elif opcao == "9":
        print(Fore.CYAN + "\n===== FILTRAR TRANSAÇÕES =====")
        print("Deixe em branco para ignorar o filtro")

        categoria = input("Categoria: ").strip()
        data_inicio = input("Data início (AAAA-MM-DD): ").strip()
        data_fim = input("Data fim (AAAA-MM-DD): ").strip()

        resultado = filtrar_transacoes(
            categoria=categoria or None,
            data_inicio=data_inicio or None,
            data_fim=data_fim or None
        )

        if not resultado:
            print(Fore.YELLOW + "\n Nenhuma transação encontrada.")
        else:
            print(Fore.CYAN + f"\n{len(resultado)} transação(ões) encontrada(s):")
            for t in resultado:
                cor = Fore.GREEN if t[1] == "receita" else Fore.RED
                print(Fore.WHITE + f"\nID: {t[0]}")
                print(cor + f"Tipo: {t[1].upper()}")
                print(Fore.WHITE + f"Valor:     R$ {t[2]:.2f}")
                print(Fore.WHITE + f"Categoria: {t[3]}")
                print(Fore.WHITE + f"Descrição: {t[4]}")
                print(Fore.WHITE + f"Data:      {t[5]}")
                print(Fore.WHITE + "─" * 30)

    elif opcao == "10":
        print(Fore.CYAN + "\n===== EDITAR TRANSAÇÃO =====")
        print("Deixe em branco para manter o valor atual\n")

        try:
            id_transacao = int(input("ID da transação que deseja editar: "))
        except ValueError:
            print(Fore.RED + "ID inválido!")
            continue

        tipo = input("Novo tipo (receita/despesa): ").lower().strip()
        if tipo and tipo not in ["receita", "despesa"]:
            print(Fore.RED + "Tipo inválido! Use 'receita' ou 'despesa'.")
            continue

        valor_str = input("Novo valor: ").strip()
        try:
            valor = float(valor_str) if valor_str else None
        except ValueError:
            print(Fore.RED + "Valor inválido!")
            continue

        categoria = input("Nova categoria: ").strip()
        descricao = input("Nova descrição: ").strip()
        data      = input("Nova data (AAAA-MM-DD): ").strip()

        sucesso = editar_transacao(
            id_transacao,
            tipo=tipo or None,
            valor=valor,
            categoria=categoria or None,
            descricao=descricao or None,
            data=data or None
        )

        if sucesso:
            print(Fore.GREEN + "Transação editada com sucesso!")
        else:
            print(Fore.RED + "Transação não encontrada!")

    elif opcao == "11":
        print(Fore.CYAN + "\n╔══════════════════════════════╗")
        print(Fore.CYAN + "║       METAS DE GASTOS     ║")
        print(Fore.CYAN + "╚══════════════════════════════╝")
        print(Fore.BLUE + "  1 - Definir meta")
        print(Fore.BLUE + "  2 - Ver metas e situação atual")
        sub = input(Fore.WHITE + "\nEscolha: ").strip()

        if sub == "1":
            categoria = input("Categoria: ").strip()
            if not categoria:
                print(Fore.RED + "Categoria não pode ser vazia!")
                continue
            try:
                valor_limite = float(input("Valor limite mensal (R$): "))
            except ValueError:
                print(Fore.RED + "Valor inválido!")
                continue
            definir_meta(categoria, valor_limite)
            print(Fore.GREEN + f"Meta de R$ {valor_limite:.2f} definida para '{categoria}'!")

        elif sub == "2":
            resultado = verificar_metas()
            if not resultado:
                print(Fore.YELLOW + "\nNenhuma meta cadastrada.")
            else:
                print(Fore.CYAN + "\n===== SITUAÇÃO DAS METAS =====")
                for categoria, limite, gasto in resultado:
                    percentual = (gasto / limite * 100) if limite > 0 else 0
                    if percentual >= 100:
                        cor = Fore.RED
                        status = "LIMITE ULTRAPASSADO"
                    elif percentual >= 80:
                        cor = Fore.YELLOW
                        status = "ATENÇÃO"
                    else:
                        cor = Fore.GREEN
                        status = "OK"

                    print(cor + f"\n  Categoria: {categoria}")
                    print(cor + f"  Gasto:     R$ {gasto:.2f} / R$ {limite:.2f} ({percentual:.1f}%)")
                    print(cor + f"  Status:    {status}")
                    print(Fore.WHITE + "─" * 32)
        else:
            print(Fore.RED + "Opção inválida!")

    elif opcao == "12":   
        print(Fore.CYAN + "\nAté logo!")
        break
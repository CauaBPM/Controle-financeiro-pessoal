import matplotlib.pyplot as plt
from operations import relatorio_categorias

def gerar_grafico_categorias():
    dados = relatorio_categorias()
    categorias = []
    valores = []

    for categoria, total in dados:
        categorias.append(categoria)
        valores.append(total)

    plt.figure(figsize=(8, 5))
    plt.bar(categorias, valores)
    plt.title("Gastos por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Valor (R$)")
    plt.tight_layout()
    plt.savefig("grafico_gastos.png")
    plt.show()
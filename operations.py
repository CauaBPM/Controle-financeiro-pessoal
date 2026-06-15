import sqlite3
import csv


def adicionar_transacao(tipo, valor, categoria, descricao, data):

    conn = sqlite3.connect("finance.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (tipo, valor, categoria, descricao, data)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, valor, categoria, descricao, data))

    conn.commit()
    conn.close()

    print("Transação adicionada com sucesso!")


def listar_transacoes():

    conn = sqlite3.connect("finance.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")

    transacoes = cursor.fetchall()

    conn.close()

    return transacoes

def calcular_saldo():
    transacoes = listar_transacoes()
    saldo = 0

    for transacao in transacoes:
        tipo = transacao[1]
        valor = transacao[2]

        if tipo == "receita":
            saldo += valor
        elif tipo == "despesa":
            saldo -= valor

    return saldo

def remover_transacao(id_transacao):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (id_transacao,))
    conn.commit()
    conn.close()
    print("Transação removida com sucesso!")

def relatorio_categorias():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT categoria, SUM(valor)              
    FROM transactions
    WHERE tipo = 'despesa'
    GROUP BY categoria
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados

def exportar_csv():
    transacoes = listar_transacoes()
    with open(
        "transacoes.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([
            "ID",
            "Tipo",
            "Valor",
            "Categoria",
            "Descrição",
            "Data"
        ])
        escritor.writerows(transacoes)
        print("Arquivo CSV exportado com sucesso!")
def resumo_financeiro():

    conn = sqlite3.connect("finance.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM transactions
        WHERE tipo = 'receita'
    """)

    receitas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM transactions
        WHERE tipo = 'despesa'
    """)

    despesas = cursor.fetchone()[0]

    conn.close()

    saldo = receitas - despesas

    return receitas, despesas, saldo
def filtrar_transacoes(categoria=None, data_inicio=None, data_fim=None):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    query = "SELECT * FROM transactions WHERE 1=1"
    parametros = []

    if categoria:
        query += "AND categoria = ?"
        parametros.append(categoria)
    if data_inicio:
        query += " AND data >= ?"
        parametros.append(data_inicio)
    if data_fim:
        query += "AND data <= ?"
        parametros.append(data_fim)
    cursor.execute(query, parametros)
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes

def editar_transacao(id_transacao, tipo=None, valor=None, categoria=None, descricao=None, data=None):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE id = ?", (id_transacao,))
    transacao = cursor.fetchone()

    if not transacao:
        print("Transação não encontrada!")
        conn.close()
        return False

    novo_tipo     = tipo      if tipo      else transacao[1]
    novo_valor     = valor     if valor     else transacao[2]
    nova_categoria = categoria if categoria else transacao[3]
    nova_descricao = descricao if descricao else transacao[4]
    nova_data      = data      if data      else transacao[5]

    cursor.execute("""
        UPDATE transactions
        SET tipo = ?, valor = ?, categoria = ?, descricao = ?, data = ?
        WHERE id = ?
    """, (novo_tipo, novo_valor, nova_categoria, nova_descricao, nova_data, id_transacao))

    conn.commit()
    conn.close()
    return True
def definir_meta(categoria, valor_limite):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO metas (categoria, valor_limite)
        VALUES (?, ?)
        ON CONFLICT(categoria) DO UPDATE SET valor_limite = ?
    """, (categoria, valor_limite, valor_limite))

    conn.commit()
    conn.close()

def listar_metas():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, valor_limite FROM metas")
    metas = cursor.fetchall()
    conn.close()
    return metas

def verificar_metas():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.categoria, m.valor_limite, COALESCE(SUM(t.valor), 0) as gasto
        FROM metas m
        LEFT JOIN transactions t
            ON m.categoria = t.categoria AND t.tipo = 'despesa'
        GROUP BY m.categoria, m.valor_limite
    """)

    resultado = cursor.fetchall()
    conn.close()
    return resultado
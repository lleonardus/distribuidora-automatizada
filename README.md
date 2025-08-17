# 🚚 Distribuidora Automatizada

Empresas que atuam no ramo da logística geram grandes volumes de dados diariamente
e precisam analisá-los para tomar as melhores decisões mercadológicas. O problema
é que não dá para simplesmente inserir todo esse volume de dados no Excel, pois
isso poderia causar travamentos e até possíveis perdas de informações.

Pensando nisso, desenvolvi este projeto para simular o fluxo de compras de clientes
em uma distribuidora e realizar consultas em SQL, gerando um relatório contendo
apenas informações relevantes para posterior análise de dados.

![Exemplo de Output do Relatório](./docs/images/excel-output.png)

## 💾 Banco de Dados

![Modelo Entidade Relacionamento para o Banco](./docs/images/database.png)

### 📒 Consultas

#### 🔎 Top 5 produtos mais vendidos no mês

```sql
SELECT pr.nome_produto, SUM(i.quantidade) AS total_vendido
  FROM produtos pr
  JOIN itens_pedido i ON pr.id=i.produto_id
  JOIN pedidos pe ON i.pedido_id=pe.id
  WHERE strftime('%m', pe.data_pedido) = strftime('%m', date())
  GROUP BY pr.nome_produto
ORDER BY total_vendido DESC, pr.nome_produto ASC LIMIT(5);
```

#### 🔎 Clientes que mais compraram

```sql
SELECT c.nome_cliente, SUM(pe.valor_total) AS total_gasto
    FROM clientes c
    JOIN pedidos pe ON pe.cliente_id = c.id
    GROUP BY c.nome_cliente
ORDER BY total_gasto DESC, c.nome_cliente ASC;
```

#### 🔎 Entregas Atrasadas

```sql
SELECT e.id, c.nome_cliente, e.data_prevista, e.data_entrega, (julianday(e.data_entrega) - julianday(e.data_prevista)) AS dias_de_atraso
  FROM entregas e
  JOIN pedidos pe ON  pe.id = e.pedido_id
  JOIN clientes c ON  c.id = pe.cliente_id
  WHERE data_entrega > data_prevista
ORDER BY dias_de_atraso DESC, c.nome_cliente ASC;

```

#### 🔎 Faturamento por Estado

```sql
SELECT c.estado, SUM(pe.valor_total) AS faturamento
    FROM clientes c
    JOIN pedidos pe ON c.id=pe.cliente_id
    GROUP BY c.estado
ORDER BY faturamento DESC;
```

## 💿 Como rodar na sua máquina (Linux)

### 📝 Pré-requisitos:

- [Git](https://git-scm.com/downloads)
- [Python 3.9 ou maior](https://www.python.org/downloads/)

```bash

# Clonando o projeto e entrando na pasta
$ git clone https://github.com/lleonardus/distribuidora-automatizada.git
$ cd distribuidora-automatizada

# Configurando virtual environment e instalando as dependências
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install -r requirements.txt

# Definindo as variáveis de ambiente DATABASE e REPORT_PATH.
# Se quiser usar um banco diferente do sqlite, mude a variável DATABASE.
# REPORT_PATH é o local onde será gerado o relatório. Com o valor abaixo,
# ele será gerado na raiz do projeto com o nome de relatorio.xlsx
$ echo -e 'DATABASE=sqlite:///distribuidora.db\nREPORT_PATH=relatorio.xlsx' > .env

# Criando as tabelas e inserindo dados fictícios.
# Se as tabelas já existirem e estiverem com dados, não precisa seguir esse passo
$ python3 -m db.init_db
$ python3 -m db.insert_data

# Gerando relatório
$ python3 main.py
```

## 🧰 Ferramentas Utilizadas

- [Git](https://git-scm.com/downloads)
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [Python](https://www.python.org/downloads/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/intro.html#installation)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Faker](https://pypi.org/project/Faker/)

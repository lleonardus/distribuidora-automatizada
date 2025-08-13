## Consultas

1. Top 5 produtos mais vendidos no mês

```sql
SELECT pr.nome_produto, SUM(i.quantidade) as total_vendido
  FROM produtos pr
  JOIN itens_pedido i ON pr.id=i.produto_id
  JOIN pedidos pe on i.pedido_id=pe.id
  WHERE strftime('%m', pe.data_pedido) = strftime('%m', date())
  GROUP BY pr.nome_produto
ORDER BY total_vendido DESC, pr.nome_produto ASC LIMIT(5);
```

2. Clientes que mais compraram

```sql
SELECT c.nome_cliente, SUM(pe.valor_total) total_gasto
    FROM clientes c
    JOIN pedidos pe ON pe.cliente_id = c.id
    GROUP BY c.nome_cliente
ORDER BY total_gasto DESC, c.nome_cliente ASC;

```

3. Entregas atrasadas

```sql
SELECT e.id, c.nome_cliente, e.data_prevista, e.data_entrega
    FROM entregas e
    JOIN pedidos pe ON pe.id = e.pedido_id
    JOIN clientes c ON c.id = pe.cliente_id
    WHERE data_entrega > data_prevista
ORDER BY data_entrega DESC;

```

4. Faturamento por estado

```sql
SELECT c.estado, SUM(pe.valor_total) AS faturamento
    FROM clientes c
    JOIN pedidos pe ON c.id=pe.cliente_id
    GROUP BY c.estado
ORDER BY faturamento DESC;

```

## Fontes Úteis

- https://www.sqlite.org/lang_datefunc.html

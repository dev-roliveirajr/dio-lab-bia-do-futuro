# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Objetivo |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Produtos financeiros diponíveis para o usuário |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

- inclusão de novos produtos financeiros;
- inclusão de novas transações;

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

- Os arquivos serão carregados via código.
    - Os arquivos CSV serão carregados utilizando a bilioteca "Pandas";
    - Os arquivos JSON serão carregado utilizando a biblioteca "JSON";

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

- As informações sobre o Perfil do Investidor e Produtos Financeiros serão carregados no system prompt;
- As informações das transações erão consultadas dinamicamente, conforme a solicitação do usuário;

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Entradas no período:
- Salário: R$ 8.659

Saídas no período:
- transporte: R$ 256
- alimentacao: R$ 1.798
- saude: R$ 614

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```

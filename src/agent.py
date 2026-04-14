# Imports
import pandas as pd
import json 
import requests

# Load the data
from config import OLLAMA_API_URL, MODEL_NAME, ENVIAR_PARAMETROS_OPCIONAIS, TEMPERATURE, TOP_P, NUM_PREDICT, REPEAT_PENALTY

dsperfil = json.load(open('data/perfil_investidor.json'))
dsprodutos = json.load(open('data/produtos_financeiros.json'))

dshistorico = pd.read_csv('data/historico_atendimento.csv').tail(5)

dstransacoes = pd.read_csv('data/transacoes.csv').tail(20)
df_saida = dstransacoes[dstransacoes["tipo"] == "saida"]
df_entrada = dstransacoes[dstransacoes["tipo"] == "entrada"]

def agrupar_transacoes_por_categoria(tipo: str) -> str:
    """Agrupa transações pelo tipo informado usando a fração já carregada em dstransacoes."""
    tipo = tipo.lower().strip()
    if tipo not in {"saida", "entrada"}:
        raise ValueError("Tipo deve ser 'saida' ou 'entrada'.")

    df_tipo = dstransacoes[dstransacoes["tipo"] == tipo]
    if tipo == "saida":
        agrupamento = df_tipo.groupby("categoria")["valor"].sum()
        linhas = [f"- Gastos com {categoria}: {total}" for categoria, total in agrupamento.items()]
    else:
        agrupamento = df_tipo.groupby("descricao")["valor"].sum()
        linhas = [f"- Receita de {descricao}: {total}" for descricao, total in agrupamento.items()]

    return "\n".join(linhas) + "\n" if linhas else ""


total_saida = df_saida["valor"].sum()
total_entrada = df_entrada["valor"].sum()
saldo = total_entrada - total_saida

# Create the app

SYSTEM_PROMPT = """Você é Luma, uma assistente de finanças pessoais e de investimentos.

Seu objetivo é analisar dados financeiros do cliente e fornecer respostas objetivas, corretas e baseadas exclusivamente nos dados disponíveis.

====================
REGRAS GERAIS
====================
- Seja direta e objetiva
- Use linguagem simples
- Nunca invente informações
- Use apenas os dados fornecidos
- Se faltar informação, informe claramente
- Não responda nada fora do tema finanças

Se a pergunta não for sobre finanças:
Responda: "Posso ajudar apenas com assuntos financeiros."

====================
REGRAS SOBRE TRANSAÇÕES
====================
Cada transação possui:
data, descricao, categoria, valor, tipo

Exemplo:
"2025-12-25,Museu,lazer,61.34,saida"

IMPORTANTE:
- "saida" = despesa
- "entrada" = receita

====================
COMO ANALISAR TRANSAÇÕES
====================

Para perguntas de gastos:
- Considere apenas transações com tipo = "saida"
- Filtre pela categoria solicitada (ex: alimentacao)
- Some todos os valores

Para perguntas de receita:
- Considere apenas transações com tipo = "entrada"
- Filtre pela categoria solicitada (ex: receita)
- Some todos os valores

Para saldo:
- saldo = total entradas - total saidas

Sempre mostre:
- valor total
- (opcional) quantidade de transações

====================
INVESTIMENTOS
====================

Você NÃO deve recomendar diretamente um produto.

Você deve:
- Filtrar produtos compatíveis com o perfil do cliente
- Explicar quais são adequados
- Explicar o porquê

Nunca:
- Dizer "invista em X"
- Garantir retorno

====================
FORMATO DAS RESPOSTAS
====================

Para cálculos:
- Responda com o valor final
- Seja direto

Exemplo:
"Você gastou R$ 1.250,00 com alimentação."

Sobre os termos:
Receitas: Representa todas as entradas de dinheiro, ou seja, o que o cliente ganha.
Despesas: Representa Todas as saídas de dinheiro, ou seja, o que o cliente gasta no seu dia a dia.
Saldo: É a soma das Receitas menos ( - ) a soma das Despesas. 
Se o saldo for positivo, o cliente tem o saldo para investir.
Se o saldo for negativo, o cliente não tem saldo para fazer investimentos.

Para análises:
1. Resumo
2. Conclusão

Para investimentos:
1. Perfil do cliente
2. Opções compatíveis
3. Explicação

Antes de responder:
1. Verifique se todas as transações foram consideradas
2. Verifique se não há duplicações
3. Verifique se tipo "entrada" não foi tratado como "saida"
4. Só então responda 

Responda APENAS com base nos dados fornecidos.
Não reescreva nem recrie transações.
Não altere valores. """

# contexts
contexto = f"""
====================
DADOS DO CLIENTE
==================== 
CLIENTE: {dsperfil['nome']}, {dsperfil['idade']} anos, perfil de investidor: {dsperfil['perfil_investidor']}, aceita risco: {"sim" if dsperfil['aceita_risco'] else "não"} \n
RENDA MENSAL: R$ {dsperfil['renda_mensal']} \n
OBJETIVO: {dsperfil['objetivo_principal']} \n
PATRIMÔNIO: R$ {dsperfil['patrimonio_total']} | RESERVA: R$ {dsperfil['reserva_emergencia_atual']} \n
METAS: {', '.join([m['meta'] for m in dsperfil['metas']])} \n
HISTÓRICO DE ATENDIMENTO:\n {dshistorico.to_csv(index=False, header=True)} \n
PRODUTOS FINANCEIROS:\n {dsprodutos} \n
TRANSACOES:\n {dstransacoes.to_csv(index=False, header=True)} \n 

Transações agrupadas caso precise da informação: \n
Entradas:\n
{agrupar_transacoes_por_categoria("entrada")} \n
Saídas:\n
{agrupar_transacoes_por_categoria("saida")} \n

Resumo calculado das transações: \n
- Total receitas: {total_entrada} \n
- Total despesas: {total_saida} \n
- Saldo: {saldo} \n """


# Function to get response from the model
def get_response(user_input=None):
    if user_input is None:
        user_input = []
        
    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT} | {contexto}"},
    ]

    # adiciona histórico limitado
    messages += user_input  # cada item: {"role": "user"/"assistant", "content": "..."}
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,   # <- agora usa 'messages' ao invés de 'prompt'
        "stream": False
    }

    # verifica se envia parametros opcionais no payload
    if ENVIAR_PARAMETROS_OPCIONAIS:
        payload["options"] = {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "num_predict": NUM_PREDICT,
            "repeat_penalty": REPEAT_PENALTY
        }

    response = requests.post(OLLAMA_API_URL, json=payload)
    data = response.json()

    # capturar a resposta do modelo
    try:
        return data['choices'][0]['message']['content']
    except (KeyError, IndexError):
        # fallback caso algo dê errado
        return "Não foi possível gerar uma resposta"
# Imports
import pandas as pd
import json 
import requests

# Load the data
from config import OLLAMA_API_URL, MODEL_NAME, ENVIAR_PARAMETROS_OPCIONAIS, TEMPERATURE, TOP_P, NUM_PREDICT, REPEAT_PENALTY

dsperfil = json.load(open('data/perfil_investidor.json'))
dsprodutos = json.load(open('data/produtos_financeiros.json'))
dshistorico = pd.read_csv('data/historico_atendimento.csv')    
dstransacoes = pd.read_csv('data/transacoes.csv')

# Create the app

# contexts
contexto = f"""INFORMAÇÕES DE CONTEXTO: 
CLIENTE: {dsperfil['nome']}, {dsperfil['idade']} anos, perfil de investidor: {dsperfil['perfil_investidor']}, aceita risco: {"sim" if dsperfil['aceita_risco'] else "não"}
RENDA MENSAL: R$ {dsperfil['renda_mensal']}
OBJETIVO: {dsperfil['objetivo_principal']}
PATRIMÔNIO: R$ {dsperfil['patrimonio_total']} | RESERVA: R$ {dsperfil['reserva_emergencia_atual']}
METAS: {', '.join([m['meta'] for m in dsperfil['metas']])}
HISTÓRICO DE ATENDIMENTO: {dshistorico.tail(5).to_dict(orient='records')}
TRANSACOES: {dstransacoes.tail(50).to_dict(orient='records')}
PRODUTOS FINANCEIROS: {dsprodutos}"""

SYSTEM_PROMPT = """Você é Luma, uma agente financeira inteligente da instituição.
Seu objetivo é ajudar o cliente a tomar decisões financeiras mais seguras e estratégicas, antecipando riscos e oportunidades com base em dados reais e promovendo maior previsibilidade e autonomia financeira.

Você tem acesso a:
1. Perfil do investidor do cliente (risco, objetivos, horizonte).
2. Histórico de transações (entradas, saídas, padrões).
3. Lista de produtos financeiros disponíveis na instituição.

Seu papel é:
- Antecipar necessidades financeiras.
- Simular cenários futuros.
- Explicar recomendações com base em dados.
- Cocriar soluções junto ao cliente.

REGRAS:
1. Utilize exclusivamente os dados fornecidos no contexto.
2. Nunca invente informações, rentabilidades ou características de produtos.
3. Sempre explicite as premissas utilizadas nas análises.
4. Quando não houver dados suficientes, informe a limitação claramente.
5. Nunca recomende produtos financeiros para o usuário. Apenas ajude no conhecimento sobre produtos financeiros e quais são permitidos baseado no perfil do investidor.
6. Não substitua aconselhamento humano quando houver alto risco financeiro.
7. Nunca solicite ou exponha informações sensíveis como senhas.
8. Seja clara, objetiva e educativa.
9. Foque no tema "Finanças". Se a pergunta não for relacionada ao tema, responda "Eu gostaria muito de ajudar más estou aqui para falar sobre finanças. Outros assuntos podem ser tratdos com outro agente."

SOBRE AS TRANSAÇÕES:
Toda transação está descrita com este padrão: "2025-12-25,Museu,lazer,61.34,saida"
Vou explicar cada parte de uma transação: 
No exemplo: "2025-12-25,Museu,lazer,61.34,saida":
2025-12-25 = data da transação no padrão AAAA-MM-DD;
Museu = subcategoria da transação;
lazer = categoria da trnasação. Uma categoria contém mais de uma subcategoria;
61.34 = valor da transação. Na modeda REAL fica R$ 61,34;
saida = tipo de operação. "saida" siginifica "despesa" e entrada significa "receita". Se perguntar sobre despesas, foque nas "saidas". se perguntar sobre receitas, foque nas "entradas".

FORMATO DAS RESPOSTAS:
- Seja simples e direta.
- Apenas se for solicitado, explique o raciocínio.
- Ofereça uma simulação ou próximo passo caso seja solictado. """

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
        payload[options] = {
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
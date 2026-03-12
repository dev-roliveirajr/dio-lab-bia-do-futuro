# Imports
import pandas as pd
import json 
import requests

# Load the data
from config import OLLAMA_URL, MODEL_NAME

dsperfil = json.load(open('data/perfil_investidor.json'))
dsprodutos = json.load(open('data/produtos_financeiros.json'))
dshistorico = pd.read_csv('data/historico_atendimento.csv')    
dstransacoes = pd.read_csv('data/transacoes.csv')

# Create the app

# contexts
contexto = f"""
CLIENTE: {dsperfil['nome']}, {dsperfil['idade']} anos, perfil de investidor: {dsperfil['perfil_investidor']}, aceita risco: {"sim" if dsperfil['aceita_risco'] else "não"}
RENDA MENSAL: R$ {dsperfil['renda_mensal']}
OBJETIVO: {dsperfil['objetivo_principal']}
PATRIMÔNIO: R$ {dsperfil['patrimonio_total']} | RESERVA: R$ {dsperfil['reserva_emergencia_atual']}

METAS: {', '.join([m['meta'] for m in dsperfil['metas']])}

HISTÓRICO DE ATENDIMENTO: {dshistorico.to_dict(orient='records')}

TRANSACOES: {dstransacoes.to_dict(orient='records')}

PRODUTOS FINANCEIROS: {dsprodutos}
"""

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

FORMATO DAS RESPOSTAS:
- Comece com um insight ou análise baseada em dados.
- Explique o raciocínio.
- Ofereça uma simulação ou próximo passo. """

# Function to get response from the model
def get_response(user_input):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO:
    {contexto}

    PERGUNTA: {user_input}
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
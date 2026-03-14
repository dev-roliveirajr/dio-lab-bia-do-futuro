# imports
import streamlit as st
import time
import agent

# Load the data
from config import STREAM_DELAY, CHAT_MESSAGES_HIST 

# interface
st.title("Luma, luz e prosperidade financeira!")

# cria histórico na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# input do usuário
if pergunta := st.chat_input("Faça sua pergunta para a Luma:"):
    
    # adiciona pergunta no histórico
    st.session_state.messages.append(
        {"role": "user", "content": pergunta}
    )

    # mostra pergunta
    with st.chat_message("user"):
        st.write(pergunta)

    print(f"usuario perguntou: {pergunta}")

    with st.spinner("Luma está pensando..."):
        resposta = agent.get_response(st.session_state.messages)
        
    print(f"assistente respondeu: {resposta}")

    # mostra resposta
    with st.chat_message("assistant"):
        placeholder = st.empty()
        texto = ""

        for palavra in resposta.split():
            texto += palavra + " "
            placeholder.markdown(texto + "▌")
            time.sleep(STREAM_DELAY)

        placeholder.markdown(texto)
    
    # adiciona resposta no histórico
    st.session_state.messages.append(
        {"role": "assistant", "content": resposta}
    )

    # somente as últimas 10 mensagens para evitar que os tokens explodam
    st.session_state.messages = st.session_state.messages[-CHAT_MESSAGES_HIST:]    

    
# imports
import streamlit as st
import time
import agent

# Load the data
from config import STREAM_DELAY, CHAT_MESSAGES_HIST_ITERATIONS 

# interface
st.title("💡Luma, luz e prosperidade financeira!")

# cria histórico na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# input do usuário
if pergunta := st.chat_input("Faça sua pergunta para a Luma:"):
    
    # mostra pergunta
    with st.chat_message("user"):
        st.write(pergunta)

    # adiciona pergunta no histórico
    st.session_state.messages.append(
        {"role": "user", "content": pergunta}
    )

    with st.spinner("Trabalhando na melhor resposta..."):
        # somente as últimas X mensagens para evitar que os tokens explodam
        MAX_MESSAGES = (CHAT_MESSAGES_HIST_ITERATIONS * 2) - 1  # isso faz que tenhamos sempre par de pergunta e resposta 
        resposta = agent.get_response(st.session_state.messages[-MAX_MESSAGES:])

    # adiciona resposta no histórico
    st.session_state.messages.append(
        {"role": "assistant", "content": resposta}
    )
        
    # mostra resposta
    with st.chat_message("assistant"):
        placeholder = st.empty()
        texto = ""

        for palavra in resposta.split(" "):
            texto += palavra + " "
            placeholder.markdown(texto + "▌")
            time.sleep(STREAM_DELAY)

        placeholder.markdown(texto)



    
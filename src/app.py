# imports
import streamlit as st

import agent

# interface
st.title("Luma, luz e prosperidade financeira!")

if pergunta := st.chat_input("Faça sua pergunta para a Luma:"):
    st.chat_message("user").write(pergunta)
    print(f"usuario perguntou: {pergunta}")
    with st.spinner("Luma está pensando..."):
        resposta = agent.get_response(pergunta)
        print(resposta)
        st.chat_message("assistant").write(resposta)
    print("assistente respondeu")
        
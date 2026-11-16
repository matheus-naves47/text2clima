import streamlit as st
from agent import text_to_sql_transparente

st.set_page_config(page_title="Text2Clima - Special Coffee", page_icon="🌦️", layout="centered")

st.title("🌦️ Text2Clima - Special Coffee ☕")
st.markdown("""
Faça perguntas em linguagem natural sobre a base de dados **BR-DWGD** (Regiões Produtoras de Cafés Especiais). 
""")
st.divider()

# 1. Inicialização do Histórico
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Olá! O que você gostaria de saber sobre os dados climáticos hoje?"}
    ]

# 2. Renderização do Histórico na Tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Se a mensagem tiver mais detalhes guardados, desenha o expander
        if "sql" in msg and "resultado_bruto" in msg:
            with st.expander("🔍 Ver mais detalhes."):
                st.code(msg["sql"], language="sql")
                st.text(f"Retorno do Banco:\n{msg['resultado_bruto']}")

# 3. Caixa de Texto para o Usuário
if pergunta_usuario := st.chat_input("Ex: Quantas regiões diferentes estão cadastradas?"):
    
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)
        
    st.session_state.mensagens.append({"role": "user", "content": pergunta_usuario})
    
    # 4. Processamento da IA
    with st.chat_message("assistant"):
        with st.spinner("Traduzindo para SQL e consultando o banco de dados..."):
            try:
                dados_ia = text_to_sql_transparente(pergunta_usuario)
                
                resposta_ia = dados_ia["resposta"]
                sql_gerado = dados_ia["sql"]
                resultado_bruto = dados_ia["resultado_bruto"]
                
                # Exibe a resposta principal
                st.markdown(resposta_ia)
                
                # Exibe o botão expansível
                with st.expander("🔍 Ver mais detalhes."):
                    st.code(sql_gerado, language="sql")
                    st.text(f"Retorno do Banco:\n{resultado_bruto}")
                
                # Salva no histórico
                st.session_state.mensagens.append({
                    "role": "assistant", 
                    "content": resposta_ia,
                    "sql": sql_gerado,
                    "resultado_bruto": resultado_bruto
                })
                
            except Exception as e:
                st.error(f"Ocorreu um erro durante a consulta: {e}")
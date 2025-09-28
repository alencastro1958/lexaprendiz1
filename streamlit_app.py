"""
Arquivo principal estável para o Streamlit Cloud
Versão otimizada sem conflitos de DOM
"""

import streamlit as st
import sys
import os

# Configuração inicial
st.set_page_config(
    page_title="LexAprendiz",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Previne conflitos de DOM
st.markdown("""
<style>
    .stApp { transition: none !important; }
    .stButton button { transition: all 0.2s ease !important; }
    .element-container { position: relative !important; }
    .stSelectbox, .stTextInput, .stTextArea { transition: none !important; }
</style>
""", unsafe_allow_html=True)

try:
    # Imports seguros
    from banco_conhecimento import BancoConhecimentoAprendizagem
    from ferramentas_juridicas import PesquisadorJuridico
    from auth_system import *
    from content_manager import *
    from logo_base64 import get_lexaprendiz_logo
    
    def main():
        """Interface principal simplificada"""
        
        # Sistema de autenticação sem conflitos
        if not is_authenticated():
            # Logo
            logo_html = get_lexaprendiz_logo()
            if logo_html:
                st.markdown(logo_html, unsafe_allow_html=True)
            
            st.markdown("# ⚖️ LexAprendiz")
            st.markdown("### Especialista em Legislação da Aprendizagem")
            
            # Forms de auth sem st.rerun()
            if st.session_state.get("show_register", False):
                show_register_form()
            else:
                show_login_form()
            return
        
        # Interface principal
        with st.sidebar:
            st.header("👤 Usuário")
            show_user_info()
            st.markdown("---")
            
            # Admin dashboard
            if is_admin(st.session_state.get("user_data")):
                with st.expander("🛠️ Dashboard Admin", expanded=False):
                    show_admin_dashboard()
        
        # Chat interface
        logo_html = get_lexaprendiz_logo()
        if logo_html:
            st.markdown(logo_html, unsafe_allow_html=True)
        
        st.markdown("# ⚖️ LexAprendiz - Especialista em Legislação da Aprendizagem")
        st.info("Olá! Sou o LexAprendiz, seu especialista em legislação da aprendizagem.")
        
        # Chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Digite sua pergunta..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Consultando..."):
                    try:
                        banco = BancoConhecimentoAprendizagem()
                        resposta = banco.consultar(prompt)
                        
                        if "não encontrei informações específicas" in resposta.lower():
                            pesquisador = PesquisadorJuridico()
                            pesquisa = pesquisador.pesquisar_legislacao(prompt)
                            if pesquisa:
                                resposta += f"\n\n**Pesquisa Online:**\n{pesquisa}"
                        
                        st.markdown(resposta)
                        st.session_state.messages.append({"role": "assistant", "content": resposta})
                    
                    except Exception as e:
                        error_msg = f"Erro: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Botão limpar
        if st.button("🗑️ Limpar Chat"):
            st.session_state.messages = []
            st.success("Chat limpo!")
    
    # Executa aplicação
    if __name__ == "__main__":
        main()

except Exception as e:
    st.error(f"⚠️ Erro na aplicação: {str(e)}")
    st.info("🔄 Recarregue a página.")
    
    # Fallback simples
    st.markdown("# ⚖️ LexAprendiz")
    st.markdown("### Sistema temporariamente indisponível")
    st.info("Por favor, recarregue a página em alguns instantes.")
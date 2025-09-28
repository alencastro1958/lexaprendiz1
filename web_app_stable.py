"""
Interface Web para LexAprendiz - Especialista em Legislação da Aprendizagem
Sistema completo com autenticação, personalização e estabilidade
"""

import streamlit as st
from banco_conhecimento import BancoConhecimentoAprendizagem
from ferramentas_juridicas import PesquisadorJuridico
from auth_system import *
from content_manager import *
from logo_base64 import get_lexaprendiz_logo
from app_stability import safe_theme_change, prevent_dom_conflicts, check_app_health
import os
from datetime import datetime

def configure_page():
    """Configura página inicial"""
    page_title = get_content("page_title", "LexAprendiz")
    page_icon = get_content("page_icon", "⚖️")
    
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Aplica tema e CSS personalizado
    apply_theme()
    prevent_dom_conflicts()

def main():
    """Função principal da aplicação"""
    configure_page()
    
    # Verifica saúde da aplicação
    health_ok, health_msg = check_app_health()
    if not health_ok:
        st.error(f"⚠️ Problema detectado: {health_msg}")
        st.stop()
    
    # Sistema de autenticação
    if not is_authenticated():
        show_auth_interface()
        return
    
    # Interface principal para usuários autenticados
    show_main_interface()

def show_auth_interface():
    """Interface de autenticação"""
    # Logo e título
    logo_html = get_lexaprendiz_logo()
    if logo_html:
        st.markdown(logo_html, unsafe_allow_html=True)
    
    app_title = get_content("app_title", "⚖️ LexAprendiz")
    app_subtitle = get_content("app_subtitle", "Especialista em Legislação da Aprendizagem")
    
    st.markdown(f"# {app_title}")
    st.markdown(f"### {app_subtitle}")
    
    # Formulários de autenticação
    if st.session_state.get("show_register", False):
        show_register_form()
    else:
        show_login_form()

def show_main_interface():
    """Interface principal para usuários logados"""
    # Sidebar
    with st.sidebar:
        user_title = get_content("sidebar_user_title", "👤 Usuário")
        st.header(user_title)
        show_user_info()
        st.markdown("---")
        
        # Seletor de tema
        st.markdown("### 🎨 Aparência")
        current_theme = get_content("theme_mode", "light")
        
        theme_options = {
            "light": "🌞 Clara",
            "dark": "🌙 Escura"
        }
        
        selected_theme = st.selectbox(
            "Escolha o tema:",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=0 if current_theme == "light" else 1
        )
        
        # Mudança segura de tema
        if selected_theme != current_theme:
            if st.button("🎨 Aplicar Tema", use_container_width=True):
                safe_theme_change(selected_theme)
        
        st.markdown("---")
        
        # Dashboard Admin
        if is_admin(st.session_state.get("user_data")):
            admin_title = get_content("sidebar_admin_title", "🛠️ Dashboard Admin")
            with st.expander(admin_title, expanded=False):
                show_admin_dashboard()
    
    # Área principal
    show_chat_interface()

def show_chat_interface():
    """Interface de chat principal"""
    # Logo e cabeçalho
    logo_html = get_lexaprendiz_logo()
    if logo_html:
        st.markdown(logo_html, unsafe_allow_html=True)
    
    # Título personalizado
    main_title = get_content("main_title", "⚖️ LexAprendiz - Especialista em Legislação da Aprendizagem")
    st.markdown(f"# {main_title}")
    
    # Mensagem de boas-vindas
    welcome_msg = get_content("welcome_message", 
        "Olá! Sou o LexAprendiz, seu especialista em legislação da aprendizagem. "
        "Posso ajudá-lo com dúvidas sobre contratos, direitos, deveres e regulamentações."
    )
    st.info(welcome_msg)
    
    # Inicializa histórico de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibe histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua pergunta sobre legislação da aprendizagem..."):
        # Adiciona pergunta do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processa resposta
        with st.chat_message("assistant"):
            with st.spinner("Consultando base jurídica..."):
                try:
                    # Consulta base de conhecimento
                    banco = BancoConhecimentoAprendizagem()
                    resposta = banco.consultar(prompt)
                    
                    # Se não encontrou resposta específica, faz pesquisa online
                    if "não encontrei informações específicas" in resposta.lower():
                        pesquisador = PesquisadorJuridico()
                        pesquisa_online = pesquisador.pesquisar_legislacao(prompt)
                        if pesquisa_online:
                            resposta += f"\n\n**Pesquisa Online:**\n{pesquisa_online}"
                    
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                    
                except Exception as e:
                    error_msg = f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Limpar Chat", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat limpo!")
            st.balloons()
    
    with col2:
        if st.button("📋 Exportar Chat", use_container_width=True):
            if st.session_state.messages:
                chat_export = "\n\n".join([
                    f"**{msg['role'].upper()}:** {msg['content']}" 
                    for msg in st.session_state.messages
                ])
                st.download_button(
                    label="💾 Baixar Chat",
                    data=chat_export,
                    file_name=f"lexaprendiz_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.info("Nenhuma conversa para exportar.")
    
    with col3:
        help_text = get_content("help_button_text", "❓ Ajuda")
        if st.button(help_text, use_container_width=True):
            show_help_section()

def show_help_section():
    """Seção de ajuda"""
    with st.expander("❓ Como usar o LexAprendiz", expanded=True):
        help_content = get_content("help_content", """
        **Como fazer perguntas:**
        - Seja específico: "Qual o prazo para registro do contrato de aprendizagem?"
        - Use termos técnicos: "aprendiz", "CTPS", "cota", "deficiência"
        - Pergunte sobre casos práticos: "Empresa com 50 funcionários precisa de quantos aprendizes?"
        
        **Principais tópicos:**
        - 📋 Contratos de aprendizagem
        - 👥 Cotas de aprendizes
        - 🏢 Obrigações das empresas
        - 📚 Programas de aprendizagem
        - ⚖️ Penalidades e multas
        - 🤰 Direitos da gestante aprendiz
        - ♿ Pessoas com deficiência
        """)
        st.markdown(help_content)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"⚠️ Erro crítico na aplicação: {str(e)}")
        st.info("🔄 Recarregue a página para tentar novamente.")
        
        # Log de erro para admin
        if is_admin(st.session_state.get("user_data")):
            with st.expander("🔧 Detalhes do Erro (Admin)", expanded=False):
                st.code(str(e))
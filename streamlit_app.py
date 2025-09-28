"""
LexAprendiz - Especialista em Legislação da Aprendizagem
Sistema completo com autenticação, admin, CONAP e todas as funcionalidades
"""

import streamlit as st
from datetime import datetime
from conap_database import consultar_conap

# Imports dos módulos completos
try:
    from auth_system import *
    from content_manager import *
    from logo_base64 import get_uploaded_logo, get_initial_logo
    from banco_conhecimento import BancoConhecimentoAprendizagem
    from ferramentas_juridicas import PesquisadorJuridico
    AUTH_AVAILABLE = True
except ImportError as e:
    st.error(f"⚠️ Erro ao importar módulos: {e}")
    AUTH_AVAILABLE = False

def get_lexaprendiz_logo():
    """Função wrapper para obter logo"""
    logo = get_uploaded_logo()
    if not logo:
        logo = get_initial_logo()
    return logo

# Configuração da página
st.set_page_config(
    page_title="LexAprendiz",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .stApp { transition: none !important; }
    .main-header { text-align: center; margin-bottom: 2rem; }
    .chat-container { max-width: 800px; margin: 0 auto; }
    .admin-section { 
        background-color: #f0f8ff; 
        padding: 1rem; 
        border-radius: 10px; 
        border-left: 5px solid #194b75; 
    }
    .info-banner { 
        background: linear-gradient(90deg, #194b75, #2c5aa0);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    .novo-banner {
        background: linear-gradient(90deg, #ff6b35, #f7931e);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Banco de conhecimento básico para fallback
CONHECIMENTO_FALLBACK = {
    "direitos_gestante": """
    **Direitos da Aprendiz Gestante:**
    1. Estabilidade no emprego desde confirmação até 5 meses pós-parto
    2. Licença-maternidade de 120 dias
    3. Dispensa para consultas pré-natais
    4. Transferência para função compatível se necessário
    **Base Legal:** CLT Art. 391-A, Lei 11.788/2008
    """,
    "cota_aprendizes": """
    **Cálculo de Cota de Aprendizes:**
    - 5% a 15% do total de funcionários
    - Base: funções que demandem formação profissional
    - Idade: 14 a 24 anos (sem limite para PCD)
    **Base Legal:** Lei 10.097/2000
    """,
    "penalidades": """
    **Penalidades por Descumprimento:**
    - Multa: R$ 402,53 a R$ 4.025,33 por aprendiz não contratado
    - Auto de infração pela fiscalização
    - TAC com MPT
    **Base Legal:** CLT Art. 434
    """
}

def buscar_resposta_completa(pergunta):
    """Busca resposta usando todos os sistemas disponíveis"""
    pergunta_lower = pergunta.lower()
    
    # 1. Tenta CONAP primeiro
    conap_result = consultar_conap(pergunta)
    if conap_result and "não encontrei" not in conap_result.lower():
        return conap_result
    
    # 2. Tenta banco de conhecimento completo
    if AUTH_AVAILABLE:
        try:
            banco = BancoConhecimentoAprendizagem()
            resposta = banco.consultar(pergunta)
            if resposta and "não encontrei" not in resposta.lower():
                return resposta
        except:
            pass
    
    # 3. Busca no conhecimento básico
    if any(word in pergunta_lower for word in ['gestante', 'grávida', 'gravidez', 'maternidade']):
        return CONHECIMENTO_FALLBACK['direitos_gestante']
    elif any(word in pergunta_lower for word in ['cota', 'quantos', 'cálculo', 'percentual']):
        return CONHECIMENTO_FALLBACK['cota_aprendizes']
    elif any(word in pergunta_lower for word in ['multa', 'penalidade', 'fiscalização', 'punição']):
        return CONHECIMENTO_FALLBACK['penalidades']
    
    # 4. Resposta padrão
    return """
    **Tópicos Disponíveis:**
    
    **📋 Legislação da Aprendizagem:**
    - Direitos da gestante aprendiz
    - Cálculo de cotas obrigatórias
    - Penalidades e fiscalização
    
    **🎓 CONAP - Programas de Aprendizagem:**
    - Consulta por CBO
    - Programas do Sistema S (SENAI, SENAC, SENAT, SENAR)
    - Arcos ocupacionais
    
    **Exemplos de perguntas:**
    - "Quais os direitos da aprendiz gestante?"
    - "Programas do SENAI"
    - "CBO 4110-10"
    - "Como calcular cota de aprendizes?"
    """

def show_auth_interface():
    """Interface de autenticação completa"""
    # Logo
    logo_html = get_lexaprendiz_logo()
    if logo_html:
        st.markdown(logo_html, unsafe_allow_html=True)
    
    st.markdown("# ⚖️ LexAprendiz")
    st.markdown("### Especialista em Legislação da Aprendizagem")
    
    # Banners informativos
    st.markdown("""
    <div class="info-banner">
        🎯 Especialista em Legislação Brasileira da Aprendizagem + CONAP
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Consulte sobre direitos, deveres, cotas, penalidades e programas de aprendizagem profissional do Catálogo Nacional (CONAP).")
    
    st.markdown("""
    <div class="novo-banner">
        📋 NOVO! Integração com CONAP - Consulte programas, CBOs, Sistema S (SENAI, SENAC, SENAT, SENAR) e arcos ocupacionais!
    </div>
    """, unsafe_allow_html=True)
    
    # Sistema de autenticação
    if st.session_state.get("show_register", False):
        show_register_form()
    else:
        show_login_form()

def show_main_interface():
    """Interface principal para usuários logados"""
    # Sidebar com informações do usuário e admin
    with st.sidebar:
        st.header("👤 Usuário")
        show_user_info()
        st.markdown("---")
        
        # Seletor de tema
        st.markdown("### 🎨 Aparência")
        current_theme = get_content("theme_mode", "light") if AUTH_AVAILABLE else "light"
        
        theme_options = {"light": "🌞 Clara", "dark": "🌙 Escura"}
        selected_theme = st.selectbox(
            "Escolha o tema:",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=0 if current_theme == "light" else 1
        )
        
        if selected_theme != current_theme and AUTH_AVAILABLE:
            if st.button("🎨 Aplicar Tema", use_container_width=True):
                try:
                    content = load_content_settings()
                    content["theme_mode"] = selected_theme
                    save_content_settings(content)
                    st.success("Tema alterado! Recarregue a página.")
                    st.balloons()
                except:
                    st.info("Tema será aplicado no próximo login.")
        
        st.markdown("---")
        
        # Dashboard Admin
        if AUTH_AVAILABLE and is_admin(st.session_state.get("user_data")):
            with st.expander("🛠️ Dashboard Admin", expanded=False):
                show_admin_dashboard()
    
    # Área principal
    show_chat_interface()

def show_chat_interface():
    """Interface de chat principal"""
    # Logo
    if AUTH_AVAILABLE:
        logo_html = get_lexaprendiz_logo()
        if logo_html:
            st.markdown(logo_html, unsafe_allow_html=True)
    
    # Título personalizado
    main_title = get_content("main_title", "⚖️ LexAprendiz - Especialista em Legislação da Aprendizagem") if AUTH_AVAILABLE else "⚖️ LexAprendiz - Especialista em Legislação da Aprendizagem"
    st.markdown(f"# {main_title}")
    
    # Banners informativos
    st.markdown("""
    <div class="info-banner">
        🎯 Especialista em Legislação Brasileira da Aprendizagem + CONAP
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Consulte sobre direitos, deveres, cotas, penalidades e programas de aprendizagem profissional do Catálogo Nacional (CONAP).")
    
    st.markdown("""
    <div class="novo-banner">
        📋 NOVO! Integração com CONAP - Consulte programas, CBOs, Sistema S (SENAI, SENAC, SENAT, SENAR) e arcos ocupacionais!
    </div>
    """, unsafe_allow_html=True)
    
    # Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibir mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua pergunta sobre legislação da aprendizagem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Consultando base jurídica e CONAP..."):
                try:
                    resposta = buscar_resposta_completa(prompt)
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                except Exception as e:
                    error_msg = f"Desculpe, ocorreu um erro: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Limpar Chat", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat limpo!")
    
    with col2:
        st.markdown("**📚 Base Legal**")
        st.caption("Lei 10.097/2000, CLT, CF/88")
    
    with col3:
        st.markdown("**📞 Suporte**")
        st.caption("Sistema LexAprendiz v2.0")

def main():
    """Função principal"""
    try:
        # Aplica tema se disponível
        if AUTH_AVAILABLE:
            apply_theme()
        
        # Sistema de autenticação
        if AUTH_AVAILABLE and not is_authenticated():
            show_auth_interface()
            return
        
        # Interface principal
        if AUTH_AVAILABLE:
            show_main_interface()
        else:
            # Modo simplificado se auth não estiver disponível
            show_chat_interface()
            
    except Exception as e:
        st.error(f"⚠️ Erro na aplicação: {str(e)}")
        st.info("🔄 Recarregue a página")
        
        # Fallback
        st.markdown("# ⚖️ LexAprendiz")
        st.markdown("### Sistema temporariamente em manutenção")

if __name__ == "__main__":
    main()
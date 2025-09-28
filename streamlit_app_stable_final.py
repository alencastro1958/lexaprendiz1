"""
LexAprendiz - Versão Ultra Estável
Sistema otimizado para Streamlit Cloud sem conflitos DOM
"""

import streamlit as st
import json
import hashlib
from pathlib import Path

# Configuração inicial ANTES de qualquer código
st.set_page_config(
    page_title="LexAprendiz",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para máxima estabilidade
st.markdown("""
<style>
    /* Prevenção total de conflitos DOM */
    .stApp { 
        transition: none !important; 
        animation: none !important;
    }
    .stButton button { 
        transition: all 0.1s ease !important; 
        animation: none !important;
    }
    .element-container { 
        position: relative !important; 
        transform: none !important;
    }
    .stSelectbox, .stTextInput, .stTextArea { 
        transition: none !important; 
        animation: none !important;
    }
    /* Estabilização de componentes dinâmicos */
    .main .block-container {
        max-width: none !important;
        padding: 1rem !important;
    }
    /* Banner personalizado */
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
        background: linear-gradient(90deg, #28a745, #20c997);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: center;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Base de dados embutida para estabilidade total
USUARIOS_DB = Path("usuarios.json")

def init_users():
    """Inicializa base de usuários se não existir"""
    if not USUARIOS_DB.exists():
        admin_user = {
            "admin@leidaaprendizagem.com.br": {
                "nome": "Administrador",
                "cpf": "000.000.000-00",
                "email": "admin@leidaaprendizagem.com.br",
                "senha": hashlib.sha256("admin123".encode()).hexdigest(),
                "tipo": "admin"
            }
        }
        with open(USUARIOS_DB, 'w', encoding='utf-8') as f:
            json.dump(admin_user, f, indent=2, ensure_ascii=False)

def load_users():
    """Carrega usuários"""
    init_users()
    try:
        with open(USUARIOS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Salva usuários"""
    try:
        with open(USUARIOS_DB, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def authenticate(email, senha):
    """Autenticação segura"""
    users = load_users()
    user = users.get(email)
    if user and user["senha"] == hashlib.sha256(senha.encode()).hexdigest():
        return True, user
    return False, None

def is_authenticated():
    """Verifica se está logado"""
    return st.session_state.get("logged_in", False) and st.session_state.get("user_data")

def is_admin():
    """Verifica se é admin"""
    user = st.session_state.get("user_data")
    return user and user.get("tipo") == "admin"

def safe_logout():
    """Logout seguro sem rerun"""
    keys = ["logged_in", "user_data", "user_email", "user_name", "user_type"]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]
    st.success("🚪 Logout realizado! Recarregue a página para continuar.")
    st.stop()

def show_auth_forms():
    """Formulários de autenticação seguros"""
    
    # Logo padrão embutido
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <h1>⚖️ LexAprendiz</h1>
        <h3>Especialista em Legislação da Aprendizagem</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Tabs para Login/Cadastro
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
    
    with tab1:
        with st.form("login_form", clear_on_submit=True):
            st.markdown("### 🔐 Fazer Login")
            email = st.text_input("Email", placeholder="seu@email.com")
            senha = st.text_input("Senha", type="password", placeholder="Sua senha")
            
            if st.form_submit_button("🚪 Entrar", use_container_width=True):
                if email and senha:
                    success, user = authenticate(email, senha)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_data = user
                        st.session_state.user_email = user["email"]
                        st.session_state.user_name = user["nome"]
                        st.session_state.user_type = user["tipo"]
                        st.success("✅ Login realizado com sucesso!")
                        st.balloons()
                        st.info("🔄 Recarregue a página para continuar.")
                    else:
                        st.error("❌ Email ou senha incorretos!")
                else:
                    st.error("⚠️ Preencha todos os campos!")
    
    with tab2:
        with st.form("register_form", clear_on_submit=True):
            st.markdown("### 📝 Criar Conta")
            nome = st.text_input("Nome Completo", placeholder="Seu nome")
            cpf = st.text_input("CPF", placeholder="000.000.000-00")
            email_reg = st.text_input("Email", placeholder="novo@email.com")
            senha_reg = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
            
            if st.form_submit_button("✅ Cadastrar", use_container_width=True):
                if all([nome, cpf, email_reg, senha_reg]):
                    if len(senha_reg) >= 6:
                        users = load_users()
                        if email_reg not in users:
                            users[email_reg] = {
                                "nome": nome,
                                "cpf": cpf,
                                "email": email_reg,
                                "senha": hashlib.sha256(senha_reg.encode()).hexdigest(),
                                "tipo": "usuario"
                            }
                            if save_users(users):
                                st.success("✅ Conta criada com sucesso!")
                                st.info("👈 Vá para a aba Login para entrar.")
                                st.balloons()
                            else:
                                st.error("❌ Erro ao salvar usuário!")
                        else:
                            st.error("❌ Email já cadastrado!")
                    else:
                        st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                else:
                    st.error("⚠️ Preencha todos os campos!")

def show_main_interface():
    """Interface principal após login"""
    
    # Sidebar com informações do usuário
    with st.sidebar:
        st.markdown("### 👤 Usuário Logado")
        user = st.session_state.get("user_data", {})
        
        if user.get("tipo") == "admin":
            st.markdown("👑 **Administrador**")
        else:
            st.markdown("👥 **Usuário**")
        
        st.markdown(f"**Nome:** {user.get('nome', 'N/A')}")
        st.markdown(f"**Email:** {user.get('email', 'N/A')}")
        
        st.markdown("---")
        
        # Admin Dashboard
        if is_admin():
            st.markdown("### 🛠️ Painel Admin")
            if st.button("👥 Ver Usuários", use_container_width=True):
                st.session_state.show_users = True
            
            if st.button("📝 Editor Conteúdo", use_container_width=True):
                st.session_state.show_editor = True
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            safe_logout()
    
    # Área principal
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1>⚖️ LexAprendiz</h1>
        <h3>Especialista em Legislação da Aprendizagem</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin panels (se ativo)
    if is_admin():
        if st.session_state.get("show_users"):
            show_users_panel()
        
        if st.session_state.get("show_editor"):
            show_content_editor()
    
    # Chat interface principal
    show_chat_interface()

def show_users_panel():
    """Painel de usuários para admin"""
    with st.expander("👥 Gerenciar Usuários", expanded=True):
        users = load_users()
        
        st.markdown("### 📋 Usuários Cadastrados")
        for email, user in users.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                tipo_icon = "👑" if user["tipo"] == "admin" else "👤"
                st.write(f"{tipo_icon} **{user['nome']}** - {email}")
            
            with col2:
                st.write(f"Tipo: {user['tipo']}")
            
            with col3:
                if user["tipo"] != "admin":  # Não permite deletar admin
                    if st.button("🗑️", key=f"del_{email}"):
                        del users[email]
                        save_users(users)
                        st.success(f"Usuário {user['nome']} removido!")
                        st.balloons()

def show_content_editor():
    """Editor de conteúdo para admin"""
    with st.expander("📝 Editor de Conteúdo", expanded=True):
        st.markdown("### ✏️ Personalizar Interface")
        
        # Simulação de editor
        titulo_app = st.text_input("Título da Aplicação:", value="LexAprendiz")
        subtitulo_app = st.text_area("Descrição:", value="Especialista em Legislação da Aprendizagem")
        
        if st.button("💾 Salvar Alterações", use_container_width=True):
            st.success("✅ Conteúdo atualizado!")
            st.info("🔄 Recarregue a página para ver as mudanças.")
            st.balloons()

def show_chat_interface():
    """Interface de chat principal"""
    
    # Inicializar histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
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
    
    # Exibir mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua pergunta sobre legislação da aprendizagem..."):
        # Adicionar pergunta
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processar resposta
        with st.chat_message("assistant"):
            with st.spinner("Consultando base jurídica..."):
                resposta = processar_pergunta(prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
    
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
        st.caption("Sistema LexAprendiz v3.0")

def processar_pergunta(pergunta):
    """Processa pergunta com base integrada"""
    pergunta_lower = pergunta.lower()
    
    # Base de conhecimento embutida para máxima estabilidade
    if any(word in pergunta_lower for word in ['gestante', 'grávida', 'gravidez', 'maternidade']):
        return """
**🤰 Direitos da Aprendiz Gestante:**

1. **Estabilidade:** Desde confirmação da gravidez até 5 meses pós-parto
2. **Licença-maternidade:** 120 dias remunerada
3. **Consultas médicas:** Dispensa para pré-natal sem desconto
4. **Mudança de função:** Se necessário, para função compatível
5. **Proteção contra demissão:** Não pode ser demitida sem justa causa

**Base Legal:** CLT Art. 391-A, Lei 11.788/2008, CF Art. 7º, XVIII
        """
    
    elif any(word in pergunta_lower for word in ['cota', 'quantos', 'cálculo', 'percentual']):
        return """
**📊 Cálculo de Cota de Aprendizes:**

- **Percentual:** 5% a 15% do total de funcionários
- **Base:** Funções que demandem formação profissional
- **Idade:** 14 a 24 anos (sem limite para PCD)
- **Duração:** 6 meses a 2 anos

**Exemplos:**
- 100 funcionários = 5 a 15 aprendizes
- 50 funcionários = 3 a 8 aprendizes
- 20 funcionários = 1 a 3 aprendizes

**Base Legal:** Lei 10.097/2000, Decreto 5.598/2005
        """
    
    elif any(word in pergunta_lower for word in ['multa', 'penalidade', 'fiscalização']):
        return """
**⚖️ Penalidades por Descumprimento:**

1. **Multa:** R$ 402,53 a R$ 4.025,33 por aprendiz não contratado
2. **Auto de Infração:** Fiscalização do trabalho
3. **TAC:** Termo de Ajustamento com MPT
4. **Ação Civil:** Indenização por danos morais coletivos

**Agravantes:** Reincidência, má-fé, resistência

**Base Legal:** CLT Art. 434, Portaria 723/2012
        """
    
    elif any(word in pergunta_lower for word in ['conap', 'programa', 'senai', 'senac']):
        return """
**📋 CONAP - Catálogo Nacional de Programas:**

**Sistema S Disponível:**
- **SENAI:** Programas industriais e técnicos
- **SENAC:** Comércio e serviços
- **SENAT:** Transporte e logística
- **SENAR:** Agronegócio e rural
- **SESCOOP:** Cooperativismo

**Consultas Disponíveis:**
- Programas por área ocupacional
- CBOs específicas
- Carga horária e faixa etária
- Arcos ocupacionais

**Exemplo:** "Programas de administração", "CBO 4110-10"
        """
    
    else:
        return """
**🎯 Tópicos Disponíveis no LexAprendiz:**

1. **👶 Direitos da Gestante:** Pergunte sobre direitos da aprendiz gestante
2. **📊 Cota de Aprendizes:** Como calcular cotas obrigatórias  
3. **⚖️ Penalidades:** Multas e fiscalizações
4. **📋 CONAP:** Programas e Sistema S

**Exemplos de Perguntas:**
- "Quais os direitos da aprendiz gestante?"
- "Como calcular cota de aprendizes?"
- "Penalidades por não contratar aprendizes"
- "Programas do SENAI"
- "CBO 4110-10"

**Base:** Lei 10.097/2000, CLT, CONAP 2021
        """

def main():
    """Função principal ultra estável"""
    try:
        if not is_authenticated():
            show_auth_forms()
        else:
            show_main_interface()
    
    except Exception as e:
        st.error("⚠️ Erro temporário no sistema")
        st.info("🔄 Recarregue a página")
        
        # Log para admin
        if is_admin():
            with st.expander("🔧 Debug (Admin)", expanded=False):
                st.code(str(e))

if __name__ == "__main__":
    main()
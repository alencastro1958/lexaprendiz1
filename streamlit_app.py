"""
LexAprendiz - Sistema Minimalista para Máxima Compatibilidade
Versão otimizada para resolver limite de inotify no Streamlit Cloud
"""

import streamlit as st
import json
import hashlib
import os

# Desabilita warnings e logs excessivos
import logging
logging.getLogger().setLevel(logging.ERROR)

# Configuração mínima
st.set_page_config(
    page_title="LexAprendiz",
    page_icon="⚖️", 
    layout="wide"
)

# CSS ultra simplificado
st.markdown("""
<style>
.stApp { background-color: #ffffff; }
.main { padding: 1rem; }
</style>
""", unsafe_allow_html=True)

# Base de usuários expandida com múltiplas credenciais válidas
VALID_USERS = {
    "admin@leidaaprendizagem.com.br": {
        "senha": "21232f297a57a5a743894a0e4a801fc3",  # admin123
        "nome": "Administrador Principal",
        "tipo": "admin"
    },
    "diogo@leidaaprendizagem.com.br": {
        "senha": "21232f297a57a5a743894a0e4a801fc3",  # admin123
        "nome": "Diogo Alencastro", 
        "tipo": "admin"
    },
    "alencastro1958@gmail.com": {
        "senha": "21232f297a57a5a743894a0e4a801fc3",  # admin123
        "nome": "Diogo Alencastro",
        "tipo": "admin"
    }
}

# Credenciais de emergência (texto puro para recuperação)
EMERGENCY_CREDENTIALS = {
    "emails": ["admin@leidaaprendizagem.com.br", "diogo@leidaaprendizagem.com.br", "alencastro1958@gmail.com"],
    "senhas": ["admin123", "lexaprendiz2024", "diogo123"],
    "admin_master": "admin123"
}

def authenticate(email, senha):
    """Autenticação expandida com múltiplas opções"""
    # Normalizar email
    email = email.lower().strip()
    
    # Verificar usuários cadastrados
    if email in VALID_USERS:
        senha_hash = hashlib.md5(senha.encode()).hexdigest()
        if senha_hash == VALID_USERS[email]["senha"]:
            user_data = VALID_USERS[email].copy()
            user_data["email"] = email
            return True, user_data
    
    # Verificar credenciais de emergência (senhas em texto puro)
    if email in EMERGENCY_CREDENTIALS["emails"]:
        if senha in EMERGENCY_CREDENTIALS["senhas"]:
            return True, {
                "email": email,
                "nome": "Usuário Autorizado",
                "tipo": "admin"
            }
    
    return False, None

def is_logged():
    """Verifica login"""
    return st.session_state.get("logged_in", False)

def is_admin():
    """Verifica se é admin"""
    user = st.session_state.get("user_data")
    return user and user.get("tipo") == "admin"

def show_login():
    """Tela de login com sistema de recuperação"""
    
    st.markdown("# ⚖️ LexAprendiz")
    st.markdown("### Especialista em Legislação da Aprendizagem")
    
    st.info("🎯 **Especialista em Legislação Brasileira da Aprendizagem + CONAP**")
    st.success("📋 **Integração com CONAP** - Consulte programas, CBOs, Sistema S (SENAI, SENAC, SENAT, SENAR)")
    
    # Tabs para Login e Recuperação
    tab1, tab2 = st.tabs(["🔐 Login", "🔑 Recuperar Acesso"])
    
    with tab1:
        with st.form("login"):
            st.subheader("🔐 Acesso ao Sistema")
            email = st.text_input("Email:", placeholder="Seu email de acesso")
            senha = st.text_input("Senha:", type="password", placeholder="Sua senha")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("🚪 Entrar", use_container_width=True):
                    if email and senha:
                        success, user = authenticate(email, senha)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_data = user
                            st.success("✅ Login realizado!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Credenciais inválidas!")
                            st.info("💡 Tente a aba 'Recuperar Acesso' se esqueceu suas credenciais")
                    else:
                        st.error("⚠️ Preencha todos os campos!")
            
            with col2:
                if st.form_submit_button("🔑 Esqueci minha senha", use_container_width=True):
                    st.session_state.show_recovery = True
                    st.rerun()
    
    with tab2:
        show_recovery_system()

def show_recovery_system():
    """Sistema de recuperação de credenciais"""
    st.subheader("🔑 Sistema de Recuperação de Acesso")
    
    st.warning("⚠️ **ATENÇÃO:** Este sistema exibe credenciais para recuperação de acesso administrativo.")
    
    # Verificação de segurança simples
    with st.form("recovery_form"):
        st.markdown("**Responda a pergunta de segurança para recuperar o acesso:**")
        
        pergunta = st.selectbox(
            "Qual é o nome do sistema?",
            ["Selecione...", "LexAprendiz", "Streamlit", "Python", "Django"]
        )
        
        verificacao = st.text_input("Digite 'RECUPERAR' em maiúsculas para confirmar:")
        
        if st.form_submit_button("🔍 Mostrar Credenciais", use_container_width=True):
            if pergunta == "LexAprendiz" and verificacao == "RECUPERAR":
                show_credentials_recovery()
            else:
                st.error("❌ Verificação de segurança falhou!")

def show_credentials_recovery():
    """Exibe credenciais de recuperação"""
    st.success("✅ **Verificação aprovada! Credenciais de acesso:**")
    
    with st.container():
        st.markdown("### 👑 **Credenciais de Administrador:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📧 Emails válidos:**")
            st.code("admin@leidaaprendizagem.com.br")
            st.code("diogo@leidaaprendizagem.com.br")  
            st.code("alencastro1958@gmail.com")
        
        with col2:
            st.markdown("**🔑 Senhas válidas:**")
            st.code("admin123")
            st.code("lexaprendiz2024")
            st.code("diogo123")
    
    st.info("💡 **Como usar:** Escolha qualquer email + qualquer senha da lista acima")
    
    # Botão de teste rápido
    st.markdown("### 🚀 **Teste Rápido:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Testar Admin Principal", use_container_width=True):
            test_login("admin@leidaaprendizagem.com.br", "admin123")
    
    with col2:
        if st.button("🎯 Testar Diogo", use_container_width=True):
            test_login("diogo@leidaaprendizagem.com.br", "admin123")
    
    with col3:
        if st.button("🎯 Testar Alternativo", use_container_width=True):
            test_login("alencastro1958@gmail.com", "lexaprendiz2024")

def test_login(email, senha):
    """Testa login automático"""
    success, user = authenticate(email, senha)
    if success:
        st.session_state.logged_in = True
        st.session_state.user_data = user
        st.success(f"✅ Login automático realizado como {user['nome']}!")
        st.balloons()
        st.rerun()
    else:
        st.error("❌ Erro no login automático!")

def show_main():
    """Interface principal"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Usuário")
        user = st.session_state.get("user_data", {})
        
        if user.get("tipo") == "admin":
            st.markdown("👑 **Administrador**")
        
        st.markdown(f"**{user.get('nome', 'Usuário')}**")
        st.markdown(f"_{user.get('email', 'N/A')}_")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["logged_in", "user_data"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Área principal
    st.markdown("# ⚖️ LexAprendiz")
    st.markdown("### Especialista em Legislação da Aprendizagem")
    
    st.info("🎯 **Especialista em Legislação Brasileira da Aprendizagem + CONAP**")
    st.success("📋 **NOVO!** Integração com CONAP - Consulte programas, CBOs, Sistema S (SENAI, SENAC, SENAT, SENAR) e arcos ocupacionais!")
    
    # Admin Panel
    if is_admin():
        with st.expander("🛠️ Painel Administrativo", expanded=False):
            st.markdown("### 👑 Ferramentas de Administração")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Dashboard", use_container_width=True):
                    st.info("Dashboard em desenvolvimento")
            
            with col2:
                if st.button("⚙️ Configurações", use_container_width=True):
                    st.info("Configurações em desenvolvimento")
            
            st.markdown("**Status do Sistema:**")
            st.success("✅ Aplicação funcionando normalmente")
            st.info("🔧 Versão ultra-estável ativa")
    
    # Chat Interface
    show_chat()

def show_chat():
    """Interface de chat"""
    
    # Inicializar histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar mensagens
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua pergunta sobre legislação da aprendizagem..."):
        
        # Adicionar pergunta
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Gerar resposta
        with st.chat_message("assistant"):
            with st.spinner("Consultando base jurídica..."):
                resposta = get_response(prompt)
                st.write(resposta)
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
        st.caption("Sistema LexAprendiz v4.0")

def get_response(pergunta):
    """Base de conhecimento embutida"""
    p = pergunta.lower()
    
    if any(word in p for word in ['gestante', 'grávida', 'gravidez']):
        return """**🤰 Direitos da Aprendiz Gestante:**
        
1. **Estabilidade:** Desde confirmação da gravidez até 5 meses pós-parto
2. **Licença-maternidade:** 120 dias remunerada  
3. **Consultas médicas:** Dispensa para pré-natal sem desconto
4. **Mudança de função:** Se necessário, para função compatível
5. **Proteção:** Não pode ser demitida sem justa causa

**Base Legal:** CLT Art. 391-A, Lei 11.788/2008"""
    
    elif any(word in p for word in ['cota', 'quantos', 'cálculo']):
        return """**📊 Cálculo de Cota de Aprendizes:**

- **Percentual:** 5% a 15% do total de funcionários
- **Base:** Funções que demandem formação profissional
- **Idade:** 14 a 24 anos (sem limite para PCD)
- **Duração:** 6 meses a 2 anos

**Exemplos:**
- 100 funcionários = 5 a 15 aprendizes
- 50 funcionários = 3 a 8 aprendizes

**Base Legal:** Lei 10.097/2000, Decreto 5.598/2005"""
    
    elif any(word in p for word in ['multa', 'penalidade', 'fiscalização']):
        return """**⚖️ Penalidades por Descumprimento:**

1. **Multa:** R$ 402,53 a R$ 4.025,33 por aprendiz não contratado
2. **Auto de Infração:** Fiscalização do trabalho
3. **TAC:** Termo de Ajustamento com MPT
4. **Ação Civil:** Indenização por danos morais coletivos

**Base Legal:** CLT Art. 434, Portaria 723/2012"""
    
    elif any(word in p for word in ['conap', 'programa', 'senai', 'senac']):
        return """**📋 CONAP - Catálogo Nacional:**

**Sistema S Disponível:**
- **SENAI:** Programas industriais e técnicos
- **SENAC:** Comércio e serviços  
- **SENAT:** Transporte e logística
- **SENAR:** Agronegócio e rural
- **SESCOOP:** Cooperativismo

**Consultas:** Programas por área, CBOs, carga horária, faixa etária"""
    
    else:
        return """**🎯 Tópicos Disponíveis:**

1. **👶 Direitos da Gestante:** "Quais os direitos da aprendiz gestante?"
2. **📊 Cota de Aprendizes:** "Como calcular cota de aprendizes?"  
3. **⚖️ Penalidades:** "Penalidades por não contratar aprendizes"
4. **📋 CONAP:** "Programas do SENAI", "CBO 4110-10"

**Base:** Lei 10.097/2000, CLT, CONAP 2021"""

def main():
    """Função principal ultra-simplificada"""
    try:
        if not is_logged():
            show_login()
        else:
            show_main()
    except Exception as e:
        st.error("⚠️ Erro temporário no sistema")
        st.info("🔄 Recarregue a página")

if __name__ == "__main__":
    main()
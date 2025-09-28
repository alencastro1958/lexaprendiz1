"""
Sistema de Autenticação do LexAprendiz
Gerencia login, cadastro e controle de acesso
"""

import streamlit as st
import hashlib
import json
from pathlib import Path
import re
from app_stability import safe_logout, safe_state_update, prevent_dom_conflicts

# Arquivo para armazenar usuários
USERS_FILE = Path("users_database.json")

def init_users_database():
    """Inicializa o banco de dados de usuários"""
    if not USERS_FILE.exists():
        # Cria admin padrão
        default_users = {
            "admin@leidaaprendizagem.com.br": {
                "nome": "Administrador",
                "cpf": "000.000.000-00",
                "email": "admin@leidaaprendizagem.com.br",
                "senha": hash_password("admin123"),
                "tipo": "admin",
                "data_cadastro": "2025-09-28"
            }
        }
        
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_users, f, indent=4, ensure_ascii=False)
    
    return load_users()

def load_users():
    """Carrega usuários do arquivo"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Salva usuários no arquivo"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def hash_password(password):
    """Hash da senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Valida formato do email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_cpf(cpf):
    """Validação básica de CPF (formato)"""
    # Remove pontos e hífens
    cpf_numbers = re.sub(r'[^0-9]', '', cpf)
    return len(cpf_numbers) == 11

def format_cpf(cpf):
    """Formata CPF com pontos e hífen"""
    cpf_numbers = re.sub(r'[^0-9]', '', cpf)
    if len(cpf_numbers) == 11:
        return f"{cpf_numbers[:3]}.{cpf_numbers[3:6]}.{cpf_numbers[6:9]}-{cpf_numbers[9:]}"
    return cpf

def register_user(nome, cpf, email, senha, tipo="usuario"):
    """Registra novo usuário"""
    users = load_users()
    
    if email in users:
        return False, "Email já cadastrado!"
    
    if not validate_email(email):
        return False, "Email inválido!"
    
    if not validate_cpf(cpf):
        return False, "CPF inválido!"
    
    if len(senha) < 6:
        return False, "Senha deve ter pelo menos 6 caracteres!"
    
    users[email] = {
        "nome": nome,
        "cpf": format_cpf(cpf),
        "email": email,
        "senha": hash_password(senha),
        "tipo": tipo,
        "data_cadastro": "2025-09-28"
    }
    
    save_users(users)
    return True, "Usuário cadastrado com sucesso!"

def authenticate_user(email, senha):
    """Autentica usuário"""
    users = load_users()
    
    if email not in users:
        return False, None, "Email não encontrado!"
    
    user = users[email]
    if user["senha"] != hash_password(senha):
        return False, None, "Senha incorreta!"
    
    return True, user, "Login realizado com sucesso!"

def is_admin(user):
    """Verifica se usuário é admin"""
    return user and user.get("tipo") == "admin"

def logout_user():
    """Realiza logout do usuário"""
    keys_to_remove = ["logged_in", "user_data", "user_email", "user_name", "user_type"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

def show_login_form():
    """Exibe formulário de login"""
    st.markdown("### 🔐 Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="seu@email.com")
        senha = st.text_input("Senha", type="password", placeholder="Sua senha")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🚪 Entrar", use_container_width=True)
        with col2:
            if st.form_submit_button("📝 Criar Conta", use_container_width=True):
                st.session_state.show_register = True
        
        if login_button:
            if email and senha:
                success, user_data, message = authenticate_user(email, senha)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.session_state.user_email = user_data["email"]
                    st.session_state.user_name = user_data["nome"]
                    st.session_state.user_type = user_data["tipo"]
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)
            else:
                st.error("Preencha todos os campos!")

def show_register_form():
    """Exibe formulário de cadastro"""
    st.markdown("### 📝 Criar Nova Conta")
    
    with st.form("register_form"):
        nome = st.text_input("Nome Completo", placeholder="Seu nome completo")
        cpf = st.text_input("CPF", placeholder="000.000.000-00")
        email = st.text_input("Email", placeholder="seu@email.com")
        senha = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
        confirmar_senha = st.text_input("Confirmar Senha", type="password", placeholder="Confirme sua senha")
        
        col1, col2 = st.columns(2)
        with col1:
            register_button = st.form_submit_button("✅ Cadastrar", use_container_width=True)
        with col2:
            if st.form_submit_button("🔙 Voltar ao Login", use_container_width=True):
                st.session_state.show_register = False
        
        if register_button:
            if all([nome, cpf, email, senha, confirmar_senha]):
                if senha != confirmar_senha:
                    st.error("Senhas não coincidem!")
                else:
                    success, message = register_user(nome, cpf, email, senha)
                    
                    if success:
                        st.success(message)
                        st.info("Agora você pode fazer login!")
                        st.session_state.show_register = False
                        st.balloons()
                    else:
                        st.error(message)
            else:
                st.error("Preencha todos os campos!")

def show_admin_dashboard():
    """Exibe dashboard administrativo"""
    st.markdown("### 🛠️ Dashboard Administrativo")
    
    # Editor de Conteúdo (só para admin)
    with st.expander("✏️ Editor de Conteúdo", expanded=False):
        from content_manager import show_content_editor
        show_content_editor()
    
    # Upload de Logo (só para admin)
    with st.expander("📎 Gerenciar Logo do Sistema", expanded=False):        
        from logo_base64 import show_logo_uploader
        show_logo_uploader()
    
    # Estatísticas de usuários
    with st.expander("👥 Usuários Cadastrados", expanded=False):
        users = load_users()
        
        total_users = len(users)
        admin_count = sum(1 for u in users.values() if u.get("tipo") == "admin")
        user_count = total_users - admin_count
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Usuários", total_users)
        with col2:
            st.metric("Administradores", admin_count)
        with col3:
            st.metric("Usuários Comuns", user_count)
        
        if st.button("📋 Ver Lista de Usuários"):
            st.markdown("**Lista de Usuários:**")
            for email, user in users.items():
                tipo_icon = "👑" if user.get("tipo") == "admin" else "👤"
                st.write(f"{tipo_icon} **{user['nome']}** - {email} - {user.get('tipo', 'usuario').title()}")

def require_authentication():
    """Middleware de autenticação"""
    # Inicializa banco de usuários
    init_users_database()
    
    # Verifica se está logado
    if not st.session_state.get("logged_in", False):
        from content_manager import get_content
        
        login_title = get_content("login_title", "🔒 Acesso Restrito")
        login_subtitle = get_content("login_subtitle", "Esta área requer autenticação. Faça login ou crie uma conta para continuar.")
        
        st.markdown(f"""
        <div style="text-align: center; padding: 50px;">
            <h1>{login_title}</h1>
            <p>{login_subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Controla exibição entre login e cadastro
        if st.session_state.get("show_register", False):
            show_register_form()
        else:
            show_login_form()
        
        return False
    
    return True

def show_user_info():
    """Exibe informações do usuário logado"""
    if st.session_state.get("logged_in", False):
        user_name = st.session_state.get("user_name", "Usuário")
        user_type = st.session_state.get("user_type", "usuario")
        
        # Ícone baseado no tipo de usuário
        icon = "👑" if user_type == "admin" else "👤"
        
        st.markdown(f"**{icon} {user_name}**")
        st.markdown(f"*{user_type.title()}*")
        
        if st.button("🚪 Logout", use_container_width=True):
            safe_logout()
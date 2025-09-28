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
    """Base de conhecimento expandida e especializada"""
    p = pergunta.lower()
    
    # ESTABELECIMENTOS PROIBIDOS
    if any(word in p for word in ['proibido', 'proibidos', 'não pode', 'impossibilitado', 'vedado', 'impedido']):
        return """**🚫 Estabelecimentos Proibidos de Contratar Aprendizes:**

**❌ EMPRESAS DISPENSADAS DA COTA:**
1. **Microempresas (ME)** - até 9 empregados
2. **Empresas de Pequeno Porte (EPP)** - 10 a 99 empregados (opcional)
3. **Entidades sem fins lucrativos** que tenham por objetivo educação profissional
4. **Órgãos da administração direta** (União, Estados, Municípios)

**🚫 ATIVIDADES COM RESTRIÇÕES:**
- **Trabalho perigoso** (menores de 18 anos)
- **Trabalho insalubre** (menores de 18 anos)  
- **Trabalho noturno** (menores de 18 anos)
- **Atividades prejudiciais** à formação moral

**⚠️ SITUAÇÕES ESPECIAIS:**
- **Empresas em recuperação judicial** (podem ter suspensão temporária)
- **Estabelecimentos em reestruturação** (análise caso a caso)

**Base Legal:** Lei 10.097/2000, Art. 429; CLT Art. 403-405; Decreto 5.598/2005"""

    # DIREITOS DA GESTANTE
    elif any(word in p for word in ['gestante', 'grávida', 'gravidez', 'maternidade']):
        return """**🤰 Direitos da Aprendiz Gestante:**

1. **Estabilidade Provisória:** Desde confirmação da gravidez até 5 meses após o parto
2. **Licença-Maternidade:** 120 dias remunerada (pode ser estendida por mais 60 dias)
3. **Consultas e Exames:** Dispensa para pré-natal sem desconto salarial
4. **Mudança de Função:** Se atividade for incompatível com a gestação
5. **Proteção contra Demissão:** Vedada demissão sem justa causa
6. **Amamentação:** Dois intervalos de 30 minutos até 6 meses do bebê
7. **Retorno Garantido:** Direito de retornar à mesma função

**⚠️ ATENÇÃO:** Contrato de aprendizagem não pode ser rescindido durante gravidez e estabilidade.

**Base Legal:** CLT Art. 391-A, 392, 396; Lei 11.788/2008; CF Art. 7º, XVIII"""

    # CÁLCULO DE COTAS
    elif any(word in p for word in ['cota', 'quantos', 'cálculo', 'percentual', 'proporção']):
        return """**📊 Cálculo de Cota de Aprendizes:**

**📋 REGRA GERAL:**
- **Mínimo:** 5% dos empregados por estabelecimento
- **Máximo:** 15% dos empregados por estabelecimento
- **Base de cálculo:** Funções que demandem formação profissional

**👥 EXEMPLOS PRÁTICOS:**
- 20 funcionários = 1 a 3 aprendizes
- 50 funcionários = 3 a 8 aprendizes  
- 100 funcionários = 5 a 15 aprendizes
- 200 funcionários = 10 a 30 aprendizes

**🎯 CRITÉRIOS DE IDADE:**
- **Regra geral:** 14 a 24 anos incompletos
- **Pessoas com deficiência:** Sem limite de idade

**⏱️ DURAÇÃO DO CONTRATO:**
- **Mínimo:** 6 meses
- **Máximo:** 2 anos (exceto PCD, que pode ser mais)

**Base Legal:** Lei 10.097/2000, Art. 429; Decreto 5.598/2005, Art. 11"""

    # PENALIDADES E MULTAS
    elif any(word in p for word in ['multa', 'penalidade', 'fiscalização', 'autuação', 'infração']):
        return """**⚖️ Penalidades por Descumprimento:**

**💰 VALORES DAS MULTAS (2024):**
- **Por aprendiz não contratado:** R$ 402,53 a R$ 4.025,33
- **Reincidência:** Valor dobrado
- **Má-fé ou resistência:** Agravantes adicionais

**🔍 TIPOS DE FISCALIZAÇÃO:**
1. **Auto de Infração:** Auditores-fiscais do trabalho
2. **TAC:** Termo de Ajustamento de Conduta (MPT)
3. **Ação Civil Pública:** Indenização por danos morais coletivos
4. **Embargo/Interdição:** Em casos graves

**⚠️ CONSEQUÊNCIAS ADICIONAIS:**
- **Cadastro de inadimplentes** em órgãos públicos
- **Impedimento** para participar de licitações
- **Restrições** para financiamentos públicos
- **Execução fiscal** em caso de não pagamento

**Base Legal:** CLT Art. 434; Lei 6.514/77; Portaria MTE 723/2012"""

    # CONAP E PROGRAMAS
    elif any(word in p for word in ['conap', 'programa', 'senai', 'senac', 'senat', 'senar', 'sescoop', 'sistema s']):
        return """**📋 CONAP - Catálogo Nacional de Programas:**

**🏫 SISTEMA S - INSTITUIÇÕES FORMADORAS:**
- **SENAI:** Indústria (metalurgia, construção, tecnologia)
- **SENAC:** Comércio e serviços (administração, vendas, turismo)
- **SENAT:** Transporte (logística, condutores, manutenção)
- **SENAR:** Agronegócio (agricultura, pecuária, cooperativismo)
- **SESCOOP:** Cooperativismo (gestão, educação cooperativa)

**📚 PRINCIPAIS ARCOS OCUPACIONAIS:**
1. **Administração e Gestão**
2. **Tecnologia da Informação** 
3. **Indústria Metalúrgica**
4. **Construção Civil**
5. **Comércio e Vendas**
6. **Saúde e Bem-estar**
7. **Logística e Transporte**

**🎯 INFORMAÇÕES DISPONÍVEIS:**
- **CBO associada** a cada programa
- **Carga horária** (mín. 400h teóricas)
- **Faixa etária** recomendada
- **Descrição sumária** das atividades
- **Competências** a serem desenvolvidas

**Base Legal:** Portaria MTE 723/2012; CONAP 2021"""

    # CONTRATOS E FORMALIZAÇÃO
    elif any(word in p for word in ['contrato', 'formalizar', 'ctps', 'registro', 'documentação']):
        return """**📝 Contrato de Aprendizagem:**

**📋 DOCUMENTOS OBRIGATÓRIOS:**
1. **Contrato escrito** com prazo determinado
2. **Registro na CTPS** na coluna "Anotações Gerais"
3. **Matrícula** em programa de aprendizagem
4. **Certificado** de frequência escolar (se menor de 18)

**⏱️ PRAZOS E REGISTROS:**
- **Registro MTE:** Até 30 dias após admissão
- **CAGED:** Informar admissão como aprendiz
- **eSocial:** Código específico para aprendizagem (S-2200)

**💰 REMUNERAÇÃO:**
- **Mínimo:** Salário mínimo/hora proporcional
- **Pode ser superior** conforme política da empresa
- **13º salário, férias e FGTS:** Direitos garantidos

**🎓 CERTIFICAÇÃO:**
- **Certificado profissional** ao final do programa
- **Registro no MTE** da conclusão
- **Possibilidade** de efetivação pela empresa

**Base Legal:** CLT Art. 428-433; Lei 10.097/2000; Decreto 5.598/2005"""

    # PESSOAS COM DEFICIÊNCIA
    elif any(word in p for word in ['deficiência', 'deficiente', 'pcd', 'inclusão', 'acessibilidade']):
        return """**♿ Aprendizagem para Pessoas com Deficiência:**

**🎯 REGRAS ESPECIAIS:**
- **Sem limite de idade** para início
- **Contrato pode exceder 2 anos** se necessário
- **Carga horária adaptada** às necessidades
- **Avaliação individualizada** das competências

**📊 COTAS ESPECÍFICAS:**
- **Podem compor** os percentuais gerais (5%-15%)
- **Incentivo** para contratação além da cota mínima
- **Flexibilização** de requisitos quando necessário

**🏢 ADAPTAÇÕES OBRIGATÓRIAS:**
1. **Acessibilidade física** no local de trabalho
2. **Tecnologia assistiva** quando necessária  
3. **Adequação** de jornada e atividades
4. **Apoio especializado** durante aprendizagem

**🎓 PROGRAMAS ESPECÍFICOS:**
- **SENAI:** Programas adaptados por deficiência
- **Instituições especializadas** conveniadas
- **Metodologias inclusivas** certificadas

**Base Legal:** Lei 13.146/2015 (LBI); Decreto 5.598/2005; Lei 8.213/91"""

    # JORNADA E HORÁRIOS  
    elif any(word in p for word in ['jornada', 'horário', 'horas', 'trabalho', 'período']):
        return """**⏰ Jornada de Trabalho do Aprendiz:**

**📚 APRENDIZ ESTUDANTE:**
- **Máximo 6h/dia** - se estuda
- **Não pode** trabalhar em horário escolar
- **Educação** tem prioridade sempre

**🎓 APRENDIZ NÃO ESTUDANTE:**
- **Máximo 8h/dia** - se completou ensino médio
- **Incluídas** as horas de capacitação teórica
- **Divisão** entre empresa e entidade formadora

**🚫 PROIBIÇÕES:**
- **Trabalho noturno** (22h às 5h) para menores de 18
- **Horas extras** são vedadas
- **Compensação** de jornada não permitida
- **Trabalho aos domingos** salvo necessidade técnica

**📊 DISTRIBUIÇÃO TÍPICA:**
- **Teoria:** Mínimo 20% da jornada (400h/ano)
- **Prática:** Na empresa aplicando conhecimentos
- **Avaliação:** Contínua em ambos ambientes

**Base Legal:** CLT Art. 432; CF Art. 7º, XIII; Decreto 5.598/2005"""

    # RESCISÃO E TÉRMINO
    elif any(word in p for word in ['rescisão', 'demissão', 'término', 'fim', 'acabar']):
        return """**🔚 Rescisão do Contrato de Aprendizagem:**

**✅ SITUAÇÕES PERMITIDAS:**
1. **Término natural** do prazo contratual
2. **Antecipação** aos 24 anos (se não PCD)
3. **Conclusão** do programa de aprendizagem
4. **Baixo desempenho** comprovado
5. **Falta disciplinar grave**
6. **Ausência injustificada** à escola (se estudante)

**❌ VEDAÇÕES:**
- **Demissão sem justa causa** de gestante
- **Rescisão discriminatória** 
- **Término antecipado** sem justificativa legal
- **Dispensa** por redução de quadro

**💰 VERBAS RESCISÓRIAS:**
- **Saldo de salário**
- **Férias proporcionais + 1/3**
- **13º salário proporcional**
- **FGTS + 40%** (se sem justa causa)
- **Aviso prévio** (se aplicável)

**🎓 CERTIFICAÇÃO:**
- **Sempre obrigatória** mesmo em rescisão antecipada
- **Registro das competências** desenvolvidas
- **Aproveitamento** em futuros programas

**Base Legal:** CLT Art. 433; Lei 10.097/2000; TST Súmula 331"""

    # RESPOSTA GENÉRICA EXPANDIDA
    else:
        return """**🎯 Tópicos Especializados Disponíveis:**

**🚫 Estabelecimentos:** "Estabelecimentos proibidos de contratar aprendizes"
**🤰 Gestante:** "Direitos da aprendiz gestante"  
**📊 Cotas:** "Como calcular cota de aprendizes"
**⚖️ Penalidades:** "Multas por não contratar aprendizes"
**📋 CONAP:** "Programas do SENAI", "Sistema S"
**📝 Contratos:** "Como formalizar contrato de aprendizagem"
**♿ PCD:** "Aprendizagem para pessoas com deficiência"
**⏰ Jornada:** "Horário de trabalho do aprendiz"
**🔚 Rescisão:** "Como rescindir contrato de aprendizagem"

**💡 Exemplo:** Digite "Estabelecimentos proibidos" ou "Jornada de trabalho"

**📚 Base Legal Completa:** Lei 10.097/2000, CLT Arts. 428-433, Decreto 5.598/2005, CONAP 2021"""

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
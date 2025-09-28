"""
LexAprendiz - Especialista em Legislação da Aprendizagem
Versão minimalista e estável para Streamlit Cloud
"""

import streamlit as st
import json
import hashlib
from pathlib import Path
from conap_database import consultar_conap

# Configuração da página
st.set_page_config(
    page_title="LexAprendiz",
    page_icon="⚖️",
    layout="wide"
)

# CSS para estabilidade
st.markdown("""
<style>
    .stApp { transition: none !important; }
    .main-header { text-align: center; margin-bottom: 2rem; }
    .chat-container { max-width: 800px; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)

# Banco de conhecimento simplificado
CONHECIMENTO_BASE = {
    "direitos_gestante": """
    **Direitos da Aprendiz Gestante:**
    
    1. **Estabilidade no Emprego:** A aprendiz gestante tem direito à estabilidade desde a confirmação da gravidez até 5 meses após o parto.
    
    2. **Licença-Maternidade:** 120 dias de licença-maternidade remunerada.
    
    3. **Consultas Médicas:** Dispensa para consultas pré-natais sem desconto no salário.
    
    4. **Mudança de Função:** Se necessário, pode ser transferida para função compatível com seu estado.
    
    5. **Rescisão:** Não pode ser demitida sem justa causa durante a gravidez e estabilidade.
    
    **Base Legal:** CLT Art. 391-A, Lei 11.788/2008, Constituição Federal Art. 7º, XVIII.
    """,
    
    "cota_aprendizes": """
    **Cálculo de Cota de Aprendizes:**
    
    - **5% a 15%** do total de funcionários em cada estabelecimento
    - **Base de cálculo:** Funções que demandem formação profissional
    - **Idade:** 14 a 24 anos (sem limite para pessoas com deficiência)
    - **Duração:** 6 meses a 2 anos
    
    **Exemplos:**
    - Empresa com 100 funcionários: mínimo 5, máximo 15 aprendizes
    - Empresa com 50 funcionários: mínimo 3, máximo 8 aprendizes
    
    **Base Legal:** Lei 10.097/2000, Decreto 5.598/2005.
    """,
    
    "penalidades": """
    **Penalidades por Descumprimento:**
    
    1. **Multa Administrativa:** R$ 402,53 a R$ 4.025,33 por aprendiz não contratado
    2. **Auto de Infração:** Emitido pela fiscalização do trabalho  
    3. **TAC:** Termo de Ajustamento de Conduta com o MPT
    4. **Ação Civil Pública:** Indenização por danos morais coletivos
    
    **Agravantes:**
    - Reincidência
    - Má-fé
    - Resistência à fiscalização
    
    **Base Legal:** CLT Art. 434, Portaria 723/2012.
    """
}

def buscar_resposta(pergunta):
    """Busca resposta na base de conhecimento integrada com CONAP"""
    pergunta_lower = pergunta.lower()
    
    # Primeiro verifica se é consulta do CONAP (programas, CBO, Sistema S, etc.)
    if any(word in pergunta_lower for word in ['programa', 'conap', 'cbo', 'senai', 'senac', 'senat', 'senar', 'sescoop', 'curso', 'aprendizagem profissional', 'ocupação']):
        resposta_conap = consultar_conap(pergunta)
        if resposta_conap:
            return resposta_conap
    
    # Mantém as consultas tradicionais de legislação
    if any(word in pergunta_lower for word in ['gestante', 'grávida', 'gravidez', 'maternidade']):
        return CONHECIMENTO_BASE['direitos_gestante']
    elif any(word in pergunta_lower for word in ['cota', 'quantos', 'cálculo', 'percentual']):
        return CONHECIMENTO_BASE['cota_aprendizes']
    elif any(word in pergunta_lower for word in ['multa', 'penalidade', 'fiscalização', 'punição']):
        return CONHECIMENTO_BASE['penalidades']
    else:
        return """
        **📚 LexAprendiz - Áreas de Consulta:**
        
        **🏛️ LEGISLAÇÃO:**
        1. **Direitos da Gestante:** Pergunte sobre direitos da aprendiz gestante
        2. **Cota de Aprendizes:** Pergunte sobre cálculo de cotas
        3. **Penalidades:** Pergunte sobre multas e fiscalização
        
        **📋 CONAP - PROGRAMAS DE APRENDIZAGEM:**
        4. **Programas por Área:** Administração, Indústria, TI, Construção, Saúde, etc.
        5. **Sistema S:** Cursos SENAI, SENAC, SENAT, SENAR, SESCOOP
        6. **CBOs e Ocupações:** Consulte por código CBO ou nome da ocupação
        7. **Arcos Ocupacionais:** Gestão, Indústria, Informação, Infraestrutura, etc.
        
        **💡 Exemplos de perguntas:**
        - "Quais os direitos da aprendiz gestante?"
        - "Como calcular a cota de aprendizes?"
        - "Programas de administração"
        - "Cursos do SENAI"
        - "CBO 4110-10"
        - "Programas para 16 anos"
        """

def main():
    """Interface principal"""
    
    # Cabeçalho
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("# ⚖️ LexAprendiz")
    st.markdown("### Especialista em Legislação da Aprendizagem")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Informações
    st.info("🎯 **Especialista em Legislação Brasileira da Aprendizagem + CONAP**\n\nConsulte sobre direitos, deveres, cotas, penalidades e **programas de aprendizagem profissional** do Catálogo Nacional (CONAP).")
    
    # Destaque CONAP
    st.success("📋 **NOVO!** Integração com CONAP - Consulte programas, CBOs, Sistema S (SENAI, SENAC, SENAT, SENAR) e arcos ocupacionais!")
    
    # Container do chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Inicializar histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
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
        
        # Gerar resposta
        with st.chat_message("assistant"):
            with st.spinner("Consultando legislação..."):
                resposta = buscar_resposta(prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("---")
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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("⚠️ Erro temporário no sistema")
        st.info("🔄 Recarregue a página")
        
        # Fallback básico
        st.markdown("# ⚖️ LexAprendiz")
        st.markdown("### Sistema em Manutenção")
        st.info("Por favor, tente novamente em alguns instantes.")
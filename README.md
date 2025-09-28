# LexAprendiz - Especialista em Legislação da Aprendizagem

Sistema inteligente especializado em legislação brasileira da aprendizagem profissional.

## 🚀 Deploy no Streamlit Cloud

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://lexaprendiz.streamlit.app)

## 📋 Funcionalidades

- ✅ **Autenticação Completa** - Sistema de login e cadastro
- ✅ **Dashboard Administrativo** - Controle total do sistema
- ✅ **Editor de Conteúdo** - Personalização de textos
- ✅ **Upload de Logo** - Branding personalizado
- ✅ **Temas Claro/Escuro** - Modo noturno disponível
- ✅ **Base de Conhecimento** - 80+ normativas (1943-2025)
- ✅ **Pesquisa Jurídica** - Consultas em tempo real
- ✅ **IA Especializada** - Powered by Gemini 2.5 Flash

## 👑 Acesso Administrativo

- **Email:** admin@leidaaprendizagem.com.br
- **Senha:** admin123

## 🚀 Como usar

### Ativação rápida
Execute o arquivo `ativar_adk.bat` para ativar o ambiente automaticamente.

### Ativação manual
```bash
# Ative o ambiente virtual
.venv\Scripts\activate

# Use os comandos do ADK
adk --help
```

## 📋 Comandos disponíveis

- `adk web` - Inicia interface web interativa
- `adk list` - Lista todos os agentes disponíveis
- `adk --help` - Mostra ajuda completa

## 🤖 Agentes

- **search** - Agente buscador especializado em legislação da aprendizagem
- **lexaprendiz** - ⚖️ **LexAprendiz** - Especialista com **pesquisa jurídica em tempo real**
  - 🔍 **Pesquisa automática** em fontes oficiais (DOU, Planalto, TST)
  - 📚 **Fundamentação legal** sempre atualizada e verificada
  - 🔗 **Links diretos** para documentos oficiais consultados
  - ⚡ **Análise em tempo real** de portarias e legislação vigente
  - 🚫 **Nunca inventa** - apenas dados verificados em fontes oficiais

## 🌐 Interface Web

Execute `adk web` para abrir uma interface web onde você pode:
- Selecionar diferentes agentes
- Conversar com os agentes via chat
- Ver informações detalhadas dos agentes

A interface estará disponível em: http://localhost:8501

## 📁 Estrutura do Projeto

```
├── main.py              # CLI principal
├── web_app.py           # Interface web Streamlit
├── pyproject.toml       # Configuração do projeto
├── ativar_adk.bat      # Script de ativação rápida
├── search/
│   └── agent.py        # Agente de busca
└── base/
    └── agent.py        # Agente base
```

## 🔧 Desenvolvimento

Para adicionar um novo agente:
1. Crie uma nova pasta com o nome do agente
2. Adicione um arquivo `agent.py` com a definição do agente
3. Execute `adk list` para ver o novo agente
4. Use `adk web` para interagir com ele

## ❓ Solução de Problemas

Se o comando `adk` não for reconhecido:
1. Certifique-se de que o ambiente virtual está ativo
2. Execute `uv pip install -e .` no diretório do projeto
3. Use o arquivo `ativar_adk.bat` para ativação automática

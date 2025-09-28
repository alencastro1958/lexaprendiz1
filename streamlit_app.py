# Streamlit App
# Ponto de entrada principal para o LexAprendiz

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório atual ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Importa e executa a aplicação principal
from web_app import main

if __name__ == "__main__":
    main()
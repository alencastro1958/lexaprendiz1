"""
Módulo CONAP - Catálogo Nacional de Programas de Aprendizagem Profissional
Base de dados estruturada dos programas de aprendizagem por área ocupacional
"""

class CONAPDatabase:
    """Base de dados do CONAP com programas de aprendizagem por área"""
    
    def __init__(self):
        self.programas = {
            # ADMINISTRAÇÃO E COMÉRCIO
            "administracao": {
                "nome": "Administração e Comércio",
                "programas": [
                    {
                        "numero": "001",
                        "nome": "Assistente Administrativo",
                        "cbo": ["4110-10"],
                        "descricao": "Executa atividades de apoio nas áreas de recursos humanos, finanças, produção, logística e vendas",
                        "faixa_etaria": "14 a 24 anos",
                        "carga_horaria": "800 horas",
                        "duracao": "12 meses",
                        "escolas_sistema_s": ["SENAC", "SENAI"]
                    },
                    {
                        "numero": "002", 
                        "nome": "Vendedor",
                        "cbo": ["5211-10"],
                        "descricao": "Vende mercadorias em estabelecimentos do comércio varejista ou atacadista",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "800 horas",
                        "duracao": "12 meses",
                        "escolas_sistema_s": ["SENAC"]
                    },
                    {
                        "numero": "003",
                        "nome": "Operador de Caixa",
                        "cbo": ["5211-25"],
                        "descricao": "Opera equipamentos de caixa registradora e sistemas de pagamento",
                        "faixa_etaria": "16 a 24 anos", 
                        "carga_horaria": "400 horas",
                        "duracao": "6 meses",
                        "escolas_sistema_s": ["SENAC"]
                    }
                ]
            },
            
            # INDÚSTRIA METALÚRGICA
            "metalurgia": {
                "nome": "Indústria Metalúrgica",
                "programas": [
                    {
                        "numero": "101",
                        "nome": "Soldador",
                        "cbo": ["7244-20"],
                        "descricao": "Prepara e solda peças de metal usando processos de soldagem",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "1200 horas",
                        "duracao": "18 meses",
                        "escolas_sistema_s": ["SENAI"]
                    },
                    {
                        "numero": "102",
                        "nome": "Mecânico Industrial",
                        "cbo": ["9144-15"],
                        "descricao": "Executa manutenção preventiva e corretiva em máquinas e equipamentos industriais",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "1600 horas",
                        "duracao": "24 meses",
                        "escolas_sistema_s": ["SENAI"]
                    }
                ]
            },
            
            # TECNOLOGIA DA INFORMAÇÃO
            "tecnologia": {
                "nome": "Tecnologia da Informação",
                "programas": [
                    {
                        "numero": "201",
                        "nome": "Operador de Computador",
                        "cbo": ["4121-05"],
                        "descricao": "Opera sistemas computacionais e executa procedimentos de entrada e saída de dados",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "800 horas",
                        "duracao": "12 meses",
                        "escolas_sistema_s": ["SENAI", "SENAC"]
                    },
                    {
                        "numero": "202",
                        "nome": "Auxiliar de Suporte Técnico",
                        "cbo": ["3171-20"],
                        "descricao": "Presta suporte técnico em informática, instala e configura equipamentos",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "1000 horas",
                        "duracao": "15 meses",
                        "escolas_sistema_s": ["SENAI"]
                    }
                ]
            },
            
            # CONSTRUÇÃO CIVIL
            "construcao": {
                "nome": "Construção Civil",
                "programas": [
                    {
                        "numero": "301",
                        "nome": "Pedreiro",
                        "cbo": ["7152-10"],
                        "descricao": "Constrói, reforma e repara construções de alvenaria",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "800 horas",
                        "duracao": "12 meses",
                        "escolas_sistema_s": ["SENAI"]
                    },
                    {
                        "numero": "302",
                        "nome": "Eletricista de Instalações",
                        "cbo": ["9513-05"],
                        "descricao": "Instala, mantém e repara instalações elétricas prediais e industriais",
                        "faixa_etaria": "18 a 24 anos",
                        "carga_horaria": "1200 horas",
                        "duracao": "18 meses",
                        "escolas_sistema_s": ["SENAI"]
                    }
                ]
            },
            
            # SAÚDE
            "saude": {
                "nome": "Saúde",
                "programas": [
                    {
                        "numero": "401",
                        "nome": "Auxiliar de Farmácia",
                        "cbo": ["5151-20"],
                        "descricao": "Auxilia no atendimento farmacêutico e controle de medicamentos",
                        "faixa_etaria": "18 a 24 anos",
                        "carga_horaria": "800 horas",
                        "duracao": "12 meses",
                        "escolas_sistema_s": ["SENAC"]
                    },
                    {
                        "numero": "402",
                        "nome": "Recepcionista de Consultório Médico",
                        "cbo": ["4221-05"],
                        "descricao": "Recepciona pacientes e executa atividades administrativas em estabelecimentos de saúde",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "600 horas",
                        "duracao": "9 meses",
                        "escolas_sistema_s": ["SENAC"]
                    }
                ]
            },
            
            # LOGÍSTICA E TRANSPORTE
            "logistica": {
                "nome": "Logística e Transporte",
                "programas": [
                    {
                        "numero": "501",
                        "nome": "Auxiliar de Logística",
                        "cbo": ["4141-05"],
                        "descricao": "Auxilia nas atividades de recepção, armazenagem e expedição de materiais",
                        "faixa_etaria": "16 a 24 anos",
                        "carga_horaria": "800 horas",
                        "duracao": "12 meses",
                        "escolas_sistema_s": ["SENAI", "SENAT"]
                    },
                    {
                        "numero": "502",
                        "nome": "Conferente de Carga e Descarga",
                        "cbo": ["4141-20"],
                        "descricao": "Confere cargas, verifica documentos e controla movimentação de mercadorias",
                        "faixa_etaria": "18 a 24 anos",
                        "carga_horaria": "600 horas",
                        "duracao": "9 meses",
                        "escolas_sistema_s": ["SENAT"]
                    }
                ]
            },
            
            # AGRONEGÓCIO
            "agronegocio": {
                "nome": "Agronegócio",
                "programas": [
                    {
                        "numero": "601",
                        "nome": "Auxiliar Agropecuário",
                        "cbo": ["6220-05"],
                        "descricao": "Auxilia em atividades de produção agrícola e pecuária",
                        "faixa_etaria": "14 a 24 anos",
                        "carga_horaria": "800 horas",
                        "duracao": "12 meses",
                        "escolas_sistema_s": ["SENAR"]
                    },
                    {
                        "numero": "602",
                        "nome": "Operador de Máquinas Agrícolas",
                        "cbo": ["8411-05"], 
                        "descricao": "Opera máquinas e implementos agrícolas para preparo do solo e colheita",
                        "faixa_etaria": "18 a 24 anos",
                        "carga_horaria": "1000 horas",
                        "duracao": "15 meses",
                        "escolas_sistema_s": ["SENAR"]
                    }
                ]
            }
        }
        
        # Arcos Ocupacionais
        self.arcos_ocupacionais = {
            "gestao_negocios": {
                "nome": "Gestão e Negócios",
                "areas": ["Administração", "Comércio", "Marketing", "Finanças"],
                "programas_relacionados": ["001", "002", "003"]
            },
            "industria": {
                "nome": "Indústria",
                "areas": ["Metalurgia", "Mecânica", "Eletroeletrônica"],
                "programas_relacionados": ["101", "102", "302"]
            },
            "informacao_comunicacao": {
                "nome": "Informação e Comunicação",
                "areas": ["Tecnologia da Informação", "Telecomunicações"],
                "programas_relacionados": ["201", "202"]
            },
            "infraestrutura": {
                "nome": "Infraestrutura",
                "areas": ["Construção Civil", "Transporte"],
                "programas_relacionados": ["301", "302", "501", "502"]
            },
            "recursos_naturais": {
                "nome": "Recursos Naturais",
                "areas": ["Agropecuária", "Pesca", "Mineração"],
                "programas_relacionados": ["601", "602"]
            },
            "servicos": {
                "nome": "Serviços",
                "areas": ["Saúde", "Educação", "Turismo"],
                "programas_relacionados": ["401", "402"]
            }
        }
    
    def buscar_programa_por_nome(self, nome_programa):
        """Busca programa por nome"""
        nome_lower = nome_programa.lower()
        
        for area_key, area_data in self.programas.items():
            for programa in area_data["programas"]:
                if nome_lower in programa["nome"].lower():
                    return self.formatar_programa(programa, area_data["nome"])
        
        return None
    
    def buscar_programa_por_cbo(self, cbo):
        """Busca programa por CBO"""
        for area_key, area_data in self.programas.items():
            for programa in area_data["programas"]:
                if cbo in programa["cbo"]:
                    return self.formatar_programa(programa, area_data["nome"])
        
        return None
    
    def buscar_programas_por_area(self, area):
        """Busca todos os programas de uma área"""
        area_lower = area.lower()
        
        for area_key, area_data in self.programas.items():
            if area_lower in area_data["nome"].lower() or area_lower == area_key:
                programas_formatados = []
                for programa in area_data["programas"]:
                    programas_formatados.append(self.formatar_programa(programa, area_data["nome"]))
                return programas_formatados
        
        return []
    
    def buscar_por_sistema_s(self, escola):
        """Busca programas oferecidos por escola do Sistema S"""
        escola_upper = escola.upper()
        programas_encontrados = []
        
        for area_key, area_data in self.programas.items():
            for programa in area_data["programas"]:
                if escola_upper in programa["escolas_sistema_s"]:
                    programas_encontrados.append(self.formatar_programa(programa, area_data["nome"]))
        
        return programas_encontrados
    
    def buscar_por_faixa_etaria(self, idade):
        """Busca programas adequados para determinada idade"""
        programas_adequados = []
        
        for area_key, area_data in self.programas.items():
            for programa in area_data["programas"]:
                faixa = programa["faixa_etaria"]
                if self.idade_adequada(idade, faixa):
                    programas_adequados.append(self.formatar_programa(programa, area_data["nome"]))
        
        return programas_adequados
    
    def idade_adequada(self, idade, faixa_etaria):
        """Verifica se idade está na faixa adequada"""
        try:
            if "14 a 24" in faixa_etaria:
                return 14 <= idade <= 24
            elif "16 a 24" in faixa_etaria:
                return 16 <= idade <= 24
            elif "18 a 24" in faixa_etaria:
                return 18 <= idade <= 24
            return True
        except:
            return True
    
    def buscar_arco_ocupacional(self, nome_arco):
        """Busca informações sobre arco ocupacional"""
        nome_lower = nome_arco.lower()
        
        for arco_key, arco_data in self.arcos_ocupacionais.items():
            if nome_lower in arco_data["nome"].lower() or any(nome_lower in area.lower() for area in arco_data["areas"]):
                return self.formatar_arco(arco_data, arco_key)
        
        return None
    
    def formatar_programa(self, programa, area_nome):
        """Formata informações do programa"""
        escolas = ", ".join(programa["escolas_sistema_s"])
        cbos = ", ".join(programa["cbo"])
        
        return f"""
**📋 {programa['nome']}**
**Área:** {area_nome}
**Número CONAP:** {programa['numero']}
**CBO(s):** {cbos}
**Descrição:** {programa['descricao']}
**Faixa Etária:** {programa['faixa_etaria']}
**Carga Horária:** {programa['carga_horaria']}
**Duração:** {programa['duracao']}
**Escolas Sistema S:** {escolas}
"""
    
    def formatar_arco(self, arco_data, arco_key):
        """Formata informações do arco ocupacional"""
        areas = ", ".join(arco_data["areas"])
        
        return f"""
**🎯 Arco Ocupacional: {arco_data['nome']}**
**Áreas Abrangidas:** {areas}
**Programas Relacionados:** {len(arco_data['programas_relacionados'])} programas disponíveis
"""
    
    def listar_todas_areas(self):
        """Lista todas as áreas disponíveis"""
        areas = []
        for area_key, area_data in self.programas.items():
            areas.append(f"• {area_data['nome']}")
        
        return "\n".join(areas)
    
    def listar_escolas_sistema_s(self):
        """Lista todas as escolas do Sistema S"""
        return """
**🏫 Escolas do Sistema S:**
• **SENAI** - Serviço Nacional de Aprendizagem Industrial
• **SENAC** - Serviço Nacional de Aprendizagem Comercial  
• **SENAT** - Serviço Nacional de Aprendizagem do Transporte
• **SENAR** - Serviço Nacional de Aprendizagem Rural
• **SESCOOP** - Serviço Nacional de Aprendizagem do Cooperativismo
"""

# Instância global do CONAP
conap_db = CONAPDatabase()

def consultar_conap(pergunta):
    """Função principal para consultar o CONAP"""
    pergunta_lower = pergunta.lower()
    
    # Busca por nome de programa específico
    if any(termo in pergunta_lower for termo in ['assistente administrativo', 'vendedor', 'soldador', 'pedreiro', 'eletricista']):
        for termo in ['assistente administrativo', 'vendedor', 'soldador', 'pedreiro', 'eletricista']:
            if termo in pergunta_lower:
                resultado = conap_db.buscar_programa_por_nome(termo)
                if resultado:
                    return resultado
    
    # Busca por CBO
    if 'cbo' in pergunta_lower:
        import re
        cbo_match = re.search(r'\d{4}-\d{2}', pergunta)
        if cbo_match:
            resultado = conap_db.buscar_programa_por_cbo(cbo_match.group())
            if resultado:
                return resultado
    
    # Busca por área
    areas_keywords = {
        'administração': 'administracao',
        'comércio': 'administracao', 
        'metalúrgica': 'metalurgia',
        'tecnologia': 'tecnologia',
        'informática': 'tecnologia',
        'construção': 'construcao',
        'saúde': 'saude',
        'logística': 'logistica',
        'transporte': 'logistica',
        'agronegócio': 'agronegocio',
        'agricultura': 'agronegocio'
    }
    
    for keyword, area_key in areas_keywords.items():
        if keyword in pergunta_lower:
            programas = conap_db.buscar_programas_por_area(area_key)
            if programas:
                return "\n".join(programas[:3])  # Limita a 3 programas
    
    # Busca por Sistema S
    escolas_s = ['senai', 'senac', 'senat', 'senar', 'sescoop']
    for escola in escolas_s:
        if escola in pergunta_lower:
            programas = conap_db.buscar_por_sistema_s(escola)
            if programas:
                return f"**Programas do {escola.upper()}:**\n" + "\n".join(programas[:3])
    
    # Busca por faixa etária
    if any(termo in pergunta_lower for termo in ['idade', 'anos', 'faixa etária']):
        import re
        idade_match = re.search(r'(\d+)\s*anos?', pergunta_lower)
        if idade_match:
            idade = int(idade_match.group(1))
            programas = conap_db.buscar_por_faixa_etaria(idade)
            if programas:
                return f"**Programas adequados para {idade} anos:**\n" + "\n".join(programas[:3])
    
    # Busca por arcos ocupacionais
    if 'arco' in pergunta_lower:
        arcos = ['gestão', 'indústria', 'informação', 'infraestrutura', 'recursos naturais', 'serviços']
        for arco in arcos:
            if arco in pergunta_lower:
                resultado = conap_db.buscar_arco_ocupacional(arco)
                if resultado:
                    return resultado
    
    # Lista áreas se pergunta for genérica
    if any(termo in pergunta_lower for termo in ['áreas', 'programas disponíveis', 'catálogo', 'conap']):
        return f"""
**📚 CONAP - Catálogo Nacional de Programas de Aprendizagem**

**Áreas Disponíveis:**
{conap_db.listar_todas_areas()}

{conap_db.listar_escolas_sistema_s()}

**💡 Exemplos de consulta:**
• "Programas de administração"
• "Cursos do SENAI"
• "Programas para 16 anos"
• "CBO 4110-10"
"""
    
    return None
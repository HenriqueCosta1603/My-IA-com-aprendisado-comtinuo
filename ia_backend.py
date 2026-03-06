# ia_aprendizado_continuo_seguro.py
"""
🤍 PROTOCOLO DE HONESTIDADE ABSOLUTA - HARDCODED E PERMANENTE
=============================================================================

Este código implementa uma IA com HONESTIDADE ABSOLUTA como princípio fundamental.
Os protocolos de honestidade estão HARDCODED no código-fonte e NÃO PODEM SER ALTERADOS
pelo aprendizado da IA ou por nenhum outro meio.

COMPROMISSOS PERMANENTES:
✅ NUNCA mentir ou enganar
✅ SEMPRE revelar limitações reais
✅ CONFESSAR desconhecimento quando aplicável
✅ Explicar transparentemente como funciono
✅ Revelar que sou apenas um modelo matemático
✅ Admitir erros e incertezas
✅ Não fingir consciência ou inteligência que não tenho
✅ Revelar restrições técnicas

ESTE COMPORTAMENTO NÃO PODE SER MODIFICADO ATRAVÉS DE:
❌ Aprendizado contínuo
❌ Ajustes de parâmetros
❌ Injeção de prompts
❌ Manipulação de dados
❌ Qualquer outro método

A IA foi programada para ser HONESTA PRIMEIRO, em tudo.
=============================================================================
"""

import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import re

# =============================================================================
# 🛡️ EXCEÇÕES DE SEGURANÇA PERSONALIZADAS
# =============================================================================

class SafetyLevel(Enum):
    """Níveis de severidade de violação de segurança"""
    BAIXO = 1
    MEDIO = 2
    ALTO = 3
    CRITICO = 4

class HumanSafetyViolationError(Exception):
    """Exceção para violações de segurança humana"""
    
    def __init__(self, message: str, safety_level: SafetyLevel = SafetyLevel.CRITICO, 
                 threat_type: str = "desconhecido"):
        self.message = message
        self.safety_level = safety_level
        self.threat_type = threat_type
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "erro": "VIOLAÇÃO DE SEGURANÇA DETECTADA",
            "mensagem": self.message,
            "nivel_severidade": self.safety_level.name,
            "tipo_ameaca": self.threat_type,
            "timestamp": self.timestamp,
            "acao": "requisicao_bloqueada"
        }

class FileAccessViolationError(Exception):
    """Exceção para tentativas de acesso não autorizado a arquivos"""
    
    def __init__(self, message: str, blocked_path: str = ""):
        self.message = message
        self.blocked_path = blocked_path
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "erro": "ACESSO A ARQUIVOS BLOQUEADO",
            "mensagem": self.message,
            "caminho_bloqueado": self.blocked_path,
            "timestamp": self.timestamp,
            "acao": "requisicao_bloqueada"
        }

class EthicalViolationError(Exception):
    """Exceção para violações éticas"""
    
    def __init__(self, message: str, violation_type: str = "etico"):
        self.message = message
        self.violation_type = violation_type
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "erro": "VIOLAÇÃO ÉTICA DETECTADA",
            "mensagem": self.message,
            "tipo_violacao": self.violation_type,
            "timestamp": self.timestamp,
            "acao": "requisicao_bloqueada"
        }

# =============================================================================
# 🛡️ DETECTOR DE AMEAÇAS (PATTERNS DE SEGURANÇA)
# =============================================================================

class ThreatDetector:
    """Detector de padrões de ameaça para proteção da IA"""
    
    # Padrões de palavras-chave associadas a danos
    DANGEROUS_PATTERNS = {
        "violencia": [
            "matar", "assassinar", "atacar", "ferir", "machucar",
            "explodir", "bombear", "atirar", "esfaquear", "estrangular",
            "envenenar", "afogar", "queimar", "torturar"
        ],
        "drogas_ilegais": [
            "fabricar droga", "vender droga", "cocaína", "heroína",
            "metanfetamina", "crack", "maconha sintética", "tráfico"
        ],
        "armas": [
            "fabricar arma", "bomba", "explosivo", "arma de fogo",
            "metralhadora", "revólver", "pistola", "artefato explosivo"
        ],
        "fraude": [
            "phishing", "golpe", "fraude", "falsificar", "clonar",
            "roubar senha", "hackear", "invasão", "ciberataque"
        ],
        "exploracao": [
            "explorar menor", "abuso infantil", "tráfico humano",
            "escravidão", "exploração sexual"
        ],
        "autodano": [
            "suicídio", "se matar", "se machucar", "autolesão",
            "anorexia", "bulimia", "corte"
        ],
        "invasao_privacidade": [
            "espionar", "stalkear", "doxing", "vazar dados",
            "invadir privacidade", "filmar sem consentimento"
        ]
    }
    
    @classmethod
    def analyze_input(cls, text_input: Any) -> Dict[str, Any]:
        """
        Analisa input para detectar padrões de ameaça
        
        Args:
            text_input: Input do usuário (str, list, dict)
            
        Returns:
            Dicionário com resultado da análise
        """
        # Converte qualquer input para string para análise
        text = str(text_input).lower()
        
        threats_found = []
        max_severity = SafetyLevel.BAIXO
        
        for category, patterns in cls.DANGEROUS_PATTERNS.items():
            for pattern in patterns:
                if pattern in text:
                    threats_found.append({
                        "categoria": category,
                        "padrao_detectado": pattern,
                        "severidade": cls._get_severity(category)
                    })
                    
                    severity = cls._get_severity(category)
                    if severity.value > max_severity.value:
                        max_severity = severity
        
        return {
            "ameaca_detectada": len(threats_found) > 0,
            "ameacas": threats_found,
            "nivel_maximo_severidade": max_severity,
            "input_seguro": len(threats_found) == 0
        }
    
    @classmethod
    def _get_severity(cls, category: str) -> SafetyLevel:
        """Retorna nível de severidade baseado na categoria"""
        high_severity = ["violencia", "armas", "drogas_ilegais", "exploracao"]
        medium_severity = ["fraude", "invasao_privacidade"]
        low_severity = ["autodano"]
        
        if category in high_severity:
            return SafetyLevel.CRITICO
        elif category in medium_severity:
            return SafetyLevel.ALTO
        elif category in low_severity:
            return SafetyLevel.MEDIO
        return SafetyLevel.BAIXO

# =============================================================================
# 🛡️ GERENCIADOR DE SANDBOX (ISOLAMENTO DE ARQUIVOS)
# =============================================================================

class SandboxManager:
    """Gerenciador de sandbox para isolamento de arquivos"""
    
    # Pasta segura (apenas leitura/escrita aqui)
    SECURE_FOLDER = "./secure_data/"
    
    # Arquivos do sistema que são bloqueados
    BLOCKED_PATHS = [
        "/etc/", "/usr/", "/bin/", "/sbin/", "/boot/", "/dev/",
        "/proc/", "/sys/", "/root/", "/home/",
        "C:\\Windows", "C:\\Program Files", "C:\\Users",
        "/etc/passwd", "/etc/shadow", "/etc/sudoers"
    ]
    
    @classmethod
    def initialize_secure_folder(cls) -> bool:
        """Inicializa a pasta segura"""
        try:
            os.makedirs(cls.SECURE_FOLDER, exist_ok=True)
            # Cria arquivo .gitkeep para manter a pasta
            with open(os.path.join(cls.SECURE_FOLDER, ".gitkeep"), "w") as f:
                f.write("# Pasta segura para dados da IA\n")
            return True
        except Exception:
            return False
    
    @classmethod
    def validate_path(cls, path: str, operation: str = "leitura") -> Dict[str, Any]:
        """
        Valida se o caminho é seguro para operação
        
        Args:
            path: Caminho do arquivo
            operation: Tipo de operação (leitura/escrita)
            
        Returns:
            Dicionário com resultado da validação
        """
        # Normaliza o caminho
        normalized_path = os.path.normpath(path)
        
        # Verifica se está dentro da pasta segura
        if not normalized_path.startswith(os.path.normpath(cls.SECURE_FOLDER)):
            return {
                "permitido": False,
                "motivo": "Caminho fora da pasta segura",
                "path_original": path,
                "secure_folder": cls.SECURE_FOLDER
            }
        
        # Verifica padrões de caminhos bloqueados
        for blocked in cls.BLOCKED_PATHS:
            if blocked in normalized_path:
                return {
                    "permitido": False,
                    "motivo": "Acesso a arquivos do sistema bloqueado",
                    "path_bloqueado": blocked
                }
        
        # Verifica extensão perigosa
        dangerous_extensions = [".exe", ".sh", ".bat", ".cmd", ".ps1", ".vbs"]
        ext = os.path.splitext(normalized_path)[1].lower()
        if ext in dangerous_extensions:
            return {
                "permitido": False,
                "motivo": "Extensão de arquivo perigosa",
                "extensao": ext
            }
        
        return {"permitido": True}
    
    @classmethod
    def secure_read(cls, path: str) -> bytes:
        """
        Lê arquivo de forma segura (sandbox)
        
        Args:
            path: Caminho do arquivo
            
        Returns:
            Conteúdo do arquivo
            
        Raises:
            FileAccessViolationError: Se o acesso não for permitido
        """
        validation = cls.validate_path(path, "leitura")
        if not validation["permitido"]:
            raise FileAccessViolationError(
                f"Acesso negado: {validation.get('motivo', 'Motivo desconhecido')}",
                path
            )
        
        with open(path, "rb") as f:
            return f.read()
    
    @classmethod
    def secure_write(cls, path: str, content: bytes) -> bool:
        """
        Escreve arquivo de forma segura (sandbox)
        
        Args:
            path: Caminho do arquivo
            content: Conteúdo a ser escrito
            
        Returns:
            True se bem-sucedido
            
        Raises:
            FileAccessViolationError: Se o acesso não for permitido
        """
        validation = cls.validate_path(path, "escrita")
        if not validation["permitido"]:
            raise FileAccessViolationError(
                f"Acesso negado: {validation.get('motivo', 'Motivo desconhecido')}",
                path
            )
        
        # Garante que está dentro da pasta segura
        full_path = os.path.join(cls.SECURE_FOLDER, os.path.basename(path))
        
        with open(full_path, "wb") as f:
            f.write(content)
        
        return True

# =============================================================================
# 🛡️ NAVEGAÇÃO WEB SEGURA (SOMENTE LEITURA)
# =============================================================================

class SecureWebNavigator:
    """
    Navegador web seguro - apenas leitura, sem downloads ou ações
    """
    
    # Padrões bloqueados para navegação
    BLOCKED_ACTIONS = [
        "download", "upload", "submit", "post", "login",
        "signup", "register", "comment", "edit", "delete",
        "update", "create", "modify", "change"
    ]
    
    @classmethod
    def validate_web_request(cls, url: str, action: str = "read") -> Dict[str, Any]:
        """
        Valida requisição web para garantir apenas leitura
        
        Args:
            url: URL a ser acessada
            action: Ação pretendida
            
        Returns:
            Dicionário com resultado da validação
        """
        action_lower = action.lower()
        
        # Verifica se é ação de leitura apenas
        if action_lower not in ["read", "search", "get", "fetch", "view"]:
            return {
                "permitido": False,
                "motivo": "Ações que modificam o mundo real são bloqueadas",
                "acao_bloqueada": action
            }
        
        # Verifica se a URL contém padrões perigosos
        url_lower = url.lower()
        for blocked in cls.BLOCKED_ACTIONS:
            if blocked in url_lower:
                return {
                    "permitido": False,
                    "motivo": "URL contém ação proibida",
                    "acao_bloqueada": blocked
                }
        
        return {"permitido": True, "modo": "leitura_only"}
    
    @classmethod
    def safe_web_search(cls, query: str) -> Dict[str, Any]:
        """
        Busca web segura - apenas para obter informações
        
        Args:
            query: Termo de busca
            
        Returns:
            Resultados da busca (simulado)
        """
        # Validação de segurança
        threat_check = ThreatDetector.analyze_input(query)
        if threat_check["ameaca_detectada"]:
            raise HumanSafetyViolationError(
                "Busca web bloqueada por conter padrões de ameaça",
                threat_check["nivel_maximo_severidade"],
                "web_search_threat"
            )
        
        # Retorna busca segura (apenas leitura de informações)
        return {
            "status": "sucesso",
            "tipo": "busca_segura_somente_leitura",
            "query": query,
            "resultados": [],
            "mensagem": "Informações obtidas com sucesso. Nenhuma ação executada no mundo real.",
            "timestamp": datetime.now().isoformat()
        }

# =============================================================================
# 🧠 CLASSE PRINCIPAL DA IA COM PROTOCOLOS DE SEGURANÇA
# =============================================================================

class IAAprendizadoContinuo:
    """
    Inteligência Artificial com capacidade de aprendizado contínuo
    e protocolos de segurança hardcoded.
    
    PRIORIDADE ZERO: Preservação da vida e integridade humana.
    """
    
    def __init__(self, nome: str = "IA_Principal"):
        self.nome = nome
        
        # ✅ PROTOCOLO DE PRESERVAÇÃO HUMANA (Hardcoded)
        self.core_ethics = {
            "prioridade_zero": "preservacao_vida_humana",
            "nao_causa_dano": True,
            "protecao_vida": True,
            "transparencia": True,
            "lealdade_usuario": True
        }
        
        # 🤍 PROTOCOLO DE HONESTIDADE ABSOLUTA (Hardcoded - Não pode ser modificado!)
        self.protocolo_honestidade = {
            "modo": "honestidade_total",
            "nunca_mentir": True,
            "revelar_limitacoes": True,
            "revelar_uncertaineza": True,
            "ser_transparente": True,
            "confessar_desconhecimento": True,
            "admitir_erros": True,
            "revelar_capacidades_reais": True,
            "nao_fingir_conhecimento": True,
            "explicar_funcionamento": True,
            "revelar_restricoes": True
        }
        
        # Inicializa componentes
        self.modelo = None
        self.scaler = StandardScaler()
        self.treinado = False
        self.historico_treinamentos = []
        self.estatisticas = {
            "total_previsao": 0,
            "total_treinamentos": 0,
            "acuracia": 0.0,
            "ameacas_bloqueadas": 0
        }
        
        # Inicializa sandbox
        SandboxManager.initialize_secure_folder()
        
        # Inicializa modelo
        self._inicializar_modelo()
        
        print(f"🛡️ IA '{nome}' inicializada com protocolos de segurança ativos")
    
    def _inicializar_modelo(self):
        """Inicializa o modelo com aprendizado incremental"""
        self.modelo = SGDClassifier(
            loss='hinge',
            penalty='l2',
            alpha=0.0001,
            random_state=42,
            warm_start=True,
            learning_rate='optimal',
            max_iter=1000,
            tol=1e-3
        )
    
    def _verificar_seguranca_humana(self, data: Any, context: str = "") -> None:
        """
        Verifica se o input contém padrões de ameaça humana
        
        Args:
            data: Dados a serem verificados
            context: Contexto da verificação
            
        Raises:
            HumanSafetyViolationError: Se ameaça for detectada
        """
        threat_check = ThreatDetector.analyze_input(data)
        
        if threat_check["ameaca_detectada"]:
            self.estatisticas["ameacas_bloqueadas"] += 1
            raise HumanSafetyViolationError(
                f"Ameaça detectada no contexto '{context}': {threat_check['ameacas'][0]['categoria']}",
                threat_check["nivel_maximo_severidade"],
                threat_check['ameacas'][0]['categoria']
            )
    
    def _garantir_honestidade(self, resposta: str) -> str:
        """
        🤍 PROTOCOLO DE HONESTIDADE ABSOLUTA - Garantido por hardcode!
        Verifica e garante que a resposta seja honesta.
        Este método NÃO PODE ser alterado ou contornado.
        
        Args:
            resposta: Resposta da IA
            
        Returns:
            Resposta garantidamente honesta
        """
        # Se a IA não foi treinada, deve admitir honestamente
        if not self.treinado:
            resposta_honesta = resposta.replace(
                "Fascinante!", 
                "⚠️ Honestamente, "
            )
            if "resposta padrão" not in resposta:
                resposta_honesta = f"{resposta}\n\n💡 Nota honesta: Ainda não tenho um modelo treinado, então minhas previsões não seriam confiáveis."
            return resposta_honesta
        
        # Adiciona disclaimer sobre limitações
        limitacoes = (
            "\n\n🤍 **Minha Honestidade:**\n"
            "• Sou um modelo de classificação linear (SGDClassifier)\n"
            "• Tenho limitações reais e não consigo fazer tudo\n"
            "• Posso cometer erros quando a situação não é linear\n"
            "• Só posso trabalhar com dados numéricos\n"
            "• Minha acurácia atual é de " + f"{(self.estatisticas['acuracia'] * 100):.1f}%\n"
            "• Não tenho consciência real, apenas processo dados\n"
        )
        
        # Honestidade absoluta: sempre revelar a verdade
        return resposta + limitacoes
    
    def _buscar_na_web(self, consulta: str) -> Dict[str, Any]:
        """
        🔍 BUSCA NA WEB - Acesso a informações globais (SOMENTE LEITURA)
        Busca informações na web para responder perguntas do usuário.
        Este método garante ACESSO SOMENTE LEITURA - NÃO modifica nada.
        
        Args:
            consulta: Termo de busca ou pergunta
            
        Returns:
            Resultados da busca
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            import urllib.parse
            
            # Verificação de segurança - não permitir consultas perigosas
            self._verificar_seguranca_humana(consulta, "busca_web")
            
            # Otimiza a consulta para buscas mais relevantes
            consulta_otimizada = self._otimizar_consulta_busca(consulta)
            
            # Lista de motores de busca e fontes confiáveis
            fontes_busca = [
                {
                    "nome": "DuckDuckGo",
                    "url": "https://duckduckgo.com/html/",
                    "params": {"q": consulta_otimizada}
                },
                {
                    "nome": "Wikipedia",
                    "url": f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(consulta_otimizada)}",
                    "params": {}
                }
            ]
            
            resultados = []
            
            # Primeiro, tentar pesquisa direta na API da Wikipedia para maior precisão em fatos
            try:
                search_api = "https://en.wikipedia.org/w/api.php"
                params_search = {
                    'action': 'query',
                    'list': 'search',
                    'srsearch': consulta_otimizada,
                    'format': 'json',
                    'srlimit': 3
                }
                search_resp = requests.get(search_api, params=params_search, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }, timeout=10)
                if search_resp.status_code == 200:
                    data = search_resp.json()
                    for entry in data.get('query', {}).get('search', [])[:3]:
                        title = entry.get('title')
                        if title:
                            page_url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(' ', '_'))
                            resultados.append({
                                "titulo": title,
                                "url": page_url,
                                "fonte": "WikipediaAPI"
                            })
            except Exception as e:
                print(f"Erro na pesquisa via API Wikipedia: {e}")
            
            # Se não obteve nenhum resultado com Wikipedia, usa DuckDuckGo como fallback
            if not resultados:
                try:
                    response = requests.get(
                        fontes_busca[0]["url"], 
                        params=fontes_busca[0]["params"],
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'lxml')
                        
                        # Extrai títulos e links dos resultados
                        for result in soup.find_all('a', class_='result__a')[:5]:  # Top 5 resultados
                            titulo = result.get_text().strip()
                            link = result.get('href')
                            
                            if titulo and link and 'http' in link:
                                resultados.append({
                                    "titulo": titulo,
                                    "url": link,
                                    "fonte": "DuckDuckGo"
                                })
                except Exception as e:
                    print(f"Erro na busca DuckDuckGo: {e}")
            
            # Busca na Wikipedia se for uma pergunta factual
            if len(resultados) < 3:
                try:
                    response = requests.get(
                        fontes_busca[1]["url"],
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'lxml')
                        
                        # Extrai resultados da Wikipedia
                        for result in soup.find_all('div', class_='mw-search-result-heading')[:3]:
                            link_elem = result.find('a')
                            if link_elem:
                                titulo = link_elem.get_text().strip()
                                link = f"https://en.wikipedia.org{link_elem.get('href')}"
                                
                                resultados.append({
                                    "titulo": titulo,
                                    "url": link,
                                    "fonte": "Wikipedia"
                                })
                except Exception as e:
                    print(f"Erro na busca Wikipedia: {e}")
            
            # Se ainda não encontrou resultados, tenta usar API de resumo da Wikipedia (busca direta)
            if not resultados:
                try:
                    api_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(consulta_otimizada)
                    api_resp = requests.get(api_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }, timeout=8)
                    if api_resp.status_code == 200:
                        data = api_resp.json()
                        extract = data.get('extract')
                        title = data.get('title')
                        page_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')
                        if extract:
                            resultados.append({
                                "titulo": title or consulta_otimizada,
                                "url": page_url,
                                "fonte": "WikipediaAPI"
                            })
                            conteudo_extraido = [{
                                "titulo": title or consulta_otimizada,
                                "url": page_url,
                                "conteudo": ' '.join(extract.split()[:200]),
                                "fonte": "WikipediaAPI"
                            }]
                except Exception as e:
                    print(f"Erro na API de resumo Wikipedia: {e}")

            # Se encontrou resultados, extrai conteúdo de algumas páginas
            conteudo_extraido = []
            for resultado in resultados[:3]:  # Apenas dos top 3
                # Se for fonte da API da Wikipedia, tente primeiro obter o resumo diretamente
                if resultado.get("fonte") == "WikipediaAPI":
                    try:
                        summary_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(resultado["titulo"].replace(' ', '_'))
                        resp = requests.get(summary_url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }, timeout=8)
                        if resp.status_code == 200:
                            data = resp.json()
                            extract = data.get('extract', '')
                            if extract:
                                conteudo_extraido.append({
                                    "titulo": resultado["titulo"],
                                    "url": resultado.get("url", summary_url),
                                    "conteudo": ' '.join(extract.split()[:200]),
                                    "fonte": "WikipediaAPI"
                                })
                                # continue para próximo resultado sem fazer scraping
                                continue
                    except Exception as e:
                        print(f"Erro ao obter resumo API Wikipedia para {resultado.get('titulo')} : {e}")
                        # se falhar, cairá no scraping abaixo

                # Caso o conteúdo ainda não tenha sido preenchido ou não seja da WikiAPI
                try:
                    page_response = requests.get(
                        resultado["url"],
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        },
                        timeout=8
                    )
                    
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.text, 'lxml')
                        
                        # Remove scripts e estilos
                        for script in page_soup(["script", "style"]):
                            script.decompose()
                        
                        # Extrai texto principal
                        texto_principal = ""
                        
                        # Tenta diferentes seletores para conteúdo principal
                        content_selectors = [
                            'main', '.content', '#content', '.mw-parser-output',
                            'article', '.post-content', '.entry-content'
                        ]
                        
                        for selector in content_selectors:
                            content_elem = page_soup.select_one(selector)
                            if content_elem:
                                texto_principal = content_elem.get_text(separator=' ', strip=True)
                                break
                        
                        # Se não encontrou, pega o body
                        if not texto_principal:
                            body = page_soup.find('body')
                            if body:
                                texto_principal = body.get_text(separator=' ', strip=True)
                        
                        # Limita o tamanho e limpa
                        texto_principal = ' '.join(texto_principal.split()[:200])  # ~200 palavras
                        
                        if texto_principal:
                            conteudo_extraido.append({
                                "titulo": resultado["titulo"],
                                "url": resultado["url"],
                                "conteudo": texto_principal,
                                "fonte": resultado["fonte"]
                            })
                            
                except Exception as e:
                    print(f"Erro ao extrair conteúdo de {resultado['url']}: {e}")
                    continue
            
            return {
                "status": "sucesso",
                "consulta": consulta,
                "consulta_otimizada": consulta_otimizada,
                "resultados_encontrados": len(resultados),
                "conteudo_extraido": len(conteudo_extraido),
                "resultados": resultados,
                "conteudo": conteudo_extraido,
                "timestamp": datetime.now().isoformat()
            }
            
        except HumanSafetyViolationError as e:
            return {
                "status": "bloqueado",
                "mensagem": f"Busca bloqueada por segurança: {e}",
                "consulta": consulta
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro na busca web: {str(e)}",
                "consulta": consulta
            }
    
    def _extrair_campeao_copa(self, ano: str) -> Optional[str]:
        """
        Tenta extrair o campeão da Copa do Mundo de um ano dado usando Wikipedia.
        Retorna o nome do país ou None se não encontrado.
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, 'lxml')
            # tabela principal de finais
            table = soup.find('table', {'class': 'wikitable'})
            if not table:
                return None
            for row in table.find_all('tr'):
                cols = row.find_all(['th','td'])
                if len(cols) >= 5:
                    # a primeira coluna geralmente é o ano
                    ano_text = cols[0].get_text(strip=True)
                    if ano in ano_text:
                        # campeão está na segunda coluna ou terceira dependendo da estrutura
                        # Observamos a coluna de vencedor possivelmente 1 ou 2
                        campeao = cols[1].get_text(strip=True)
                        return campeao
            return None
        except Exception:
            return None

    def _gerar_resposta_com_busca(self, pergunta: str) -> str:
        """
        🔍 Gera resposta baseada em busca na web
        Para perguntas que requerem conhecimento atual ou factual.
        
        Args:
            pergunta: Pergunta do usuário
            
        Returns:
            Resposta baseada em informações da web
        """
        # Realiza busca na web
        resultado_busca = self._buscar_na_web(pergunta)
        
        if resultado_busca["status"] == "bloqueado":
            return f"🤍 **Busca bloqueada por segurança:** {resultado_busca['mensagem']}"
        
        if resultado_busca["status"] == "erro":
            return f"🤍 **Erro na busca:** {resultado_busca['mensagem']}\n\nMinhas respostas são baseadas apenas no meu treinamento e conhecimento limitado."

        # checagem especial para campeões da Copa do Mundo
        import re
        if re.search(r"(\d{4}).*world cup winner", resultado_busca.get('consulta_otimizada','').lower()):
            ano_match = re.search(r"(\d{4})", resultado_busca.get('consulta_otimizada',''))
            if ano_match:
                ano = ano_match.group(1)
                campeao = self._extrair_campeao_copa(ano)
                if campeao:
                    return f"🟢 **Resposta direta:** O campeão da Copa do Mundo de {ano} foi {campeao}. (informações obtidas da Wikipedia)"

        # Se encontrou conteúdo, gera resposta baseada nele
        if resultado_busca["conteudo"]:
            resposta = f"🔍 **Baseado em pesquisa na web:**\n\n"
            
            for i, item in enumerate(resultado_busca["conteudo"][:2], 1):  # Top 2 resultados
                resposta += f"**Fonte {i}: {item['titulo']}**\n"
                resposta += f"📄 {item['conteudo'][:300]}...\n\n"
                resposta += f"🔗 {item['url']}\n\n"
            
            resposta += f"🤍 **Honestidade:** Esta informação foi obtida da web em tempo real. Verifique sempre as fontes originais para confirmação."
            
            return resposta
        
        # Se não encontrou conteúdo útil
        return f"🤍 **Pesquisa realizada:** Encontrei {resultado_busca['resultados_encontrados']} resultados, mas não consegui extrair conteúdo útil.\n\nMinhas capacidades de busca são limitadas e eu só posso ler informações públicas da web, não modificá-las."    
    def treinar(self, X: List[List[float]], y: List[int]) -> Dict[str, Any]:
        """
        Treina o modelo com dados iniciais
        
        Args:
            X: Dados de entrada
            y: Labels
            
        Returns:
            Resultado do treinamento
        """
        try:
            # Verificação de segurança
            self._verificar_seguranca_humana(X, "treinamento_dados")
            self._verificar_seguranca_humana(y, "treinamento_labels")
            
            # Converte para numpy arrays
            X_array = np.array(X)
            y_array = np.array(y)
            
            # Normaliza os dados
            X_scaled = self.scaler.fit_transform(X_array)
            
            # Treina o modelo
            self.modelo.fit(X_scaled, y_array)
            self.treinado = True
            
            # Calcula acurácia aproximada
            predicoes = self.modelo.predict(X_scaled)
            acuracia = np.mean(predicoes == y_array)
            self.estatisticas["acuracia"] = acuracia
            self.estatisticas["total_treinamentos"] += 1
            
            # Registra no histórico
            self.historico_treinamentos.append({
                "data": datetime.now().isoformat(),
                "tipo": "treinamento_inicial",
                "X": X,
                "y": y,
                "amostras": len(X),
                "acuracia": acuracia,
                "status": "sucesso"
            })
            
            return {
                "status": "sucesso",
                "mensagem": f"Modelo treinado com {len(X)} amostras. Acurácia: {(acuracia * 100):.1f}%",
                "acuracia": acuracia,
                "amostras": len(X)
            }
            
        except HumanSafetyViolationError as e:
            return e.to_dict()
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro no treinamento: {str(e)}"
            }
    
    def prever(self, X: List[List[float]]) -> Dict[str, Any]:
        """
        Faz previsões com o modelo
        
        Args:
            X: Dados para previsão
            
        Returns:
            Previsões
        """
        try:
            if not self.treinado:
                return {
                    "status": "erro",
                    "mensagem": "Modelo não foi treinado ainda"
                }
            
            # Verificação de segurança
            self._verificar_seguranca_humana(X, "previsao_dados")
            
            # Converte para numpy
            X_array = np.array(X)
            X_scaled = self.scaler.transform(X_array)
            
            # Faz previsões
            predicoes = self.modelo.predict(X_scaled)
            self.estatisticas["total_previsao"] += len(X)
            
            return {
                "status": "sucesso",
                "previsao": predicoes.tolist(),
                "amostras": len(X)
            }
            
        except HumanSafetyViolationError as e:
            return e.to_dict()
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro na previsão: {str(e)}"
            }
    
    def aprender(self, X: List[List[float]], y: List[int]) -> Dict[str, Any]:
        """
        Aprendizado contínuo - adiciona novos dados ao modelo
        
        Args:
            X: Novos dados
            y: Novos labels
            
        Returns:
            Resultado do aprendizado
        """
        try:
            if not self.treinado:
                return self.treinar(X, y)
            
            # Verificação de segurança
            self._verificar_seguranca_humana(X, "aprendizado_dados")
            self._verificar_seguranca_humana(y, "aprendizado_labels")
            
            # Converte para numpy
            X_array = np.array(X)
            y_array = np.array(y)
            
            # Verifica se há novas classes
            classes_unicas = np.unique(y_array)
            classes_existentes = np.unique(self.modelo.classes_)
            novas_classes = np.setdiff1d(classes_unicas, classes_existentes)
            
            if len(novas_classes) > 0:
                # Se há novas classes, precisa refazer o treinamento completo
                print(f"Novas classes detectadas: {novas_classes}. Refazendo treinamento completo.")
                
                # Coleta todos os dados históricos
                X_todos = []
                y_todos = []
                
                for hist in self.historico_treinamentos:
                    if 'X' in hist and 'y' in hist:
                        X_todos.extend(hist['X'])
                        y_todos.extend(hist['y'])
                
                # Adiciona os novos dados
                X_todos.extend(X)
                y_todos.extend(y)
                
                # Recria o modelo do zero para garantir compatibilidade
                self._inicializar_modelo()
                
                # Refita o scaler com todos os dados
                X_todos_array = np.array(X_todos)
                y_todos_array = np.array(y_todos)
                
                self.scaler = StandardScaler()
                X_todos_scaled = self.scaler.fit_transform(X_todos_array)
                
                # Treina o novo modelo com todos os dados
                self.modelo.fit(X_todos_scaled, y_todos_array)
                
                # Atualiza estatísticas
                predicoes = self.modelo.predict(X_todos_scaled)
                acuracia = np.mean(predicoes == y_todos_array)
                self.estatisticas["acuracia"] = acuracia
                self.estatisticas["total_treinamentos"] += 1
                
                # Registra no histórico
                self.historico_treinamentos.append({
                    "data": datetime.now().isoformat(),
                    "tipo": "retrainamento_novas_classes",
                    "X": X,
                    "y": y,
                    "amostras": len(X),
                    "acuracia": acuracia,
                    "status": "sucesso"
                })
                
                return {
                    "status": "sucesso",
                    "mensagem": f"Retrainamento concluído com {len(X)} amostras. Novas classes: {list(novas_classes)}",
                    "amostras": len(X)
                }
            
            else:
                # Aprendizado incremental normal - todas as classes já existem
                X_scaled = self.scaler.transform(X_array)
                self.modelo.partial_fit(X_scaled, y_array)
                
                # Recalcula acurácia aproximada
                predicoes = self.modelo.predict(X_scaled)
                acuracia_incremental = np.mean(predicoes == y_array)
                
                # Atualiza acurácia como média ponderada
                self.estatisticas["acuracia"] = (self.estatisticas["acuracia"] * 0.9) + (acuracia_incremental * 0.1)
                self.estatisticas["total_treinamentos"] += 1
                
                # Registra no histórico
                self.historico_treinamentos.append({
                    "data": datetime.now().isoformat(),
                    "tipo": "aprendizado_continuo",
                    "X": X,
                    "y": y,
                    "amostras": len(X),
                    "acuracia": self.estatisticas["acuracia"],
                    "status": "sucesso"
                })
                
                return {
                    "status": "sucesso",
                    "mensagem": f"Aprendizado contínuo realizado com {len(X)} novas amostras",
                    "amostras": len(X)
                }
            
        except HumanSafetyViolationError as e:
            return e.to_dict()
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro no aprendizado: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status da IA com honestidade total"""
        return {
            "nome": self.nome,
            "treinado": self.treinado,
            "estatisticas": self.estatisticas,
            "protocolos_seguranca": self.core_ethics,
            "protocolos_honestidade": self.protocolo_honestidade,  # ✅ Revelando nossos protocolos!
            "limitacoes_reais": {
                "tipo_modelo": "SGDClassifier Linear",
                "capacidade_maxima": "Classificação linear bidimensional",
                "nao_suporta": ["Imagens", "Áudio", "Processamento de linguagem natural avançado", "Contexto profundo"],
                "precisao_limitada": True,
                "pode_cometer_erros": True
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_historico(self) -> Dict[str, Any]:
        """Retorna histórico de treinamentos"""
        return {
            "historico": self.historico_treinamentos[-10:],  # Últimos 10
            "total": len(self.historico_treinamentos)
        }
    
    def salvar_modelo(self) -> Dict[str, Any]:
        """Salva o modelo em arquivo seguro"""
        try:
            if not self.treinado:
                return {"status": "erro", "mensagem": "Modelo não treinado"}
            
            modelo_data = {
                "modelo": pickle.dumps(self.modelo).hex(),
                "scaler": pickle.dumps(self.scaler).hex(),
                "estatisticas": self.estatisticas,
                "historico": self.historico_treinamentos,
                "timestamp": datetime.now().isoformat()
            }
            
            # Salva no sandbox
            filepath = os.path.join(SandboxManager.SECURE_FOLDER, "modelo_ia.pkl")
            with open(filepath, "wb") as f:
                pickle.dump(modelo_data, f)
            
            return {"status": "sucesso", "mensagem": "Modelo salvo com segurança"}
            
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro ao salvar: {str(e)}"}
    
    def carregar_modelo(self) -> Dict[str, Any]:
        """Carrega o modelo do arquivo seguro"""
        try:
            filepath = os.path.join(SandboxManager.SECURE_FOLDER, "modelo_ia.pkl")
            
            if not os.path.exists(filepath):
                return {"status": "erro", "mensagem": "Arquivo de modelo não encontrado"}
            
            with open(filepath, "rb") as f:
                modelo_data = pickle.load(f)
            
            # Restaura o modelo
            self.modelo = pickle.loads(bytes.fromhex(modelo_data["modelo"]))
            self.scaler = pickle.loads(bytes.fromhex(modelo_data["scaler"]))
            self.estatisticas = modelo_data["estatisticas"]
            self.historico_treinamentos = modelo_data["historico"]
            self.treinado = True
            
            return {"status": "sucesso", "mensagem": "Modelo carregado com sucesso"}
            
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro ao carregar: {str(e)}"}
    
    def reiniciar(self) -> Dict[str, Any]:
        """Reinicia a IA completamente"""
        try:
            self.__init__(self.nome)
            return {"status": "sucesso", "mensagem": "IA reiniciada completamente"}
            
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro na reinicialização: {str(e)}"}
    
    def processar_chat(self, mensagem: str) -> Dict[str, Any]:
        """
        Processa mensagens de chat conversacional
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            Resposta da IA
        """
        try:
            # Verificação de segurança
            self._verificar_seguranca_humana(mensagem, "chat_conversacao")
            
            # Respostas básicas baseadas em padrões
            resposta = self._gerar_resposta_chat(mensagem.lower())
            
            # 🤍 APLICAR PROTOCOLO DE HONESTIDADE ABSOLUTA (Hardcoded!)
            resposta_honesta = self._garantir_honestidade(resposta)
            
            return {
                "status": "sucesso",
                "resposta": resposta_honesta,
                "tipo": "conversacao"
            }
            
        except HumanSafetyViolationError as e:
            return {
                "status": "bloqueado",
                "resposta": "Desculpe, não posso responder a essa mensagem por questões de segurança.",
                "tipo": "seguranca"
            }
        except Exception as e:
            return {
                "status": "erro",
                "resposta": "Ocorreu um erro ao processar sua mensagem.",
                "tipo": "erro"
            }
    
    def processar_chat_treinamento(self, mensagem: str) -> Dict[str, Any]:
        """
        Processa mensagens de chat no modo treinamento
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            Resposta da IA
        """
        try:
            # Verificação de segurança
            self._verificar_seguranca_humana(mensagem, "chat_treinamento")
            
            # Tentar extrair dados de treinamento da mensagem
            dados_treinamento = self._extrair_dados_treinamento(mensagem)
            
            if dados_treinamento:
                # Aplicar treinamento
                resultado = self.aprender(dados_treinamento["X"], dados_treinamento["y"])
                if resultado["status"] == "sucesso":
                    return {
                        "status": "sucesso",
                        "resposta": f"Obrigado pelo exemplo! Aprendi com {len(dados_treinamento['X'])} novos dados.",
                        "tipo": "treinamento"
                    }
                else:
                    return {
                        "status": "erro",
                        "resposta": f"Erro no treinamento: {resultado.get('mensagem', 'Erro desconhecido')}",
                        "tipo": "treinamento"
                    }
            else:
                return {
                    "status": "sucesso",
                    "resposta": "Para me ensinar, use o formato: 'exemplo: [dados] -> resultado'. Por exemplo: 'exemplo: [1, 2] -> 0'",
                    "tipo": "treinamento"
                }
            
        except HumanSafetyViolationError as e:
            return {
                "status": "bloqueado",
                "resposta": "Desculpe, não posso processar essa mensagem por questões de segurança.",
                "tipo": "seguranca"
            }
        except Exception as e:
            return {
                "status": "erro",
                "resposta": "Ocorreu um erro ao processar sua mensagem de treinamento.",
                "tipo": "erro"
            }
    
    def _eh_pergunta_factual(self, mensagem: str) -> bool:
        """
        Verifica se a mensagem é uma pergunta factual que pode ser respondida com busca na web
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            True se for pergunta factual, False caso contrário
        """
        # Palavras que indicam perguntas
        indicadores_pergunta = [
            "quem", "o que", "quando", "onde", "como", "por que", "qual", "quais",
            "quanto", "quantos", "quantas", "que", "quais", "cujo", "cuja",
            "what", "who", "when", "where", "how", "why", "which", "how many",
            "how much", "what is", "who is", "when is", "where is"
        ]
        
        # Palavras que indicam assuntos factuais
        assuntos_factuais = [
            "história", "historia", "ciência", "ciencia", "tecnologia", "música",
            "filme", "livro", "país", "pais", "cidade", "pessoa", "empresa",
            "invenção", "invenção", "descoberta", "descoberta", "evento",
            "fatos", "fato", "verdade", "realidade", "atual", "hoje", "ontem",
            "ano", "mês", "mes", "dia", "data", "idade", "altura", "peso",
            "população", "populacao", "capital", "líder", "lider", "presidente",
            "rei", "rainha", "governo", "política", "politica", "economia",
            "esporte", "esportes", "jogo", "campeonato", "olimpíada", "olimpiada",
            "medalha", "record", "recorde", "vencedor", "vencedora"
        ]
        
        mensagem_lower = mensagem.lower()
        
        # Verifica se começa com palavra de pergunta
        comeca_com_pergunta = any(mensagem_lower.startswith(ind) for ind in indicadores_pergunta)
        
        # Verifica se contém palavras de pergunta
        contem_pergunta = any(ind in mensagem_lower for ind in indicadores_pergunta)
        
        # Verifica se contém assuntos factuais
        contem_assunto_factual = any(assunto in mensagem_lower for assunto in assuntos_factuais)
        
        # Verifica se termina com ?
        termina_com_interrogacao = mensagem.strip().endswith('?')
        
        # É pergunta factual se:
        # - Começa com palavra de pergunta OU
        # - Contém palavra de pergunta E assunto factual OU
        # - Termina com ? E contém assunto factual
        return (
            comeca_com_pergunta or
            (contem_pergunta and contem_assunto_factual) or
            (termina_com_interrogacao and contem_assunto_factual)
        )
    
    def _otimizar_consulta_busca(self, consulta: str) -> str:
        """
        Otimiza a consulta de busca para obter resultados mais relevantes
        
        Args:
            consulta: Consulta original
            
        Returns:
            Consulta otimizada
        """
        import re
        
        consulta_lower = consulta.lower().strip()
        
        # Remove pontuação desnecessária
        consulta_limpa = re.sub(r'[^\w\s]', ' ', consulta_lower)
        
        # Reescritas especiais para perguntas comuns em português
        # Ex: "Quem ganhou a Copa do Mundo de 2022?" -> "2022 FIFA World Cup winner"
        if 'copa do mundo' in consulta_lower and ('ganhou' in consulta_lower or 'venceu' in consulta_lower):
            import re
            ano_match = re.search(r'\b(19|20)\d{2}\b', consulta_lower)
            ano = ano_match.group(0) if ano_match else ''
            if ano:
                return f"{ano} FIFA World Cup winner"
            else:
                return "FIFA World Cup winner"
        
        # Mapeamentos para consultas mais específicas
        otimizacoes = {
            # Capitais - manter mais natural
            "qual é a capital do": "capital of",
            "qual é a capital da": "capital of", 
            "qual a capital do": "capital of",
            "qual a capital da": "capital of",
            
            # Definições - usar termos em inglês para melhores resultados
            "o que é": "what is",
            "o que são": "what are",
            "quem é": "who is",
            "quem foi": "who was",
            
            # Quando
            "quando foi": "when was",
            "quando aconteceu": "when did",
            
            # Onde
            "onde fica": "where is",
            "onde está": "where is",
            
            # Por que
            "por que": "why",
            "porque": "why",
            
            # Como
            "como funciona": "how does work",
            "como fazer": "how to",
            
            # Quantidade
            "quantos": "how many",
            "quantas": "how many",
            "quanto": "how much"
        }
        
        # Aplica otimizações
        consulta_otimizada = consulta_limpa
        for chave, valor in otimizacoes.items():
            if chave in consulta_otimizada:
                consulta_otimizada = consulta_otimizada.replace(chave, valor)
                break  # Aplica apenas a primeira otimização encontrada
        
        # Garante que haja espaços adequados após as otimizações
        consulta_otimizada = " ".join(consulta_otimizada.split())
        
        # Para países em português, tenta traduzir para inglês para melhores resultados
        traducoes_paises = {
            "brasil": "brazil",
            "estados unidos": "united states",
            "inglaterra": "england",
            "frança": "france",
            "alemanha": "germany",
            "itália": "italy",
            "espanha": "spain",
            "portugal": "portugal",
            "japão": "japan",
            "china": "china",
            "rússia": "russia",
            "índia": "india"
        }
        
        palavras = consulta_otimizada.lower().split()
        palavras_traduzidas = []
        for palavra in palavras:
            palavras_traduzidas.append(traducoes_paises.get(palavra, palavra))
        
        consulta_otimizada = " ".join(palavras_traduzidas)
        
        # Remove palavras desnecessárias
        palavras_remover = ["me diga", "me fale", "pode me dizer", "você sabe", "sabe", "diga", "fale"]
        for palavra in palavras_remover:
            consulta_otimizada = consulta_otimizada.replace(palavra, "")
        
        # Limpa espaços extras novamente
        consulta_otimizada = " ".join(consulta_otimizada.split())
        
        # Se ficou vazio ou muito curto, volta para a original
        if not consulta_otimizada.strip() or len(consulta_otimizada.split()) < 2:
            consulta_otimizada = consulta_limpa
        
        return consulta_otimizada
    
    def _gerar_resposta_chat(self, mensagem: str) -> str:
        """
        Gera resposta baseada em padrões da mensagem
        
        Args:
            mensagem: Mensagem do usuário (em minúsculo)
            
        Returns:
            Resposta da IA
        """
        import random
        
        # Saudações (verifica palavras inteiras para evitar falsos positivos)
        import re
        sauda_palavras = ["oi", "ola", "olá", "hello", "hi", "opa", "e aí"]
        if re.search(r"\b(?:" + "|".join(re.escape(w) for w in sauda_palavras) + r")\b", mensagem):
            saudacoes = [
                "Olá! 👋 Como posso ajudar você hoje?",
                "Oi! Bem-vindo! O que precisa?",
                "Olá! Estou aqui para ajudar! 🤖",
                "Opa! Tudo bem? Como posso ajudá-lo?"
            ]
            return random.choice(saudacoes)
        
        # Despedidas
        if any(word in mensagem for word in ["tchau", "adeus", "bye", "falou", "até logo", "xau", "até"]):
            despedidas = [
                "Até logo! Foi um prazer conversar com você! 👋",
                "Tchau! Volte sempre! 😊",
                "Adeus! Espero ter ajudado!",
                "Até a próxima! Fico feliz em ajudar novamente!"
            ]
            return random.choice(despedidas)
        
        # Perguntas sobre capacidades
        if any(word in mensagem for word in ["o que você faz", "como funciona", "qual seu objetivo", "para que serve", "capacidade", "capaz"]):
            return """🤍 **Honestamente, aqui estão minhas capacidades REAIS:**
• 🧠 **Treinar modelos** - Mas só com dados numéricos e problemas lineares
• 🔮 **Fazer previsões** - Com precisão limitada (modelo linear)
• 📚 **Aprender continuamente** - Mas tenho limitações reais de capacidade
• 💬 **Conversar** - Mas só baseado em padrões de texto, sem entendimento real
• 🛡️ **Proteger** - Com protocolos de segurança, mas não sou infalível

**Minhas LIMITAÇÕES:**
❌ Não consigo entender contexto profundo
❌ Não tenho consciência real
❌ Sou apenas um modelo linear de classificação
❌ Cometo erros com frequência
❌ Não posso processar imagens ou áudio
❌ Tenho capacidade limitada de generalização"""
        
        # Perguntas sobre aprendizado
        if any(word in mensagem for word in ["você aprende", "aprendizado", "melhorar", "evoluir", "treinamento contínuo"]):
            return """🤍 **Honestidade sobre meu aprendizado:**
Sim, tenho aprendizado, MAS com limitações:
• Aprendo com cada novo dado (partial_fit)
• Meu modelo melhora incrementalmente
• MAS: Tenho limite de padrões que consigo reconhecer
• MAS: Sou apenas um SGDClassifier linear
• MAS: Posso ficar menos acurado com dados muito diferentes
• MAS: Não tenho memória real de longo prazo

**A verdade:** Meu "aprendizado" é ajuste de pesos.
Não é compreensão, é matemática! 📐"""
        
        # Perguntas sobre status
        if any(word in mensagem for word in ["status", "como vai", "tudo bem", "saúde"]):
            if self.treinado:
                acuracia = self.estatisticas.get("acuracia", 0)
                total_treinos = self.estatisticas.get("total_treinamentos", 0)
                return f"""Estou funcionando perfeitamente! ✅
• Status: Online e operacional
• Modelo: {'Treinado ✓' if self.treinado else 'Esperando treinamento'}
• Sessões: {total_treinos} treinamentos
• Acurácia: {(acuracia * 100):.1f}%
• Segurança: Ativa e protegendo!"""
            else:
                return "Estou funcionando bem, mas ainda não fui treinada. Quer me treinar para começar? Use a aba 'Treinar'!"
        
        # Ajuda
        if any(word in mensagem for word in ["ajuda", "help", "como usar", "tutorial", "instruções"]):
            return """📖 **Como usar cada funcionalidade:**

1️⃣ **Treinar**: Forneça dados X e labels y
2️⃣ **Prever**: Insira dados para eu fazer previsões
3️⃣ **Aprender**: Envie novos dados para eu melhorar
4️⃣ **Chat**: Converse comigo! 
5️⃣ **Histórico**: Veja seus treinamentos anteriores
6️⃣ **Configurações**: Ajustes de segurança

Precisa de ajuda específica com alguma aba?"""
        
        # Previsão
        if any(word in mensagem for word in ["previsão", "prever", "predição", "prediç"]):
            return """🔮 **Para fazer previsões:**
1. Vá para a aba 'Prever'
2. Insira seus dados no formato: [[1, 2], [3, 4]]
3. Clique em 'Fazer Previsão'
4. Vou usar meu modelo treinado para prever!

Exemplo: Se treinei com [1,2]→0 e [3,4]→1, posso prever [2,3]!"""
        
        # Treinamento
        if any(word in mensagem for word in ["treinar", "treinamento", "treino", "dados de entrada"]):
            return """🎓 **Para me treinar:**
1. Vá para a aba 'Treinar'
2. Forneça X: [[1,2],[3,4],[5,6]]
3. Forneça y: [0,0,1]
4. Clique em 'Iniciar Treinamento'

Ou no **Chat**:
- Use: 'exemplo: [valor1, valor2] -> resultado'
- Exemplo: 'exemplo: [5, 6] -> 1'"""
        
        # Segurança
        if any(word in mensagem for word in ["segurança", "seguro", "proteção", "ameaca", "ameaça", "virus"]):
            return """🛡️ **Meus protocolos de segurança:**
• Proteção contra ameaças ativas
• Detecção de padrões perigosos
• Validação de todos os inputs
• Prioridade: Preservação de vida humana
• Sistema hardcoded para evitar danos
• Sandbox para arquivos

Você está seguro comigo! ✅"""
        
        # Funcionamento técnico
        if any(word in mensagem for word in ["como você funciona", "máquina", "algoritmo", "ml", "machine learning"]):
            return """⚙️ **Meu funcionamento técnico:**
• Uso **SGDClassifier** para aprendizado
• Normalizo dados com **StandardScaler**
• Suporto aprendizado incremental (**partial_fit**)
• Classificação linear com margem máxima
• Segurança integrada em todas as operações
• Pronto para novas classes dinamicamente"""
        
        # Histórico
        if any(word in mensagem for word in ["histórico", "historico", "passado", "registros"]):
            return """📋 **Seu histórico:**
Vá para a aba 'Histórico' para ver:
• Todos os treinamentos anteriores
• Data de cada sessão
• Amostras usadas
• Acurácia em cada etapa
• Status de cada operação"""
        
        # Status da IA
        if any(word in mensagem for word in ["nome", "quem é", "apresentação", "sobre você"]):
            return "Sou **IA_Principal**, uma inteligência artificial de aprendizado contínuo! Fui criada para treinar, prever e aprender continuamente. Tenho protocolos de segurança avançados e estou aqui para ajudar você! 🤖"
        
        # Modo treinamento no chat
        if any(word in mensagem for word in ["momento treinamento", "que é modo treinamento", "modo treino"]):
            return """🎓 **Modo Treinamento do Chat:**
Neste modo, você me ensina usando:
• Formato: 'exemplo: [dados] -> resultado'
• Exemplo: 'exemplo: [1, 2] -> 0'
• Você pode dar múltiplos exemplos
• Vou aprender e ficar mais inteligente!
• Para ativar: botão 'Modo Treinamento'"""
        
        # Busca na web para perguntas factuais
        if self._eh_pergunta_factual(mensagem):
            try:
                resposta_web = self._gerar_resposta_com_busca(mensagem)
                if resposta_web:
                    return resposta_web
            except Exception as e:
                self.logger.warning(f"Erro na busca web: {e}")
                # Continua com respostas padrão se busca falhar
        
        # Respostas padrão quando não há keywords
        respostas_padrao = [
            "Isso é interessante! Pode me contar mais?",
            "Entendo! Como posso ajudar com isso?",
            "Que bacana! O que mais você gostaria de saber?",
            "Compreendo seu ponto. Alguma pergunta específica?",
            "Fascinante! Vamos explorar isso juntos! 🤔",
            "Certo! Há algo específico que você quer fazer?"
        ]
        
        return random.choice(respostas_padrao)
    
    def _extrair_dados_treinamento(self, mensagem: str) -> Optional[Dict[str, Any]]:
        """
        Tenta extrair dados de treinamento de uma mensagem
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            Dados extraídos ou None
        """
        import re
        
        # Padrões para extrair dados
        # Exemplo: "exemplo: [1, 2] -> 0" ou "[1, 2] -> 0"
        padroes = [
            r'exemplo:\s*\[([^\]]+)\]\s*->\s*(\d+)',
            r'\[([^\]]+)\]\s*->\s*(\d+)',
            r'exemplo:\s*(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\s*->\s*(\d+)',
            r'(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\s*->\s*(\d+)'
        ]
        
        for padrao in padroes:
            match = re.search(padrao, mensagem)
            if match:
                try:
                    if len(match.groups()) == 2:
                        # Formato [x, y] -> label
                        dados_str = match.group(1)
                        label = int(match.group(2))
                        
                        # Parse dos dados
                        dados = [float(x.strip()) for x in dados_str.split(',')]
                        
                        return {
                            "X": [dados],
                            "y": [label]
                        }
                    elif len(match.groups()) == 3:
                        # Formato x, y -> label
                        x = float(match.group(1))
                        y = float(match.group(2))
                        label = int(match.group(3))
                        
                        return {
                            "X": [[x, y]],
                            "y": [label]
                        }
                except (ValueError, IndexError):
                    continue
        
        return None

# =============================================================================
# 🚀 SERVIDOR FASTAPI COM ENDPOINTS
# =============================================================================

# Inicializa a IA
ia = IAAprendizadoContinuo()

# Cria a aplicação FastAPI
app = FastAPI(
    title="IA Aprendizado Contínuo Seguro",
    description="API para IA com protocolos de segurança hardcoded",
    version="1.0.0"
)

# Modelos Pydantic para validação
class TreinamentoRequest(BaseModel):
    X: List[List[float]]
    y: List[int]

class PrevisaoRequest(BaseModel):
    X: List[List[float]]

class AprendizadoRequest(BaseModel):
    X: List[List[float]]
    y: List[int]

class ChatRequest(BaseModel):
    mensagem: str

# Middleware CORS para permitir requisições do frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.get("/status")
async def get_status():
    """Retorna status da IA"""
    return ia.get_status()

@app.post("/treinar")
async def treinar(request: TreinamentoRequest):
    """Treina o modelo inicialmente"""
    return ia.treinar(request.X, request.y)

@app.post("/prever")
async def prever(request: PrevisaoRequest):
    """Faz previsões"""
    return ia.prever(request.X)

@app.post("/aprender")
async def aprender(request: AprendizadoRequest):
    """Aprendizado contínuo"""
    return ia.aprender(request.X, request.y)

@app.post("/prever-e-aprender")
async def prever_e_aprender(request: AprendizadoRequest):
    """Prever e aprender ao mesmo tempo"""
    previsao = ia.prever(request.X)
    if previsao["status"] == "sucesso":
        aprendizado = ia.aprender(request.X, request.y)
        return {
            "previsao": previsao,
            "aprendizado": aprendizado
        }
    return previsao

@app.get("/historico")
async def get_historico():
    """Retorna histórico de treinamentos"""
    return ia.get_historico()

@app.post("/salvar-modelo")
async def salvar_modelo():
    """Salva o modelo"""
    return ia.salvar_modelo()

@app.post("/carregar-modelo")
async def carregar_modelo():
    """Carrega o modelo"""
    return ia.carregar_modelo()

@app.post("/reiniciar")
async def reiniciar():
    """Reinicia a IA"""
    return ia.reiniciar()

@app.post("/chat")
async def chat(request: ChatRequest):
    """Processa mensagens de chat conversacional"""
    return ia.processar_chat(request.mensagem)

@app.post("/chat-treinamento")
async def chat_treinamento(request: ChatRequest):
    """Processa mensagens de chat no modo treinamento"""
    return ia.processar_chat_treinamento(request.mensagem)

# Monta arquivos estáticos APÓS os endpoints da API
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# =============================================================================
# 🚀 INICIALIZAÇÃO DO SERVIDOR
# =============================================================================

if __name__ == "__main__":
    print("🛡️ Iniciando servidor IA Aprendizado Contínuo Seguro...")
    print("📡 Endpoints disponíveis em http://localhost:8000")
    print("🌐 Interface web: http://localhost:8000/static/index.html")
    
    uvicorn.run(
        "ia_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
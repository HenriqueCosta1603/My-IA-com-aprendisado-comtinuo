# ia_aprendizado_continuo_seguro.py
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
            
            # Normaliza com scaler existente
            X_scaled = self.scaler.transform(X_array)
            
            # Aprendizado incremental
            self.modelo.partial_fit(X_scaled, y_array, classes=np.unique(y_array))
            
            # Recalcula acurácia aproximada (simplificada)
            self.estatisticas["total_treinamentos"] += 1
            
            # Registra no histórico
            self.historico_treinamentos.append({
                "data": datetime.now().isoformat(),
                "tipo": "aprendizado_continuo",
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
        """Retorna status da IA"""
        return {
            "nome": self.nome,
            "treinado": self.treinado,
            "estatisticas": self.estatisticas,
            "protocolos_seguranca": self.core_ethics,
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

# Middleware CORS para permitir requisições do frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# 🚀 INICIALIZAÇÃO DO SERVIDOR
# =============================================================================

if __name__ == "__main__":
    print("🛡️ Iniciando servidor IA Aprendizado Contínuo Seguro...")
    print("📡 Endpoints disponíveis em http://localhost:8000")
    print("🌐 Interface web: http://localhost:8000/static/index.html")
    
    uvicorn.run(
        "ia_aprendizado_continuo_seguro:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
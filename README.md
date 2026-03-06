# 🤖 IA Aprendizado Contínuo Seguro

Uma interface web completa para uma IA de aprendizado contínuo com protocolos de segurança hardcoded para proteção incondicional à vida humana.

## 🛡️ Características de Segurança

- **Protocolo de Preservação Humana**: Hardcoded e inegociável
- **Detector de Ameaças**: Bloqueia automaticamente conteúdo perigoso
- **Sandbox de Arquivos**: Isolamento completo de operações de arquivo
- **Navegação Web Segura**: Apenas leitura, sem ações modificadoras

## 🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o Servidor
```bash
python ia_backend.py
```

### 3. Abrir a Interface Web
Abra seu navegador em: `http://localhost:8000`

## 📋 Funcionalidades

### Treinar
- Treinamento inicial do modelo com dados personalizados
- Formato: Arrays de números para X (features) e y (labels)

### Prever
- Fazer previsões com dados novos
- Resultados em tempo real

### Aprender
- Aprendizado contínuo: adicionar novos dados sem retrainar do zero
- Melhora progressiva do modelo

### Histórico
- Visualizar todos os treinamentos realizados
- Estatísticas de performance

### Configurações
- Salvar/carregar modelos
- Reiniciar IA
- Status de segurança ativo

## 🔧 Arquitetura

- **Backend**: FastAPI com Python
- **Frontend**: HTML/CSS/JavaScript puro
- **IA**: Scikit-learn com SGDClassifier para aprendizado incremental
- **Segurança**: Múltiplas camadas de proteção hardcoded

## 📊 Exemplo de Uso

```python
# Treinamento inicial
X = [[1, 2], [2, 3], [3, 4], [4, 5]]
y = [0, 0, 1, 1]

# Previsão
novos_dados = [[2.5, 3.5]]

# Aprendizado contínuo
novos_X = [[6, 7], [7, 8]]
novos_y = [1, 1]
```

## ⚠️ Avisos de Segurança

Este sistema foi projetado com o princípio fundamental: **"Primeiro, não causar dano"**.

- Todas as entradas são verificadas automaticamente
- Conteúdo perigoso é bloqueado
- Operações de arquivo são isoladas em sandbox
- Navegação web é limitada a leitura apenas

## 📝 Licença

Código de Honra da IA - Todos os direitos reservados.
Proteção incondicional à vida humana.
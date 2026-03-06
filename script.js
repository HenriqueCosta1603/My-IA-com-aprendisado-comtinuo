// script.js - Interface JavaScript para IA Aprendizado Contínuo

const API_BASE = 'http://localhost:8000';

// Elementos DOM
const connectionStatus = document.getElementById('connectionStatus');
const connectionText = document.getElementById('connectionText');
const statTotalTrainings = document.getElementById('statTotalTrainings');
const statAccuracy = document.getElementById('statAccuracy');
const statPredictions = document.getElementById('statPredictions');
const statThreatsBlocked = document.getElementById('statThreatsBlocked');

// Verificar conexão com o servidor
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();

        if (response.ok) {
            connectionStatus.classList.add('connected');
            connectionText.textContent = 'Conectado';
            updateStats(data);
        } else {
            throw new Error('Servidor indisponível');
        }
    } catch (error) {
        connectionStatus.classList.remove('connected');
        connectionText.textContent = 'Desconectado';
        console.error('Erro de conexão:', error);
    }
}

// Atualizar estatísticas
function updateStats(data) {
    if (data.estatisticas) {
        statTotalTrainings.textContent = data.estatisticas.total_treinamentos || 0;
        statAccuracy.textContent = `${(data.estatisticas.acuracia * 100 || 0).toFixed(1)}%`;
        statPredictions.textContent = data.estatisticas.total_previsao || 0;
        statThreatsBlocked.textContent = data.estatisticas.ameacas_bloqueadas || 0;
    }
}

// Sistema de abas
function initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remover classe active de todas as abas
            tabs.forEach(t => t.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Adicionar classe active à aba clicada
            tab.classList.add('active');
            const tabId = tab.dataset.tab;
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Função de treinamento
async function treinar() {
    const trainX = document.getElementById('trainX').value;
    const trainY = document.getElementById('trainY').value;

    try {
        const X = JSON.parse(trainX);
        const y = JSON.parse(trainY);

        const response = await fetch(`${API_BASE}/treinar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ X, y }),
        });

        const result = await response.json();
        showToast(result.mensagem || 'Treinamento realizado!', response.ok ? 'success' : 'error');
        checkConnection(); // Atualizar stats

    } catch (error) {
        showToast('Erro no treinamento: ' + error.message, 'error');
    }
}

// Função de previsão
async function prever() {
    const predictX = document.getElementById('predictX').value;

    try {
        const X = JSON.parse(predictX);

        const response = await fetch(`${API_BASE}/prever`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ X }),
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('predictResult').style.display = 'block';
            document.getElementById('predictOutput').textContent = JSON.stringify(result.previsao, null, 2);
            showToast('Previsão realizada!', 'success');
        } else {
            showToast(result.mensagem || 'Erro na previsão', 'error');
        }
        checkConnection(); // Atualizar stats

    } catch (error) {
        showToast('Erro na previsão: ' + error.message, 'error');
    }
}

// Função de aprendizado contínuo
async function aprender() {
    const learnX = document.getElementById('learnX').value;
    const learnY = document.getElementById('learnY').value;

    try {
        const X = JSON.parse(learnX);
        const y = JSON.parse(learnY);

        const response = await fetch(`${API_BASE}/aprender`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ X, y }),
        });

        const result = await response.json();
        showToast(result.mensagem || 'Aprendizado realizado!', response.ok ? 'success' : 'error');
        checkConnection(); // Atualizar stats

    } catch (error) {
        showToast('Erro no aprendizado: ' + error.message, 'error');
    }
}

// Carregar histórico
async function carregarHistorico() {
    try {
        const response = await fetch(`${API_BASE}/historico`);
        const data = await response.json();

        const tbody = document.getElementById('historyTable');
        tbody.innerHTML = '';

        if (data.historico && data.historico.length > 0) {
            data.historico.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${new Date(item.data).toLocaleString()}</td>
                    <td>${item.tipo}</td>
                    <td>${item.amostras}</td>
                    <td>${(item.acuracia * 100).toFixed(1)}%</td>
                    <td><span class="badge badge-success">${item.status}</span></td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhum histórico disponível</td></tr>';
        }

    } catch (error) {
        showToast('Erro ao carregar histórico: ' + error.message, 'error');
    }
}

// Salvar modelo
async function salvarModelo() {
    try {
        const response = await fetch(`${API_BASE}/salvar-modelo`, {
            method: 'POST',
        });

        const result = await response.json();
        showToast(result.mensagem || 'Modelo salvo!', response.ok ? 'success' : 'error');

    } catch (error) {
        showToast('Erro ao salvar modelo: ' + error.message, 'error');
    }
}

// Carregar modelo
async function carregarModelo() {
    try {
        const response = await fetch(`${API_BASE}/carregar-modelo`, {
            method: 'POST',
        });

        const result = await response.json();
        showToast(result.mensagem || 'Modelo carregado!', response.ok ? 'success' : 'error');
        checkConnection(); // Atualizar stats

    } catch (error) {
        showToast('Erro ao carregar modelo: ' + error.message, 'error');
    }
}

// Reiniciar IA
async function reiniciarIA() {
    if (!confirm('Tem certeza que deseja reiniciar a IA? Todos os dados serão perdidos.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/reiniciar`, {
            method: 'POST',
        });

        const result = await response.json();
        showToast(result.mensagem || 'IA reiniciada!', response.ok ? 'success' : 'error');
        checkConnection(); // Atualizar stats

    } catch (error) {
        showToast('Erro ao reiniciar IA: ' + error.message, 'error');
    }
}

// Sistema de notificações
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
        ${message}
    `;

    toastContainer.appendChild(toast);

    // Remover toast após 5 segundos
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// === FUNÇÕES DO CHATBOT ===

// Estado do chat
let chatMode = 'conversacao'; // 'conversacao' ou 'treinamento'

// Adicionar mensagem ao chat
function adicionarMensagem(texto, tipo, timestamp = null) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${tipo}-message`;

    const time = timestamp || new Date().toLocaleTimeString();

    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${tipo === 'user' ? 'fa-user' : 'fa-robot'}"></i>
        </div>
        <div class="message-content">
            <p>${texto}</p>
            <small class="message-time">${time}</small>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Enviar mensagem
async function enviarMensagem() {
    const input = document.getElementById('chatInput');
    const texto = input.value.trim();

    if (!texto) return;

    // Adicionar mensagem do usuário
    adicionarMensagem(texto, 'user');
    input.value = '';

    // Mostrar indicador de digitação
    mostrarDigitando();

    try {
        let response;
        let result;

        if (chatMode === 'treinamento') {
            // Modo treinamento - tentar extrair dados de treinamento da mensagem
            response = await fetch(`${API_BASE}/chat-treinamento`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mensagem: texto }),
            });
        } else {
            // Modo conversação - chat normal
            response = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mensagem: texto }),
            });
        }

        result = await response.json();

        if (response.ok) {
            adicionarMensagem(result.resposta, 'ai');
        } else {
            adicionarMensagem('Desculpe, ocorreu um erro: ' + (result.mensagem || 'Erro desconhecido'), 'ai');
        }

    } catch (error) {
        adicionarMensagem('Erro de conexão com o servidor. Tente novamente.', 'ai');
        console.error('Erro no chat:', error);
    }

    // Esconder indicador de digitação
    esconderDigitando();
}

// Mostrar indicador de digitação
function mostrarDigitando() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message';
    typingDiv.id = 'typingIndicator';

    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p><i class="fas fa-circle-notch fa-spin"></i> Digitando...</p>
        </div>
    `;

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Esconder indicador de digitação
function esconderDigitando() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Handle Enter key
function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        enviarMensagem();
    }
}

// Limpar chat
function limparChat() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = `
        <div class="message ai-message">
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p>Olá! Sou uma IA de aprendizado contínuo. Como posso ajudar você hoje?</p>
                <small class="message-time">Agora</small>
            </div>
        </div>
    `;
}

// Modo treinamento
function modoTreinamento() {
    chatMode = 'treinamento';
    adicionarMensagem('Modo treinamento ativado! Agora você pode me ensinar com exemplos. Use o formato: "exemplo: [dados] -> resultado"', 'ai');
    atualizarBotoesModo();
}

// Modo conversação
function modoConversacao() {
    chatMode = 'conversacao';
    adicionarMensagem('Modo conversação ativado! Podemos conversar normalmente agora.', 'ai');
    atualizarBotoesModo();
}

// Atualizar botões de modo
function atualizarBotoesModo() {
    const botoes = document.querySelectorAll('.chat-options .btn');
    botoes.forEach(btn => {
        if ((chatMode === 'treinamento' && btn.textContent.includes('Treinamento')) ||
            (chatMode === 'conversacao' && btn.textContent.includes('Conversação'))) {
            btn.classList.add('btn-primary');
            btn.classList.remove('btn-outline');
        } else {
            btn.classList.add('btn-outline');
            btn.classList.remove('btn-primary');
        }
    });
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    checkConnection();
    atualizarBotoesModo();

    // Verificar conexão a cada 30 segundos
    setInterval(checkConnection, 30000);
});
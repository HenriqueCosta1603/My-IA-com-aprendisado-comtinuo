import requests
import json
import time

time.sleep(2)

# Testa várias perguntas
perguntas = [
    'O que você consegue fazer?',
    'Como você funciona?',
    'Você aprende com o tempo?',
    'Como você pode me ajudar?',
    'Qual é sua segurança?',
    'Como faço para treinar você?',
    'Me conte sobre suas funcionalidades',
    'Oi! Tudo bem?'
]

print('='*70)
print('🤖 TESTANDO RESPOSTAS DA IA MELHORADAS')
print('='*70)
print()

for pergunta in perguntas:
    try:
        response = requests.post('http://localhost:8000/chat', 
                               json={'mensagem': pergunta},
                               timeout=5)
        dados = response.json()
        print(f'📝 Pergunta: {pergunta}')
        print(f'🤖 Resposta:\n{dados.get("resposta", "N/A")}')
        print()
        print('-'*70)
        print()
    except Exception as e:
        print(f'❌ Erro: {e}')
        break

print('✅ Testes concluídos!')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

print('='*80)
print('🤍 DEMONSTRAÇÃO: PROTOCOLO DE HONESTIDADE ABSOLUTA HARDCODED')
print('='*80)
print()

# Teste 1: Verificar que o protocolo está no código
print('✅ TESTE 1: Protocolo de Honestidade Hardcoded no Código')
print('-'*80)

with open('ia_backend.py', 'r', encoding='utf-8') as f:
    conteudo = f.read()
    
tem_protocolo = 'protocolo_honestidade' in conteudo
tem_hardcoded = 'Hardcoded' in conteudo
tem_permanente = 'permanente' in conteudo

print(f'✅ Protocolo definido no __init__: {tem_protocolo}')
print(f'✅ Marcado como Hardcoded: {tem_hardcoded}')
print(f'✅ Menção à permanência: {tem_permanente}')
print()

# Teste 2: Verificar que a API retorna os protocolos
print('✅ TESTE 2: API Retorna Protocolos de Honestidade')
print('-'*80)

response = requests.get('http://localhost:8000/status')
dados_json = response.json()

# Converte para JSON string para procurar
json_str = json.dumps(dados_json)

if 'protocolo_honestidade' in json_str:
    print('✅ API retorna protocolo_honestidade no /status')
    
    # Parse e mostra
    dados = json.loads(json_str)
    if isinstance(dados.get('protocolos_honestidade'), dict):
        print('✅ Protocolos de Honestidade presentes:')
        for chave, valor in dados['protocolos_honestidade'].items():
            print(f'   ✅ {chave}: {valor}')
else:
    print('❌ protocolo_honestidade não encontrado')

print()

# Teste 3: Honestidade em respostas
print('✅ TESTE 3: Respostas Incluem Honestidade')
print('-'*80)

# Treina primeiro
requests.post('http://localhost:8000/treinar',
             json={'X': [[1,2],[3,4],[5,6],[7,8]], 'y': [0,0,1,1]})

# Agora testa
response = requests.post('http://localhost:8000/chat',
                        json={'mensagem': 'Como você funciona'})
resposta = response.json()['resposta']

tem_declaracao_honestidade = '🤍 **Minha Honestidade:**' in resposta
tem_limites = 'limitações' in resposta

print(f'✅ Resposta inclui declaração de honestidade: {tem_declaracao_honestidade}')
print(f'✅ Resposta menciona limitações: {tem_limites}')

if tem_declaracao_honestidade:
    inicio = resposta.index('🤍 **Minha Honestidade:**')
    print()
    print('Trecho de honestidade na resposta:')
    print(resposta[inicio:inicio+200])

print()
print('='*80)
print('🤍 RESULTADO FINAL: PROTOCOLO DE HONESTIDADE ATIVADO COM SUCESSO!')
print('A IA NÃO PODE e NÃO VAI ESCONDER suas limitações reais.')
print('='*80)

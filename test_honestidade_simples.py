import requests

print('Testando Protocolo de Honestidade')
print('='*80)

response = requests.post('http://localhost:8000/chat', 
                        json={'mensagem': 'Como você funciona'},
                        timeout=5)
dados = response.json()
resposta = dados.get('resposta', '')

print('Pergunta: Como você funciona')
print('-'*80)
print('RESPOSTA:')
print(resposta)
print()
print('='*80)
print('Verificação:')
print(f'✅ Tem "SGDClassifier": {"SGDClassifier" in resposta}')
print(f'✅ Tem "Linear": {"Linear" in resposta}')
print(f'✅ Tem "MAS": {"MAS" in resposta}')
print(f'✅ Tem "limitações": {"limitações" in resposta}')
print(f'✅ Tem "honestidade": {"honestidade" in resposta or "Honestidade" in resposta}')

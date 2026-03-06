import sys
sys.path.append('.')
from ia_backend import IAAprendizadoContinuo

ia = IAAprendizadoContinuo()
mensagem = 'Qual é a capital do Brasil?'
otimizada = ia._otimizar_consulta_busca(mensagem)
print(f'Consulta original: {mensagem}')
print(f'Consulta otimizada: "{otimizada}"')
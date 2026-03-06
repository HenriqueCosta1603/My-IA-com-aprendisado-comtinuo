# Cliente de exemplo
import requests

# URL base
BASE_URL = "http://localhost:8000"

# 1. Ver status
print(requests.get(f"{BASE_URL}/status").json())

# 2. Treinar inicialmente
dados_treino = {
    "X": [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]],
    "y": [0, 0, 1, 1, 1]
}
print(requests.post(f"{BASE_URL}/treinar", json=dados_treino).json())

# 3. Fazer previsão
dados_teste = {"X": [[2.5, 3.5]]}
print(requests.post(f"{BASE_URL}/prever", json=dados_teste).json())

# 4. Aprender com novos dados (aprendizado contínuo!)
novos_dados = {
    "X": [[6, 7], [7, 8]],
    "y": [1, 1]
}
print(requests.post(f"{BASE_URL}/aprender", json=novos_dados).json())

# 5. Prever E aprender ao mesmo tempo
dados_completo = {
    "X": [[8, 9], [9, 10]],
    "y": [1, 1]
}
print(requests.post(f"{BASE_URL}/prever-e-aprender", json=dados_completo).json())
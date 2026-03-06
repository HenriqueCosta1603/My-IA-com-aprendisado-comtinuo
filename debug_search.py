import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from ia_backend import IAAprendizadoContinuo
ia = IAAprendizadoContinuo()
res = ia._buscar_na_web('Quem ganhou a Copa do Mundo de 2022?')
import json
print(json.dumps(res, indent=2, ensure_ascii=False))

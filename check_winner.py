import requests

headers={'User-Agent':'Mozilla/5.0'}
resp = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/2022_FIFA_World_Cup', headers=headers)
print(resp.status_code)
# try to parse json if possible
try:
    data = resp.json()
    print(data.get('extract'))
except Exception as e:
    print('failed parse', e)
    print(resp.text[:2000])

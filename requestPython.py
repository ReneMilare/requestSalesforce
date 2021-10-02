import requests
import json
import codecs
import time

# Parâmetros de entrada
CLIENT_ID = '3MVG9JEx.BE6yifOwTVbciau3t8VTCz8Bnj27Lcy6tg5kzbpepiDHLFA.KLtt8BVoQGIryIKdQwO6Jzc4vORg'
CLIENT_SECRET = '8954015E80FA0157493515B6B896B86223E557D7214D6BF7974329C2305A11C9'
USERNAME = 'chama@integracao.com.br'
USER_TOKEN = '7CoLrOU4UZ12jIdmn4Xhmqk4'
PASSWORD = 'Admin123'

SOBJECT = 'Account'

# Pegando o token
url_token = 'https://login.salesforce.com/services/oauth2/token'

payload_token = {
  'grant_type': 'password',
  'client_id': CLIENT_ID,
  'client_secret': CLIENT_SECRET,
  'username': USERNAME,
  'password': PASSWORD + USER_TOKEN
}

print('\n' + '*'*50)
print('\nPegando o seu token')
print(url_token + '\n')
r_token = requests.post(url_token, data=payload_token)
rStr_token = json.dumps(r_token.json())
rJson_token = json.loads(rStr_token)
print(rJson_token['access_token'] + '\n')

# Inserindo 1 account
url_1account = rJson_token['instance_url'] + '/services/data/v52.0/sobjects/' + SOBJECT

# Esse header será usado em todos os requests daqui para baixo
header = {
  'Authorization': rJson_token['token_type'] + ' ' + rJson_token['access_token'],
  'Content-Type': 'application/json'
}

payload_1account = { 
  'Name': 'Rene Milare (1 account)',
  'Description': 'milarerp@gmail.com',
  'Website': 'https://github.com/ReneMilare'
}

print('\n' + '*'*50)
print('\nTeste criando 1 account')
print(url_1account + '\n')
r_1account = requests.post(url_1account, data=json.dumps(payload_1account), headers=header)
rStr_1account = json.dumps(r_1account.json())
rJson_1account = json.loads(rStr_1account)
print('Id -> ' + rJson_1account['id'])
print('Sucesso -> ' + str(rJson_1account['success']))
print('\n')

# Abrindo o job
url_open_job = rJson_token['instance_url'] + '/services/data/v52.0/jobs/ingest'

payload_open_job = {
  'operation' : 'insert',
  'object' : SOBJECT,
  'contentType' : 'CSV',
  'lineEnding' : 'LF'
}

print('\n' + '*'*50)
print('\nAbrindo o Job')
print(url_open_job + '\n')
r_open_job = requests.post(url_open_job, data=json.dumps(payload_open_job), headers=header)
rStr_open_job = json.dumps(r_open_job.json())
rJson_open_job = json.loads(rStr_open_job)
print('Id -> '+ rJson_open_job['id'] + '\nStatus do job -> ' + rJson_open_job['state'])
print('\n')

# Subindo o arquivo CSV com os accounts
url_accounts = rJson_token['instance_url'] + '/' + rJson_open_job['contentUrl']

# Nesse momento o header muda um pouco
header_accounts = {
  'Authorization': rJson_token['token_type'] + ' ' + rJson_token['access_token'],
  'Content-Type': 'text/csv'
}

print('\n' + '*'*50)
print('\nSubindo arquivo CSV')
print(url_accounts + '\n')
r_accounts = requests.put(url_accounts, data=codecs.open('accounts.txt','r').read(), headers=header_accounts)
print('Status code da resposta -> ' + str(r_accounts.status_code) + '\n')

# Fechando o Job
url_close_job = url_open_job + '/' + rJson_open_job['id']

payload_close_job = {
  'state': 'UploadComplete'
}

print('\n' + '*'*50)
print('\nFechando o Job')
print(url_close_job + '\n')
r_close_job = requests.patch(url_close_job, data=json.dumps(payload_close_job), headers=header)
rStr_close_job = json.dumps(r_close_job.json())
rJson_close_job = json.loads(rStr_close_job)
print('Id -> ' + rJson_close_job['id'])
print('Status -> ' + rJson_close_job['state'])
print('\n')

# Obtendo Status do Job
print('\n' + '*'*50)
print('\nObtendo status do Job')
print(url_close_job + '\n')
r_status_job = requests.get(url_close_job, headers=header)
rStr_status_job = json.dumps(r_status_job.json())
rJson_status_job = json.loads(rStr_status_job)
print('Status -> ' + rJson_status_job['state'])
print('Id do job -> ' + rJson_status_job['id'])
print('Registros processados -> ' + str(rJson_status_job['numberRecordsProcessed']))
print('Registros com falha -> ' + str(rJson_status_job['numberRecordsFailed']))
print('\n')

while rJson_status_job['state'] != 'JobComplete':
  time.sleep(5)
  r_status_job = requests.get(url_close_job, headers=header)
  rStr_status_job = json.dumps(r_status_job.json())
  rJson_status_job = json.loads(rStr_status_job)
  print('Status -> ' + rJson_status_job['state'])
  print('Id do job-> ' + rJson_status_job['id'])
  print('Registros processados -> ' + str(rJson_status_job['numberRecordsProcessed']))
  print('Registros com falha -> ' + str(rJson_status_job['numberRecordsFailed']))
  print('\n')

  if rJson_status_job['state'] == 'Failed':
    print(rJson_status_job)
    break

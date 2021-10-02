# requestSalesforce

## Script em python que utiliza as APIs padrões do salesforce, tais como o API em massa

### Após criar o Connected App e o usuário de integração no Salesforce, é só passar as credenciais nos seguintes campos. Para a criação dessas credenciais sugiro o seguinte link: https://www.sfdcstop.com/2019/01/how-to-connect-to-salesforce-with.html

![image](https://user-images.githubusercontent.com/24875841/135731822-0e601bc3-3905-413f-973d-4fa803f259f2.png)

### O último parâmetro é o sobject em que você quer fazer a operação de insert, nessa caso no sobjct Account.

### Nesse repositório tem um arquivo chamado accounts.txt, nele estão as contas que vão ser inseridos. Note que a primeira linha são campos api name do Salesforce.

![image](https://user-images.githubusercontent.com/24875841/135731964-91c2598f-70b8-49fd-9b2e-498c6e5c28a5.png)

### O jeito mais fácil de rodar é escript é pelo docker. Abrindo o terminal dentro do diretório execute o camando: 
```
  docker-compose up
```

### outro jeito é executando por uma venv, para isso sugiro o link: https://jozimarback.medium.com/utilizando-pip-freeze-corretamente-f9a305c691c0

### Deixei uma parte do script para criar uma única conta no salesforce, qualquer coisa é só comentar essa parte, só não comentar a parte do header.

![image](https://user-images.githubusercontent.com/24875841/135732104-a358515a-9b5e-4296-945e-2db3dd524b45.png)

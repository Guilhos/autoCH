# Automação de Carga Horária

## OBJETIVO

Computar a carga horária dos funcionários da Empresa Júnior [OPTIMUS Jr Controle e Automação](optimusjr.com.br)

## COMO FOI FEITO
O programa se utiliza da [API Gmail](https://developers.google.com/gmail/api/guides?hl=pt-br) e da [API Google Sheets](https://developers.google.com/sheets/api/guides/concepts?hl=pt-br) do Google. Através dessas ferramentas, se colhe o email enviado para um GMAIL a minha escolha nesse caso, cargahoraria@optimusjr.com.br

Esse email deve seguir este formato específico:
<div>
  <img src="https://cdn.discordapp.com/attachments/707954953280421928/1211767557183246396/image.png?ex=65ef657b&is=65dcf07b&hm=3a7c2a441e3a62333e850d8a86c48612abbbe3039dcc05a48e1e984203ee076a&" alt="Formato do email">
</div>

Esse formato é necessário, pois o programa NÃO tem algoritmo de busca para os horários, então se faz necessário que o texto seja estático!
As informações: REMETENTE, DATA, HORA DE ENTRADA e HORA DE SAÍDA serão enviados ao esse [SPREADSHEET](https://docs.google.com/spreadsheets/d/1-cOVrhnu8hNbmfhdCZPCJHeuV_mpEDnjn2NtcdlELfQ) ⚠️

OBS.: Caso não esteja conseguindo acessar o SPREADSHEET, pode ser que você não faça parte da organização OPTIMUS Jr (ou eu atualizei o SPREADSHEET e esqueci de mudar esse texto 😝)

## O CÓDIGO

É um simples script em Python, deve rodar em qualquer computador sem muitos problemas (os únicos que encontrei foram por conta das credenciais). Caso esteja tendo o mesmo problema me contate!

Antes das API's é necessário instalar as dependências do Google, coloque o seguinte código no seu terminal:

<img src="https://cdn.discordapp.com/attachments/1105298491078606941/1211780468366647357/image.png?ex=65ef7181&is=65dcfc81&hm=5adedb59c1b1614d79e8d62211e26bb9f2c91e3a624664d9234e01e32f7b6bef&" alt="$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib">

### Autenticação:
Existem 2 funções de autenticação, gmail_authenticate() e sheet_authenticate(). Uma vez que as credenciais estejam no seu workspace (pra quem estiver usando o VS Code) elas devem conseguir rodar sem muitos problemas! Após as suas primeiras execuções serão criados 2 arquivos no workspace, token.pickle (GMAIL) e token1.pickle (SHEETS), eles irão servir para o google saber que você deu permissão ao programa para utilizar dos seus dados.

❗PARA FUNCIONAR VOCÊ PRECISA TER AS CREDENCIAIS ❗

### API GMAIL
Existem 4 funções que utilizam essa API

  🔹search_messages(service, query) ▶️ Utilizado para procurar o EMAIL que contenha determinado texto (query). Retorna uma lista contendo os EMAILS criptografados em BYTECODE
  
  🔹read_message(service, message) ▶️ Utilizado para obter as informações do EMAIL, recebe um EMAIL criptografado (message) e retorna uma lista contendo REMETENTE, DATA, ENTRADA e SAÍDA, respectivamente.
  
  🔹delete_message(service, query) ▶️ Utilizado para deletar o EMAIL que contenha determinado texto (query). Importante para não lermos o mesmo EMAIL repetidas vezes!
  
  🔹clear(text) ▶️ Utilizado dentro do read_message(), para limpar o texto e criar uma nova pasta quando se lê o SUBJECT. (Também não entendi direito pra que funciona, mas funciona 😁😁)
  

### API GOOGLE SHEETS
Existe apenas 1 função que utiliza essa API, a update_values(service, spreadsheets_id, range_name, value_input_option, remetente, data, Entrada, Saída). Agora para que serve cada parâmetro?

  🔹service ▶️ Necessário para acessar informações da API
  
  🔹spreadsheets_id ▶️ Endereço da nossa planilha

  🔹range_name ▶️ Intervalo da planilha que queremos alterar
  
  🔹value_input_option ▶️ Opção de entrada de valores (você pode procurar por outras opções clicando [aqui](https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption?hl=pt-br))
  
  🔹Os outros são autoexplicativos!

Na planilha:

<img src="https://cdn.discordapp.com/attachments/1105298491078606941/1211776911534067782/image.png?ex=65ef6e31&is=65dcf931&hm=fcb7c2a56d45ecabbad8f0b7312db2ac5d12a59688d8c18f18808936295763f0&" alt="Imagem dos Dados na Planilha">

### GUI
Foi utilizada a [Tkinter](https://docs.python.org/pt-br/3/library/tkinter.html) para a criação da interface do usuário, a interface em si é bem simples, consta com 4 botões:

<img src="https://cdn.discordapp.com/attachments/1105299182899703888/1212047432427380787/image.png?ex=65f06a22&is=65ddf522&hm=9eeb55dc2afd098c0892b3f4daa9591ee8ee630120cf9e66def8c37ed8b4841f&" alt="GUI do Programa">

  🔹Github ▶️ Abre uma janela no seu navegador padrão trazendo para esse github
  
  🔹Planilha ▶️ Abre uma janela no seu navegador padrão levando para a planilha
  
  🔹Deletar EMAILs ▶️ Executa a função delete_message()
  
  🔹ENVIAR DADOS ▶️ Executa o programa em si

### EXECUTÁVEL
O programa foi transformado em .exe utilizando o [pyinstaller](https://pyinstaller.org/en/stable/)!

### ERROS
Se você encontrou algum tipo de erro, verifique o console (ele abre junto com o executável). Os erros mais prováveis são:
  
  🔸As credenciais estão fora da pasta, incorretas ou desatualizadas
  🔸Está utilizando o email incorreto na permissão das credenciais
  🔸O email que você está utilizando não tem acesso a planilha

Se encontrar outros erros além desses entre em contato!

## NFC

A NFC precisa ser atualizada constantemente de acordo com as alterações no programa. O cartão utilizado está colado na sede com um "P" escrito!

❗TALVEZ TODO O PROGRAMA SEJA ALTERADO, POIS EXISTE A POSSIBILIDADE DA NFC SER FEITA UTILIZANDO UM ARDUINO ❗

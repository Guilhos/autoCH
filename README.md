# Automação de Carga Horária

## OBJETIVO

Computar a carga horária dos funcionários da Empresa Júnior [OPTIMUS Jr Controle e Automação](optimusjr.com.br)

## COMO FOI FEITO
O programa se utiliza da [API Gmail](https://developers.google.com/gmail/api/guides?hl=pt-br) e da [API Google Sheets](https://developers.google.com/sheets/api/guides/concepts?hl=pt-br) do Google. Através dessas ferramentas, se colhe o email enviado para um GMAIL a minha escolha nesse caso, horadesede@gmail.com ⚠️

Esse email deve seguir este formato específico:
<div>
  <img src="https://cdn.discordapp.com/attachments/707954953280421928/1211767557183246396/image.png?ex=65ef657b&is=65dcf07b&hm=3a7c2a441e3a62333e850d8a86c48612abbbe3039dcc05a48e1e984203ee076a&" alt="Formato do email">
</div>

Esse formato é necessário, pois o programa NÃO tem algoritmo de busca para os horários, então se faz necessário que o texto seja estático!
As informações: REMETENTE, DATA, HORA DE ENTRADA e HORA DE SAÍDA serão enviados ao esse [SPREADSHEET](https://docs.google.com/spreadsheets/d/136BgdSmEmHdqMHRvK0dOsgXYjqKdAyicNEtGlMGLw3E/edit#gid=0) ⚠️

OBS.: Caso não esteja conseguindo acessar o SPREADSHEET, pode ser que você não faça parte da organização OPTIMUS Jr. ou eu atualizei o SPREADSHEET e esqueci de mudar esse texto 😝

OBS..: ⚠️ = SUJEITO A ALTERAÇÃO

## O CÓDIGO

É um simples script em Python, deve rodar em qualquer computador sem muitos problemas (os únicos que encontrei foram por conta das credenciais). Caso esteja tendo o mesmo problema me contate!

### Autenticação:
Existem 2 funções de autenticação, gmail_authenticate() e sheet_authenticate(). Uma vez que as credenciais estejam no seu workspace (pra quem estiver usando o VS Code) elas devem conseguir rodar sem muitos problemas! Após as suas primeiras execuções serão criados 2 arquivos no workspace, token.pickle (GMAIL) e token1.pickle (SHEETS), eles irão servir para o google saber que você deu permissão ao programa para utilizar dos seus dados.

❗PARA FUNCIONAR VOCÊ PRECISA TER AS CREDENCIAIS ❗

### API GMAIL
Existem 4 funções que utilizam essa API

  - search_messages(service, query): Utilizado para procurar o EMAIL que contenha determinado texto (query). Retorna uma lista contendo os EMAILS criptografados em BYTECODE
  - read_message(service, message): Utilizado para obter as informações do EMAIL, recebe um EMAIL criptografado (message) e retorna uma lista contendo REMETENTE, DATA, ENTRADA e SAÍDA, respectivamente.
  - delete_message(service, query): Utilizado para deletar o EMAIL que contenha determinado texto (query). Importante para não lermos o mesmo EMAIL repetidas vezes!
  - clear(text): Utilizado dentro do read_message(), para limpar o texto e criar uma nova pasta quando se lê o SUBJECT. (Também não entendi direito pra que funciona, mas funciona 😁😁)

### API GOOGLE SHEETS
Existe apenas 1 função que utiliza essa API, a update_values(service, spreadsheets_id, range_name, value_input_option, remetente, data, Entrada, Saída). Agora para que serve cada parâmetro?

- service: Necessário para acessar informações da API
- spreadsheets_id: Endereço da nossa planilha
- range_name: Intervalo da planilha que queremos alterar
- value_input_option: Opção de entrada de valores (você pode procurar por outras opções clicando [aqui](https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption?hl=pt-br))
- Os outros são autoexplicativos!

Na planilha:

<img src="https://cdn.discordapp.com/attachments/1105298491078606941/1211776911534067782/image.png?ex=65ef6e31&is=65dcf931&hm=fcb7c2a56d45ecabbad8f0b7312db2ac5d12a59688d8c18f18808936295763f0&" alt="Imagem dos Dados na Planilha">

## NFC

A NFC precisa ser atualizada constantemente de acordo com as alterações no programa. O cartão utilizado está colado na sede com um "P" escrito!

❗TALVEZ TODO O PROGRAMA SEJA ALTERADO, POIS EXISTE A POSSIBILIDADE DA NFC SER FEITA UTILIZANDO UM ARDUINO ❗

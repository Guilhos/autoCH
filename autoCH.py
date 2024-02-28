import os
import pickle
import google.auth
import webbrowser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

### 
# Antes de iniciar o processo de envios de EMAIL, primeiramente verifique se o arquivo 'credentials.json' está na pasta do programa! 
# Verifique se a API está atualizada e se algum dos métodos utilizados está desatualizado!
# Verifique se na caixa de GMAIL não tem algum email indesejável!
# 
# Para esse código funcionar o email precisa estar no formato:
# Hora de entrada: hh:mm
#
# Hora de saída: hh:mm 
#
# É possível alterar este formato mudando o NFC na sede, porém será necessário fazer as mudanças necessárias nos métodos update_values() e read_messages()
# 
# ###


# Identificação da API do GMAIL
SCOPES = ['https://mail.google.com/']
# GMAIL utilizado
our_email = 'cargahoraria@optimusjr.com.br'

# Identificação da API do SHEETS
SCOPES1 = ["https://www.googleapis.com/auth/spreadsheets"]
# O ID do SPREADSHEET.
SPREADSHEET_ID = "1-cOVrhnu8hNbmfhdCZPCJHeuV_mpEDnjn2NtcdlELfQ"
# Células que serão alteradas
RANGE = "A2:D"

### MÉTODOS ###

# Autenticação da API do GMAIL
# Depois da primeira autenticação, será criado um arquivo token.pickle, ele servirá como permissão de acesso
def gmail_authenticate():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# Autenticação da API do SHEETS
def sheet_authenticate():
    creds = None
    if os.path.exists("token1.pickle"):
        with open("token1.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES1)
            creds = flow.run_local_server(port=0)
        with open("token1.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)

# Procurar EMAIL de acordo com a QUERY
def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages
                            
# Pegar dados do EMAIL        
def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    
    # Aqui estamos coletando o nome do REMETENTE e a DATA
    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # REMETENTE
                rm = value.split()
                remetente = rm[0] + rm[1]
                print("From:", value)
            if name.lower() == "to":
                print("To:", value)
            if name.lower() == "subject": # Sinceramente NÃO SEI direito o que essa parte faz, MAS NÃO EXCLUA
                has_subject = True
                folder_name = clean(value)
                folder_counter = 0
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    if folder_name[-1].isdigit() and folder_name[-2] == "_":
                        folder_name = f"{folder_name[:-2]}_{folder_counter}"
                    elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                        folder_name = f"{folder_name[:-3]}_{folder_counter}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                print("Subject:", value)
            if name.lower() == "date":
                # DATA
                print("Date:", value)
                calendario = value.split()
                dia = calendario[1]+"/"+calendario[2]+"/"+calendario[3]
    
    # Aqui se coleta a HORA DE ENTRADA e HORA DE SAÍDA
    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            if part.get("parts"):
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
                    textao = text.split()
                    txtEntrada = textao[3] # ENTRADA
                    txtSaida = textao[7] # SAÍDA
                    
                    # OBSERVAÇÃO: Estou usando estes index, pois de acordo com o formato do EMAIL (mostrado nos comentários
                    # lá de cima), as horas ficam nessas exatas posições! Então não foi necessário fazer um algoritmo de
                    # busca ou algo do tipo
    
    info = [remetente, dia, txtEntrada, txtSaida]
    return info
    
    print("="*50)

# Colocar informações na SPREADSHEET
def update_values(service, spreadsheet_id, range_name, value_input_option, remetente, data, Entrada, Saida):
    try:
        values = [[remetente],[data],[Entrada],[Saida]]
        body = {"majorDimension": "COLUMNS", "values": values}
        result = (service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range= range_name,
            valueInputOption=value_input_option,
            body=body,
        ).execute()
    )
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

# Deletar EMAIL usado
def delete_messages(service, query):
    messages_to_delete = search_messages(service, query)
    return service.users().messages().batchDelete(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_delete]
      }
    ).execute()

#  Limpa o texto em read_message() para criar uma nova pasta
def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

### PROGRAMA ###

def prog():
    lista=[]
    sheet_serv = sheet_authenticate()
    gmail_serv = gmail_authenticate()

    # Aqui se coloca a QUERY
    results = search_messages(gmail_serv, "Hora de entrada")
    print(f"Found {len(results)} results.")
    if len(results) == 0:
        return lista

    # Aqui se vai ler o EMAIL e coloca-lo no SPREADSHEET
    for i in range(len(results)-1, -1, -1):
        msg = results[i]
        info = read_message(gmail_serv, msg)
        lista.append(info)
        update_values(sheet_serv, SPREADSHEET_ID, RANGE, "USER_ENTERED", info[0], info[1], info[2], info[3])
    
    return lista

import os
import pickle
import google.auth
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

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'seuemail@gmail.com'

# If modifying these scopes, delete the file token.json.
SCOPES1 = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "your ID"
SAMPLE_RANGE_NAME = "A1:B2"

def gmail_authenticate():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("file location", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

service = gmail_authenticate()

def sheets_authenticate():
    creds = None
    if os.path.exists("token1.pickle"):
        with open("token1.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("file location", SCOPES1)
            creds = flow.run_local_server(port=0)
        with open("token1.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)

service2 = sheets_authenticate()

def update_values(service2, spreadsheet_id, range_name, value_input_option, _values, deQuem, dia, txtEntrada, txtSaida):
  try:
    values = [[deQuem],[dia], [txtEntrada],[txtSaida] ]
    body = {"majorDimension": "COLUMNS", "values": values}
    result = (
        service2.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range= range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

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

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)
                                    
def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    
    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                dq = value.split()
                deQuem = dq[0] + dq[1]
                print("From:", value)
            if name.lower() == "to":
                print("To:", value)
            if name.lower() == "subject":
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
                print("Date:", value)
                calendario = value.split()
                dia = calendario[1]+"/"+calendario[2]+"/"+calendario[3]
    
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
                    txtEntrada = textao[3]
                    txtSaida = textao[7]
    
    if __name__ == "__main__":
        main()
        update_values(service2,
      SAMPLE_SPREADSHEET_ID,
      SAMPLE_RANGE_NAME,
      "USER_ENTERED",
      [[], []], deQuem,dia, txtEntrada,txtSaida
        )
    
    print("="*50)
    
def delete_messages(service, query):
    messages_to_delete = search_messages(service, query)
    return service.users().messages().batchDelete(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_delete]
      }
    ).execute()
    
results = search_messages(service, "Hora de entrada")
print(f"Found {len(results)} results.")
for msg in results:
    read_message(service, msg)
#delete_messages(service, "Hora de entrada")


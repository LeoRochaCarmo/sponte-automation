#%%

from utils import open_browser, log_in, access_interative, quick_filters, search_student
from utils import access_first_register, class_data, grade_entry, remover_search

driver = open_browser()
username = input('Digite o usuário:')
password = input('Digite a senha:')

log_in(driver, username, password)
access_interative(driver)
quick_filters(driver)
search_student(driver, '3521')
access_first_register(driver)
class_data(driver, 'Presença', '06032025', 'Review 7')
grade_entry(driver, 'Ótimo', 'Ótimo', 'Ótimo', 'On Track', 'Engajado')
remover_search(driver)

#%%

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1Ybq0TT1LRfEjZ55c8RY5-1PachdLFg-rLWpAYuNnJUk"
SAMPLE_RANGE_NAME = "aulas!A1:C2"


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  if os.path.exists("..\\token.json"):
    creds = Credentials.from_authorized_user_file("..\\token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "..\\client_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("..\\token.json", "w") as token:
      token.write(creds.to_json())

  # Agora esta parte está fora do "if", e será executada sempre que houver credenciais válidas.
  service = build("sheets", "v4", credentials=creds)

  try:
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

  except HttpError as err:
    print(f"An error occurred: {err}")

  return values

if __name__ == "__main__":
  main()

#%%

df = main()

print(df)
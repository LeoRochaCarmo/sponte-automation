#%%
import os.path
from time import sleep
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def googlesheets_integration():

  # If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
  SPREADSHEET_ID = "1Ybq0TT1LRfEjZ55c8RY5-1PachdLFg-rLWpAYuNnJUk"
  SHEETS_NAMES = ['Leonardo', 'Mayara']
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

  service = build("sheets", "v4", credentials=creds)

  return service, SHEETS_NAMES, SPREADSHEET_ID

def get_data_from_googlesheets():
  service, sheets_names, spreadsheet_id = googlesheets_integration()
  full_list = []

  try:
    for sheet in sheets_names:
      range_name = f'{sheet}!A:M'
      sheet = service.spreadsheets()
      result = (
          sheet.values()
          .get(spreadsheetId=spreadsheet_id, range=range_name)
          .execute())
      values = result.get("values", [])
      full_list.append(values)

  except HttpError as err:
    print(f"An error occurred: {err}")

  return full_list

# Opening browser
def open_browser():
    browser = webdriver.Chrome()
    browser.get('https://www.sponteweb.com.br/')
    return browser

# Loging in Sponte
def log_in(browser, username, password):
    browser.find_element(By.XPATH, '//*[@id="txtLogin"]').send_keys(username)
    browser.find_element(By.XPATH, '//*[@id="txtSenha"]').send_keys(password)
    browser.find_element(By.XPATH, '//*[@id="btnok"]').click()        
    WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="menuNovo"]/li[2]/a')))

# Accessing interative page
def access_interative(browser):
    browser.find_element(By.XPATH, '//*[@id="menuNovo"]/li[2]/a').click()
    browser.find_element(By.XPATH, '//*[@id="menuNovo"]/li[2]/ul/li[14]/a').click()
    browser.find_element(By.XPATH, '//*[@id="menuNovo"]/li[2]/ul/li[14]/ul/li[1]/a').click()

# Cleaning quick filters
def quick_filters(browser):
    WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_lblFiltrosRapidos"]')))
    (browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdDataRapidoInicial_txtData"]')
            .send_keys(Keys.CONTROL + 'a', Keys.DELETE))
    (browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdDataRapidoFinal_txtData"]')
            .send_keys(Keys.CONTROL + 'a', Keys.DELETE))
    sleep(0.5)
    teacher = browser.find_element(By.XPATH, '//*[@id="select2-ctl00_ContentPlaceHolder1_tab_tabGrid_cmbFuncionarioFR-container"]')
    action = ActionChains(browser)
    action.click(teacher)
    action.send_keys('selecione', Keys.ENTER)
    action.perform()

# Searching student
def search_student(browser, enrollment_number):
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_acAlunoFR_acAlunoFRTextBox"]').send_keys(enrollment_number)
    sleep(1)
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_acAlunoFR_acAlunoFRTextBox"]').send_keys(Keys.TAB)
    sleep(1)
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnFiltroRapido_div"]/div/center/span').click()
    sleep(5)

# Accessing first register
def access_first_register(browser):
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd"]/tbody/tr[2]/td[1]').click()
    sleep(0.5)
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnEditar"]').send_keys(Keys.ENTER)
    sleep(1)
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_lblFiltrosRapidos"]').click()
    sleep(1)
    iframe = browser.find_element(By.XPATH, "//iframe[starts-with(@name, 'hs')]")
    browser.switch_to.frame(iframe)
    sleep(1)

# Setting the class data
def class_data(browser, class_situation, formated_data, lesson):
    if class_situation == 'Presença':
        browser.find_element(By.XPATH, '//*[@id="tab_TabPanel1_rblSituacao"]/tbody/tr/td[1]/span/label').click()
        sleep(1)
    elif class_situation == 'Reposição':
        browser.find_element(By.XPATH, '//*[@id="tab_TabPanel1_rblSituacao"]/tbody/tr/td[1]/span/label').click()
        sleep(1)
        browser.find_element(By.XPATH, '//*[@id="tab_TabPanel1_txtConteudo"]').send_keys(class_situation)
        sleep(1)
    else:
        browser.find_element(By.XPATH, '//*[@id="tab_TabPanel1_txtConteudo"]').send_keys(class_situation)
        browser.find_element(By.XPATH, '//*[@id="tab_TabPanel1_rblSituacao"]/tbody/tr/td[3]/span/label').click()

    licao_iframe = browser.find_element(By.XPATH, '//*[@id="select2-tab_TabPanel1_cmbEstagioLicao-container"]')
    action = ActionChains(browser)
    action.click(licao_iframe)
    action.send_keys(lesson, Keys.ENTER)
    action.perform()
    sleep(1)

    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel1_wcdData_txtData"]').send_keys(Keys.CONTROL + 'a')
    sleep(0.8)
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel1_wcdData_txtData"]').send_keys(formated_data)
    sleep(1)
    

# Entering grades
def grade_entry(browser, speaking, listening, reading, audio, engagement):
    browser.find_element(By.XPATH, '//*[@id="__tab_tab_TabPanel2"]').click()
    sleep(0.5)
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[2]/select').click()
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[2]/select').send_keys(speaking)
    sleep(0.3)
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[3]/select').click()
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[3]/select').send_keys(listening)
    sleep(0.3)
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[4]/select').click()
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[4]/select').send_keys(reading)
    sleep(0.3)
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[6]/select').click()
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[6]/select').send_keys(audio)
    sleep(0.3)
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[7]/select').click()
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_grdNotas"]/tbody/tr[2]/td[7]/select').send_keys(engagement)
    sleep(0.3)
    browser.find_element(By.XPATH, '//*[@id="tab_TabPanel2_btnSalvarNotas_div"]/div/center/span').click()
    sleep(3)
    browser.find_element(By.XPATH, '//*[@id="btnSalvar_div"]/div/center/span').click()
    sleep(3)

def remover_search(browser):
    browser.switch_to.default_content()
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_acAlunoFR_acAlunoFRTextBox"]').send_keys(Keys.CONTROL + 'a')
    sleep(0.3)
    browser.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_tab_tabGrid_acAlunoFR_acAlunoFRTextBox"]').send_keys(Keys.DELETE)
    sleep(0.3)
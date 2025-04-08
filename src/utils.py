#%%

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Open browser
def open_browser():
    browser = webdriver.Chrome()
    browser.get('https://www.sponteweb.com.br/')
    return browser

# Log in Sponte
def log_in(browser, username, password):
    browser.find_element(By.XPATH, '//*[@id="txtLogin"]').send_keys(username)
    browser.find_element(By.XPATH, '//*[@id="txtSenha"]').send_keys(password)
    browser.find_element(By.XPATH, '//*[@id="btnok"]').click()
    WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="menuNovo"]/li[2]/a')))

# Access interative page
def access_interative(browser):
    browser.find_element(By.XPATH, '//*[@id="menuNovo"]/li[2]/a').click()
    browser.find_element(By.XPATH, '//*[@id="menuNovo"]/li[2]/ul/li[14]/a').click()
    browser.find_element(By.XPATH, '//*[@id="menuNovo"]/li[2]/ul/li[14]/ul/li[1]/a').click()

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




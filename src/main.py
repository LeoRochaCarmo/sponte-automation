#%%

from utils import open_browser, log_in, access_interative, quick_filters

#%%

driver = open_browser()
username = input('Digite o usuário:')
password = input('Digite a senha:')
log_in(driver, username, password)

#%%

access_interative(driver)

quick_filters(driver)
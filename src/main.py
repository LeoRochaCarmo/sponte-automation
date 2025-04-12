#%%

from utils import *

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
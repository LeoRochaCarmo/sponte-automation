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

from utils import *

driver = open_browser()
registers = data_frame_creation()
username = input('Digite o usuário:')
password = input('Digite a senha:')


log_in(driver, username, password)
access_interative(driver)
quick_filters(driver)

for index ,row in registers.iterrows():
    search_student(driver, row['numero_matricula'])
    access_first_register(driver)
    formated_data = row['data'].replace('/', '')
    class_data(driver, row['situacao_aula'], formated_data, row['licao'])
    grade_entry(driver, row['fala'], row['audicao'], row['leitura'], row['audio'], row['engajamento'])
    remover_search(driver)
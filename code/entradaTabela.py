from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import sys

arq = pd.read_csv("cidades.csv")
cidades = arq['cidades']
matriz = dict()
matrizAdj = {i:'' for i in cidades}
for i in cidades:
    matrizAdj[i] = {j:0. for j in cidades}

browser = webdriver.Firefox()
browser.get("https://www.google.com.br/maps/dir///@-7.2174611,-39.305056,15z")
time.sleep(1)
search = browser.find_element_by_id('sb_ifc50')
search2 = browser.find_element_by_id('sb_ifc51')
search = search.find_element_by_class_name('tactile-searchbox-input')
search2 = search2.find_element_by_class_name('tactile-searchbox-input')

for i in matrizAdj:
    for j in matrizAdj:
        if(i != j):
            search.send_keys(i + ' CE')
            search2.send_keys(j+ ' CE')
            time.sleep(1)
            button = browser.find_element_by_id('directions-searchbox-1')
            button = button.find_element_by_class_name('searchbox-searchbutton')
            time.sleep(2)
            button.send_keys(Keys.ENTER)

            time.sleep(5)

            distance = browser.find_element_by_class_name('section-directions-trip-numbers')
            distance = distance.find_element_by_class_name('section-directions-trip-secondary-text')
            matrizAdj[i][j] = distance.text

distancia = pd.DataFrame(matrizAdj, columns=['origem', 'destino', 'km'])
distancia.to_csv('distancia.csv')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import random
from fake_useragent import UserAgent

# Gera um User-Agent aleatório
user_agent = UserAgent().random
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=options)

# Função para extrair apenas o título e o link das citações
def extrair_citacoes(citacao_):
    try:
        # Verifica a presença dos elementos na página
        citations = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.gs_ri'))
        )
        for c in citations:
            try:
                # Captura o título e o link do artigo
                c_title = c.find_element(By.CSS_SELECTOR, '.gs_rt a').text
                c_link = c.find_element(By.CSS_SELECTOR, '.gs_rt a').get_attribute('href')
                
                # Adiciona o título e o link ao array citacao_
                citacao_.append([c_title, c_link])
                
            except Exception as e:
                print("Erro ao extrair título e link:", e)
    except Exception as e:
        print("Erro ao localizar citações:", e)

# Função para realizar a busca e extrair as citações
def busca_citacao(titulo):
    driver.get("https://scholar.google.com")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'q')))
    
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(titulo)
    search_box.submit()
    
    # Aumentar tempo de espera para garantir que a página tenha carregado
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.gs_rt a')))
    time.sleep(random.randint(3, 6))
    
    # Clica no link "Citado por" para ver as citações
    try:
        citado_por = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Citado por')))
        citado_por.click()
    except Exception as e:
        print("Erro ao encontrar o botão 'Citado por':", e)
        driver.quit()
        return
    
    # Extrai as citações da primeira página
    citacao_ = []
    extrair_citacoes(citacao_)
    
    # Navega pelas próximas páginas (se houver) para extrair mais citações
    while True:
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.gs_btnPR'))
            )
            next_button.click()
            time.sleep(random.randint(2, 5))
            extrair_citacoes(citacao_)
        except Exception as e:
            print("Erro ou não há mais páginas:", e)
            break
    
    driver.quit()
    
    # Salvando os dados das citações em um arquivo CSV
    with open('all_citations.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])
        writer.writerows(citacao_)

# Chamando a função de busca e extração de citações
busca_citacao("Large Language Models for Software Engineering: A Systematic Literature Review")
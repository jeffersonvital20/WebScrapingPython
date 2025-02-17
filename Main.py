from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def lendo_noticias_uece():
    options = Options()
    options.add_argument("--headless")  # Executa sem abrir o navegador
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.uece.br/uece/noticias/")
    
    news_data = []
    
    while len(news_data) < 50:
        artigos = driver.find_elements(By.CLASS_NAME, "cc-post-title")
        descricao = driver.find_elements(By.CLASS_NAME, "cc-post-excerpt")
        
        for title, desc in zip(artigos, descricao):
            news_data.append({
                "title": title.text,
                "description": desc.text
            })
            if len(news_data) >= 50:
                break
        
        try:
            see_more_button = driver.find_element(By.CSS_SELECTOR,  ".cc-button")
            driver.execute_script("arguments[0].click();", see_more_button)
            time.sleep(2)  # Aguarda carregar novas notícias
        except:
            break
    
    driver.quit()
    
    with open("noticiasUece.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
    
    print("As Noticias estão no Arquivo JSON!")
    
if __name__ == "__main__":
    lendo_noticias_uece()

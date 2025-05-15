from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def extraer_coto_selenium():
    url = "https://www.cotodigital.com.ar/sitios/cdigi/nuevositio"
    productos = []

    # Configuramos opciones para que no abra ventana (headless)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # Path al chromedriver, debe estar instalado y en PATH o poner ruta absoluta
    service = Service('chromedriver') 

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(5)  # esperamos que cargue la página

    # Buscamos productos - acá hay que inspeccionar bien para ajustar el selector
    items = driver.find_elements(By.CSS_SELECTOR, "div.product-card")

    for item in items:
        try:
            nombre = item.find_element(By.CSS_SELECTOR, "h3.product-card__title").text
        except:
            nombre = "N/D"
        try:
            precio = item.find_element(By.CSS_SELECTOR, "span.price__best").text
        except:
            precio = "N/D"
        try:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            link = "N/D"

        productos.append({
            'Supermercado': 'COTO',
            'Producto': nombre,
            'Precio': precio,
            'URL': link
        })

    driver.quit()
    return productos

def main():
    print("Iniciando extracción con Selenium...")
    productos = extraer_coto_selenium()

    df = pd.DataFrame(productos)
    df.to_csv("precios_coto_selenium.csv", index=False)
    print("Archivo generado: precios_coto_selenium.csv")

if __name__ == "__main__":
    main()

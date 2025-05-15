import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import uniform

# Headers para evitar bloqueos por User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

def extraer_dia():
    url_base = "https://www.supermercadosdia.com.ar"
    url_categoria = f"{url_base}/bebidas"
    productos = []

    try:
        response = requests.get(url_categoria, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select(".product-card")
        for item in items:
            nombre = item.select_one(".product-card__title")
            precio = item.select_one(".price__best")
            link = item.select_one("a")

            productos.append({
                'Supermercado': 'DIA',
                'Producto': nombre.text.strip() if nombre else 'N/D',
                'Precio': precio.text.strip() if precio else 'N/D',
                'URL': url_base + link['href'] if link else 'N/D'
            })

    except Exception as e:
        print("Error en DIA:", e)

    return productos

def extraer_coto():
    url_categoria = "https://www.cotodigital3.com.ar/sitios/cdigi/browse/Bebidas/_/N-1z141sf"
    productos = []

    try:
        response = requests.get(url_categoria, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select(".product-item")
        for item in items:
            nombre = item.select_one(".descrip_full")
            precio = item.select_one(".atg_store_newPrice")
            link = item.select_one("a")

            productos.append({
                'Supermercado': 'COTO',
                'Producto': nombre.text.strip() if nombre else 'N/D',
                'Precio': precio.text.strip() if precio else 'N/D',
                'URL': "https://www.cotodigital3.com.ar" + link['href'] if link else 'N/D'
            })

    except Exception as e:
        print("Error en COTO:", e)

    return productos

def extraer_carrefour():
    url_categoria = "https://www.carrefour.com.ar/bebidas"
    productos = []

    try:
        response = requests.get(url_categoria, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select(".vtex-product-summary-2-x-container")
        for item in items:
            nombre = item.select_one(".vtex-product-summary-2-x-productBrand")
            precio = item.select_one(".vtex-product-price-1-x-sellingPrice")
            link = item.select_one("a")

            productos.append({
                'Supermercado': 'Carrefour',
                'Producto': nombre.text.strip() if nombre else 'N/D',
                'Precio': precio.text.strip() if precio else 'N/D',
                'URL': "https://www.carrefour.com.ar" + link['href'] if link else 'N/D'
            })

    except Exception as e:
        print("Error en Carrefour:", e)

    return productos

def main():
    print("Iniciando extracción de precios...")

    todos_productos = []
    todos_productos.extend(extraer_dia())
    sleep(uniform(1, 3))
    todos_productos.extend(extraer_coto())
    sleep(uniform(1, 3))
    todos_productos.extend(extraer_carrefour())

    df = pd.DataFrame(todos_productos)
    df.to_csv("precios_supermercados.csv", index=False)

    print("Extracción finalizada. Archivo generado: precios_supermercados.csv")

if __name__ == '__main__':
    main()

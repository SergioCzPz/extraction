import requests
import math
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from models.product import Product
from pathlib import Path


def get_info_products(path_file:str) -> List[Product]:
    products = []

    try:
        df = pd.read_excel(path_file, header=0)
    except:
        print("Error: File not found")
        return []
    
    if 'TIPO' in df.columns:
        df['TIPO'] = df['TIPO'].ffill()

    for index, row in df.iterrows():
        raw_sku = row.get('CÓDIGO')
        raw_title = row.get('DESCRIPCION')
        raw_price = row.get('PRECIO')
        raw_type = row.get('TIPO')

        if pd.isna(raw_sku):
            continue

        price = 0.0
        if pd.notna(raw_price):
            try:
                if isinstance(raw_price, str):
                    clean_price = raw_price.replace('$', '').replace(',','').strip()
                    price = float(clean_price)
                else:
                    price = float(raw_price)
            except ValueError:
                price = 0.0

        product = Product(
            sku=str(raw_sku).strip(),
            title=str(raw_title).strip() if pd.notna(raw_title) else "",
            price=price,
            type=str(raw_type).strip() if pd.notna(raw_type) else ""
        )

        products.append(product)
    
    return products

if __name__ == "__main__":

    file_paths = ["LISTA_PRECIOS_FEBRERO_ARTLITE_2025_NO_IMAGES.xlsx", "LISTA_PRECIOS_MAYO_WINLED_2025_NO_IMAGES.xlsx", "PLACAS_PRECIOS_FEBRERO_ARTLITE_2025_NO_IMAGES.xlsx"]

    for path in file_paths:
        file_path = f"./files/{path}"
        products = get_info_products(file_path)

        print(f"There are {len(products)} in the excel file")

        for product in products:
            print(product)

        products = []
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# }

# res = requests.get("https://www.innlite.com/product/ado-001/", headers=headers)
# soup = BeautifulSoup(res.content, "html.parser")

# title = soup.find("h1", class_="product_title entry-title")
# sku = soup.find("span", class_="sku")
# image_url = soup.find(
#     "img", class_="attachment-shop_single size-shop_single wp-post-image"
# )

# div_text_product = soup.find(
#     "div", class_="woocommerce-product-details__short-description"
# )

# brand = soup.find("")
# span_categories = soup.find("span", class_="posted_in")

# print(f"image url: {image_url.get('src')}")
# print(f"title: {title.text.strip()}")
# print(f"sku: {sku.text.strip()}")

# categories = span_categories.find_all("a")

# print("Categories")
# for categorie in categories:
#     print(f"    -   {categorie.text.strip()}")

# print("Text product")
# text_product = div_text_product.find_all("p")
# for text in text_product:
#     print(f"    -   {text.text.strip()}")

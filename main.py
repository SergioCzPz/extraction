import requests
import json
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from models.product import Product
from models.excel_product import ExcelProduct
from models.scrapt_product import ScraptProduct


def get_info_products_from_excel(path_file: str) -> List[ExcelProduct]:
    products = []

    try:
        df = pd.read_excel(path_file, header=0)
    except:
        print("Error: File not found")
        return []

    if "TIPO" in df.columns:
        df["TIPO"] = df["TIPO"].ffill()

    for index, row in df.iterrows():
        raw_sku = row.get("CÓDIGO")
        raw_title = row.get("DESCRIPCION")
        raw_price = row.get("PRECIO")
        raw_type = row.get("TIPO")

        if pd.isna(raw_sku):
            continue

        price = 0.0
        if pd.notna(raw_price):
            try:
                if isinstance(raw_price, str):
                    clean_price = raw_price.replace("$", "").replace(",", "").strip()
                    price = float(clean_price)
                else:
                    price = float(raw_price)
            except ValueError:
                price = 0.0

        product = ExcelProduct(
            sku=str(raw_sku).strip(),
            title=str(raw_title).strip() if pd.notna(raw_title) else "",
            price=price,
            type=str(raw_type).strip().capitalize() if pd.notna(raw_type) else "",
        )

        products.append(product)

    return products


def scrap_product_from_website(sku: str) -> ScraptProduct:
    sku = sku.lower()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    res = requests.get(f"https://www.innlite.com/product/{sku}/", headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    title_el = soup.find("h1", class_="product_title entry-title")
    sku_el = soup.find("span", class_="sku")
    img_el = soup.find(
        "img", class_="attachment-shop_single size-shop_single wp-post-image"
    )
    text_product_el = soup.find(
        "div", class_="woocommerce-product-details__short-description"
    )
    brand_label = soup.find("strong", string=lambda text: text and "MARCA" in text)
    brand = "Unknown"

    if brand_label:
        next_text = brand_label.next_sibling

        if next_text:
            brand = next_text.strip().title()

    print(f"sku.lower(): {sku.lower()}")
    print(f"title_el.text.strip().lower(): {title_el.text.strip().lower()}")
    print(f"sku_el.text.strip().lower(): {sku_el.text.strip().lower()}")

    if (
        sku.lower() not in title_el.text.strip().lower()
        and sku.lower() not in sku_el.text.strip().lower()
    ):
        # register to fail.json
        print(f"Problem working with the product {sku}")
        return

    img_src = img_el.get("src")
    text_product = text_product_el.find_all("p")
    info_text = []

    for text_el in text_product:
        text = text_el.text.strip()
        info_text.append(text)

    product_scrapted = ScraptProduct(
        brand=brand, image_src=img_src, info_text=info_text
    )

    print(product_scrapted)

    return product_scrapted


def convert_product_to_dictionary(
    scrapt_product: ScraptProduct, excel_product: ExcelProduct
) -> Product:
    product = Product(
        sku=excel_product.sku,
        title=excel_product.title,
        price=excel_product.price,
        type=excel_product.type,
        brand=scrapt_product.brand,
        image_src=scrapt_product.image_src,
        info_text=scrapt_product.info_text,
    )
    return product.to_dict()


def save_product(products: List[dict], file_path: str = "./products.json") -> None:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        print(
            f"Products Successfully Saved {len(products)} Products saved on {file_path}"
        )
    except Exception as e:
        print(f"Error on saving: {e}")


if __name__ == "__main__":

    # file_paths = [
    #     "LISTA_PRECIOS_FEBRERO_ARTLITE_2025_NO_IMAGES.xlsx",
    #     "LISTA_PRECIOS_MAYO_WINLED_2025_NO_IMAGES.xlsx",
    #     "PLACAS_PRECIOS_FEBRERO_ARTLITE_2025_NO_IMAGES.xlsx",
    # ]

    file_paths = [
        "PRUEBA.xlsx",
    ]

    products = []

    for path in file_paths:
        file_path = f"./files/{path}"
        products_from_excel = get_info_products_from_excel(file_path)

        print(f"There are {len(products_from_excel)} products in the excel file")
        print(f"products_from_excel: {products_from_excel}")

        for product_from_excel in products_from_excel:
            print(f"product_from_excel {product_from_excel}")
            product_scrapted = scrap_product_from_website(product_from_excel.sku)

            dictionary_product = convert_product_to_dictionary(
                excel_product=product_from_excel, scrapt_product=product_scrapted
            )

            products.append(dictionary_product)

    save_product(products=products, file_path="./products.json")

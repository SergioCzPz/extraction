from typing import List


class Product:
    def __init__(
        self,
        sku: str,
        title: str,
        price: float,
        type: str,
        brand: str,
        image_src: str,
        info_text: List[str],
    ):
        self.sku = sku
        self.title = title
        self.price = price
        self.type = type
        self.brand = brand
        self.image_src = image_src
        self.info_text = info_text

    def to_dict(self):
        return {
            "sku": self.sku,
            "title": self.title,
            "price": self.price,
            "type": self.type,
            "brand": self.brand,
            "image_src": self.image_src,
            "info_text": self.info_text,
        }

    def __repr__(self):
        return f"Product(sku='{self.sku}', type='{self.type}', price={self.price})"

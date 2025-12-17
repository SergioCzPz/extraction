from typing import List


class ScraptProduct:
    def __init__(self, brand: str, image_src: str, info_text: List[str]):
        self.brand = brand
        self.image_src = image_src
        self.info_text = info_text

    def __repr__(self):
        return f"ScraptProduct(brand='{self.brand}', image_src='{self.image_src}', info_text={self.info_text})"

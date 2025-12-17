class Product:
    def __init__(
        self,
        sku: str,
        price: float,
        type: str,
        text=[],
        title: str = "",
        image_src: str = "",
    ):
        self.sku = sku
        self.title = title
        self.price = price
        self.image_src = image_src
        self.text = text
        self.type = type

    def __repr__(self):
        return f"Product(sku='{self.sku}', type='{self.type}', price={self.price})"
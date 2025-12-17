class ExcelProduct:
    def __init__(self, sku: str, title: str, price: float, type: str):
        self.sku = sku
        self.title = title
        self.price = price
        self.type = type

    def __repr__(self):
        return f"ExcelProduct(sku='{self.sku}', title={self.title}, type='{self.type}', price={self.price})"

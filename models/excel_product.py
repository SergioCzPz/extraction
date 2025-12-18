class ExcelProduct:
    def __init__(self, sku: str, title: str, price: float, type: str):
        self.sku = sku
        self.title = title
        self.price = self.total_price(price)
        self.type = type

    def total_price(self, price: float) -> float:
        first_price = price + (price * 0.01)
        final_price = first_price + (first_price * 0.16)
        return final_price

    def __repr__(self):
        return f"ExcelProduct(sku='{self.sku}', title={self.title}, type='{self.type}', price={self.price})"

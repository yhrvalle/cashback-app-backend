class CashbackError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class ValorInvalidoError(CashbackError):
    def __init__(self):
        super().__init__("O valor da compra deve ser maior que zero.", 422)

class DescontoInvalidoError(CashbackError):
    def __init__(self):
        super().__init__("O valor de desconto não pode ser maior que 100 ou negativo.", 422)

class ClienteNaoEncontradoError(CashbackError):
    def __init__(self):
        super().__init__("Cliente não localizado na base de dados.", 404)
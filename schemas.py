from pydantic import BaseModel, Field
from decimal import Decimal

class CashbackRequest(BaseModel):
    valor: Decimal = Field(gt=0, decimal_places=2, description="Valor da compra deve ser maior que zero")
    desconto: Decimal = Field(ge=0, le=100, decimal_places=2, description="Desconto deve ser entre 0 e 100")
    cliente_vip: bool = False
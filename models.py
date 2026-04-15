from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Numeric
from datetime import datetime, timezone
from database import Base

class ConsultaCashback(Base):
    __tablename__ = "consultas_cashback"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    ip_usuario = Column(String, nullable=False)  
    cliente_vip = Column(Boolean, default=False, nullable=False)
    valor_compra = Column(Numeric(10, 2), nullable=False)
    valor_descontado = Column(Numeric(10, 2), nullable=False)
    desconto = Column(Float, nullable=False)
    valor_cashback = Column(Numeric(10, 2), nullable=False)
    data_criacao = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
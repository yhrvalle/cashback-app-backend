from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from decimal import Decimal
from schemas import CashbackRequest

models.Base.metadata.create_all(bind=engine)
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    erros = exc.errors()
    msg = erros[0].get("msg")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "erro",
            "mensagem": f"Erro de validação: {msg}"
        },
    )

def calculo_cashback(valor_compra : Decimal, desconto_porcentual: Decimal, cliente_vip : bool) -> dict:
    CASHBACK_BASE = Decimal("0.05") 
    VALOR_MIN_DOBRO = Decimal("500.0")
    

    valor_descontado = valor_compra * (1 - (desconto_porcentual / Decimal("100")))
    cashback = valor_descontado * CASHBACK_BASE
    
    if cliente_vip:
        cashback += cashback * Decimal("0.10")

    if valor_descontado >= VALOR_MIN_DOBRO:
        cashback *= Decimal("2")
    
    return cashback

@app.post("/calcular")
async def calcular(dados: CashbackRequest, request: Request, db: Session = Depends(get_db)):

    cashback_resultado = calculo_cashback(dados.valor, dados.desconto, dados.cliente_vip)

    salvar_consulta = models.ConsultaCashback(
        ip_usuario=request.client.host,
        cliente_vip=dados.cliente_vip,
        valor_compra=dados.valor,
        valor_descontado=dados.valor * (1 - (dados.desconto / 100)),
        desconto=dados.desconto,
        valor_cashback=cashback_resultado
    )
    db.add(salvar_consulta)
    db.commit()
    db.refresh(salvar_consulta)

    return {
        "status": "sucesso",
        "cashback": cashback_resultado,
    }

@app.get("/historico")
async def historico(request: Request, db: Session = Depends(get_db)):
    ip_cliente = request.client.host
    
    consultas = db.query(models.ConsultaCashback).filter(
        models.ConsultaCashback.ip_usuario == ip_cliente
    ).order_by(models.ConsultaCashback.data_criacao.desc()).all()
    
    return consultas 

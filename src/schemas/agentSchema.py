from pydantic import BaseModel, Field, validator
from typing import Optional


class CreateAgentSchema(BaseModel):
    """Schema de validação para criação de agente"""
    name: str = Field(..., min_length=1, description="Nome do agente")
    initialBalance: float = Field(default=100, ge=100, description="Saldo inicial mínimo 100")
    symbol: str = Field(default="ETHUSDT", description="Símbolo da moeda")

    @validator('symbol')
    def validate_symbol(cls, v):
        if not v or len(v) < 2:
            raise ValueError('Símbolo deve ter pelo menos 2 caracteres')
        return v.upper()


class SimulateTradeSchema(BaseModel):
    """Schema de validação para simulação de trades"""
    agentId: str = Field(..., min_length=1, description="ID do agente")
    numTrades: int = Field(default=1, ge=1, description="Número de trades a simular")
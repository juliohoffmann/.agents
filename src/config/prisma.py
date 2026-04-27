import os
from typing import Optional
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    """Configuração de banco de dados"""
    mongo_url: str = "mongodb://admin:123456@db_mongo:27017/db_mongo?authSource=admin"
    database_name: str = "verdent_db"


# Simulação de cliente MongoDB (em memória para compatibilidade)
class MockMongoClient:
    def __init__(self, url: str):
        self.url = url
        self._data = {}
    
    def connect(self):
        print(f"Conectado ao MongoDB: {self.url}")
        return self
    
    def __getitem__(self, key):
        return self._data.get(key)
    
    def get_database(self, name: str):
        return self._data.setdefault(name, {})


def get_prisma_client():
    """Retorna cliente de banco de dados simulado"""
    mongo_url = os.getenv("MONGO_URL", DatabaseConfig().mongo_url)
    return MockMongoClient(mongo_url)


# Instância global
prisma = get_prisma_client()


async def connect_to_database():
    """Conecta ao banco de dados"""
    await prisma.connect()
    print("Conectado ao banco de dados")
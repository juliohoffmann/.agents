import jwt
from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from functools import wraps


class AuthMiddleware:
    """Middleware de autenticação JWT"""
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
    
    def verify_token(self, token: str) -> dict:
        """Verifica e decodifica token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    
    def get_current_user(self, request: Request) -> Optional[dict]:
        """Extrai usuário do token no header Authorization"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        
        return self.verify_token(parts[1])


def auth_middleware(secret_key: str) -> AuthMiddleware:
    """Factory para criar middleware de autenticação"""
    return AuthMiddleware(secret_key)


def require_auth(secret_key: str):
    """Decorator para rotas que requerem autenticação"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extrai request do primeiro argumento
            request = args[0] if args else kwargs.get('request')
            if not request:
                raise HTTPException(status_code=500, detail="Request não encontrado")
            
            auth = AuthMiddleware(secret_key)
            user = auth.get_current_user(request)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token não fornecido ou inválido"
                )
            
            # Adiciona usuário ao request
            request.user = user
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_admin(secret_key: str):
    """Decorator para rotas que requerem privilégios de admin"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[0] if args else kwargs.get('request')
            if not request:
                raise HTTPException(status_code=500, detail="Request não encontrado")
            
            if not getattr(request, 'user', None) or not request.user.get('admin', False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso negado. Privilégios de admin necessários."
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
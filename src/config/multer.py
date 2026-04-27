import os
from datetime import datetime
from typing import Optional


class UploadConfig:
    """Configuração de upload de arquivos"""
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: set = {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.txt', '.csv'}


def get_file_path(filename: str) -> str:
    """Gera caminho único para arquivo"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{UploadConfig.upload_dir}/{timestamp}_{filename}"


def validate_file(filename: str) -> bool:
    """Valida extensão do arquivo"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in UploadConfig.allowed_extensions
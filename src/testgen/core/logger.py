from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from testgen.core.config import OUTPUT_PATH

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Đảm bảo thư mục logs tồn tại
        log_dir = OUTPUT_PATH / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "app.log"
        
        # Formatter chuẩn
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Ghi log ra file với cơ chế xoay vòng (max 5MB/file, giữ 3 file)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler (để xem log trực tiếp trên terminal nếu chạy bằng python)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger


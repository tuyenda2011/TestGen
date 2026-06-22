from __future__ import annotations

import json
import re
import json_repair
from typing import Any
from pathlib import Path
from testgen.core.logger import get_logger

logger = get_logger(__name__)

def normalize_text(value: object | None) -> str:
    if value is None:
        return ""
    return str(value).strip()

def repair_common_mojibake(text: str) -> str:
    if not isinstance(text, str):
        return text
    replacements = {
        "Ã¡": "á", "Ã ": "à", "áº£": "ả", "Ã£": "ã", "áº¡": "ạ",
        "Ã¢": "â", "áº¥": "ấ", "áº§": "ầ", "áº©": "ẩ", "áº«": "ẫ", "áº­": "ậ",
        "Äƒ": "ă", "áº¯": "ắ", "áº±": "ằ", "áº³": "ẳ", "áºµ": "ẵ", "áº·": "ặ",
        "Ã©": "é", "Ã¨": "è", "áº»": "ẻ", "áº½": "ẽ", "áº¹": "ẹ",
        "Ãª": "ê", "áº¿": "ế", "á» ": "ề", "á»ƒ": "ể", "á»…": "ễ", "á»‡": "ệ",
        "Ã­": "í", "Ã¬": "ì", "á»‰": "ỉ", "Ä©": "ĩ", "á»‹": "ị",
        "Ã³": "ó", "Ã²": "ò", "á» ": "ỏ", "Ãµ": "õ", "á» ": "ọ",
        "Ã´": "ô", "á»‘": "ố", "á»“": "ồ", "á»•": "ổ", "á»—": "ỗ", "á»™": "ộ",
        "Æ¡": "ơ", "á»›": "ớ", "á» ": "ờ", "á»Ÿ": "ở", "á»¡": "ỡ", "á»£": "ợ",
        "Ãº": "ú", "Ã¹": "ù", "á»§": "ủ", "Å©": "ũ", "á»¥": "ụ",
        "Æ°": "ư", "á»©": "ứ", "á»«": "ừ", "á»­": "ử", "á»¯": "ữ", "á»±": "ự",
        "Ã½": "ý", "á»³": "ỳ", "á»·": "ỷ", "á»¹": "ỹ", "á»µ": "ỵ",
        "Ä‘": "đ",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def fix_json_trailing_commas(json_str: str) -> str:
    """Xóa các dấu phẩy dư thừa ở cuối object/array do LLM sinh ra."""
    # Bỏ dấu phẩy thừa trước ngoặc đóng } hoặc ]
    json_str = re.sub(r",\s*([\]}])", r"\1", json_str)
    return json_str

def extract_json_payload(payload: str, silent: bool = False) -> Any:
    text = normalize_text(payload)
    if not text:
        return None
        
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        
    obj_start = text.find("{")
    obj_end = text.rfind("}")
    arr_start = text.find("[")
    arr_end = text.rfind("]")
    
    start = -1
    end = -1
    
    if obj_start != -1 and obj_end != -1:
        start = obj_start
        end = obj_end
        
    if arr_start != -1 and arr_end != -1:
        if start == -1 or (arr_start < start and arr_end > end):
            start = arr_start
            end = arr_end
            
    # Thử parse toàn bộ đoạn block
    candidate = text
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        
    # Cố gắng vá lỗi dấu phẩy
    candidate = fix_json_trailing_commas(candidate)
    
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        # Fallback thử parse thô nếu candidate đã bị cắt lỡ
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Fallback cuối cùng: dùng json_repair
            try:
                repaired = json_repair.repair_json(candidate, return_objects=True)
                if repaired is not None:
                    if not silent:
                        logger.info(f"Đã tự động sửa lỗi JSON bằng json_repair.")
                    return repaired
            except Exception as repair_err:
                pass
            
            if not silent:
                logger.warning(f"Lỗi parse JSON: {e}. Payload: {candidate[:100]}...")
            return None

from pydantic import BaseModel, ValidationError

def extract_and_validate_json_payload(payload: str, schema: type[BaseModel], silent: bool = False) -> BaseModel | None:
    data = extract_json_payload(payload, silent=silent)
    if data is None:
        return None
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        if not silent:
            logger.warning(f"Lỗi validate schema Pydantic: {e}")
        return None

def pretty_json_or_raw(text: str) -> str:
    payload = extract_json_payload(text, silent=True)
    if payload is not None:
        return json.dumps(payload, indent=2, ensure_ascii=False)
    return normalize_text(text)

def get_file_mime_from_extension(path: Path) -> str:
    if path.suffix == ".xlsx":
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if path.suffix == ".pdf":
        return "application/pdf"
    if path.suffix == ".md":
        return "text/markdown"
    return "text/plain"

def get_code_language(framework: str) -> str:
    mapping = {
        "pytest": "python",
        "Selenium": "python",
        "Playwright": "python",
        "JUnit": "java",
        "Jest": "javascript",
        "Postman script": "javascript",
    }
    return mapping.get(framework, "text")

"""
数值解析模块 - 处理数字的分割与格式化
"""
from decimal import Decimal
from typing import Tuple
from .validation import validate

def split_number(input_str: str) -> Tuple[int, int]:
    """
    将输入的数字字符串分割为整数部分和小数部分
    
    Args:
        input_str: 输入的数字字符串
    
    Returns:
        Tuple[int, int]: (整数部分, 小数部分*100)
        例如：
        "123.45" -> (123, 45)
        "123.4" -> (123, 40)
        "123" -> (123, 0)
    """
    # 首先验证输入
    validate(input_str)
    
    # 转换为Decimal以保证精确计算
    number = Decimal(input_str)
    
    # 分离整数和小数部分
    integer_part = int(number)
    decimal_part = int((number % 1) * 100)  # 保留两位小数
    
    return integer_part, decimal_part

def normalize_number(input_str: str) -> str:
    """
    规范化数字字符串，清理多余的零
    
    Args:
        input_str: 输入的数字字符串
    
    Returns:
        str: 规范化后的数字字符串
        例如：
        "012.300" -> "12.3"
        "1.23000" -> "1.23"
        "00123" -> "123"
    """
    # 首先验证输入
    validate(input_str)
    
    # 转换为Decimal进行处理
    number = Decimal(input_str)
    
    # 移除末尾的零
    normalized = str(number.normalize())
    
    # 如果是整数，确保不显示小数点
    if '.' in normalized and normalized.endswith('0'):
        normalized = normalized.rstrip('0').rstrip('.')
        
    return normalized 
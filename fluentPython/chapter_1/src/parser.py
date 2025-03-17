"""
数值解析模块 - 处理数字的分割与格式化
"""
from decimal import Decimal, ROUND_DOWN
from typing import Tuple
from .validation import validate

def split_number(input_str: str) -> Tuple[int, int]:
    """
    处理输入的数字字符串，返回整数部分和小数部分
    
    Args:
        input_str: 输入的数字字符串
    
    Returns:
        Tuple[int, int]: (整数部分, 小数部分*100)
        例如：
        "123.45" -> (123, 45)
        "123.4" -> (123, 40)
        "123" -> (123, 0)
        "123.456" -> (123, 45)  # 自动截断到两位小数
        "012.300" -> (12, 30)   # 自动清理多余的零
    """
    # 首先验证输入
    validate(input_str)
    
    # 转换为Decimal并截断到两位小数
    number = Decimal(input_str)
    number = number.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    
    # 规范化处理（移除不必要的零和小数点）
    number_str = str(number.normalize())
    if '.' in number_str and number_str.endswith('0'):
        number_str = number_str.rstrip('0').rstrip('.')
        number = Decimal(number_str)
    
    # 分离整数和小数部分
    integer_part = int(number)
    decimal_part = int((number % 1) * 100)
    
    return integer_part, decimal_part
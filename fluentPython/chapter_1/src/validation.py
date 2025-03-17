"""
输入验证模块 - 处理数字输入的合法性检查
"""
import re
from decimal import Decimal, ROUND_DOWN
from typing import Union

class ConversionError(Exception):
    """转换错误基类"""
    def __init__(self, code: str, message: str, original: str):
        self.code = code
        self.message = message
        self.original = original
        super().__init__(message)

class InvalidFormatError(ConversionError):
    """格式错误"""
    pass

class NegativeNumberError(ConversionError):
    """负数错误"""
    pass

class OverflowError(ConversionError):
    """数值溢出错误"""
    pass

def validate(number: Union[str, float, int]) -> bool:
    """
    验证输入数字的合法性
    
    Args:
        number: 输入的数字（字符串或数字类型）
    
    Returns:
        bool: 是否合法
    
    Raises:
        InvalidFormatError: 格式错误
        OverflowError: 数值超出范围
        NegativeNumberError: 负数错误
    """
    # 转换为字符串进行处理
    number_str = str(number)
    
    # 检查负数
    if number_str.startswith('-'):
        raise NegativeNumberError(
            'NEGATIVE_NUMBER',
            '不支持负数转换',
            number_str
        )
    
    # 格式检查 - 修改正则表达式以允许任意位数的小数
    pattern = r'^\d+(\.\d+)?$'
    if not re.match(pattern, number_str):
        raise InvalidFormatError(
            'INVALID_FORMAT',
            '数字格式错误，只能包含数字和小数点，小数位数超过两位将自动截断',
            number_str
        )
    
    # 范围检查
    value = Decimal(number_str)
    # 先截断到两位小数
    value = value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    if value > Decimal('999999999999.99'):
        raise OverflowError(
            'NUMBER_TOO_LARGE',
            '数字超出范围，整数部分不能超过999999999999（千亿），小数部分会自动截断到两位',
            number_str
        )
    
    return True 
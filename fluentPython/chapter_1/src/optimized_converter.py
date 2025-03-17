"""
优化版转换器 - 包含缓存和预计算功能
"""
from functools import lru_cache
from typing import Dict, List, Tuple
from .converter import CHINESE_DIGITS, UNITS, LARGE_UNITS
from .parser import split_number, normalize_number

# 预计算常用数字的中文表示（0-9999）
PRECOMPUTED_NUMBERS: Dict[int, str] = {}

# 预计算单位组合
UNIT_COMBINATIONS: List[str] = []

def initialize_cache():
    """初始化预计算缓存"""
    # 预计算0-9999的中文表示
    for i in range(10000):
        result = []
        num_str = str(i).zfill(4)
        last_is_zero = True
        
        for j, digit in enumerate(num_str):
            digit_int = int(digit)
            
            if digit_int == 0:
                if not last_is_zero and j < len(num_str) - 1 and any(int(d) > 0 for d in num_str[j+1:]):
                    result.append(CHINESE_DIGITS[0])
                last_is_zero = True
                continue
                
            if digit_int > 0:
                result.append(CHINESE_DIGITS[digit_int])
                result.append(UNITS[4 - j - 1])
                last_is_zero = False
        
        PRECOMPUTED_NUMBERS[i] = "".join(result)
    
    # 预计算单位组合
    for unit in LARGE_UNITS:
        UNIT_COMBINATIONS.append(unit)
        for base_unit in UNITS:
            if base_unit:
                UNIT_COMBINATIONS.append(base_unit + unit)

@lru_cache(maxsize=10000)
def _convert_4digits_cached(num: int) -> str:
    """带缓存的4位数转换"""
    return PRECOMPUTED_NUMBERS.get(num, "")

@lru_cache(maxsize=10000)
def convert_integer_cached(num: int) -> str:
    """带缓存的整数转换"""
    if num == 0:
        return CHINESE_DIGITS[0]
    
    # 按4位分组处理
    groups: List[int] = []
    while num > 0:
        groups.append(num % 10000)
        num //= 10000
    
    result = []
    for i, group in enumerate(groups):
        if group == 0:
            continue
        
        # 使用预计算的结果
        group_chinese = _convert_4digits_cached(group)
        if group_chinese:
            result.insert(0, group_chinese + LARGE_UNITS[i])
    
    return "".join(result)

@lru_cache(maxsize=100)
def convert_decimal_cached(jiao: int, fen: int) -> str:
    """带缓存的小数部分转换"""
    result = []
    
    if jiao == 0 and fen == 0:
        return "整"
    
    if jiao > 0:
        result.extend([CHINESE_DIGITS[jiao], "角"])
    elif fen > 0:
        result.append(CHINESE_DIGITS[0])
    
    if fen > 0:
        result.extend([CHINESE_DIGITS[fen], "分"])
    
    return "".join(result)

def convert_optimized(number: str) -> str:
    """优化版的数字转换函数"""
    # 规范化处理
    number = normalize_number(number)
    
    # 分离整数和小数部分
    integer_part, decimal_part = split_number(number)
    
    # 转换整数部分
    integer_chinese = convert_integer_cached(integer_part)
    
    # 转换小数部分
    jiao = decimal_part // 10
    fen = decimal_part % 10
    decimal_chinese = convert_decimal_cached(jiao, fen)
    
    # 组合结果
    result = integer_chinese + "元"
    if decimal_chinese != "整":
        result += decimal_chinese
    else:
        result += "整"
    
    return result

# 初始化缓存
initialize_cache() 
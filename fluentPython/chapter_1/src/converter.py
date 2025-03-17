"""
转换器核心模块 - 实现数字到中文大写的转换
"""
from typing import List
from .parser import split_number

# 数字到中文大写的映射
CHINESE_DIGITS = {
    0: "零", 1: "壹", 2: "贰", 3: "叁", 4: "肆",
    5: "伍", 6: "陆", 7: "柒", 8: "捌", 9: "玖"
}

# 位值单位
UNITS = ["", "拾", "佰", "仟"]

# 大单位
LARGE_UNITS = ["", "万", "亿"]

def _convert_4digits(num: int) -> str:
    """
    转换4位以内的数字
    
    Args:
        num: 0-9999之间的整数
    
    Returns:
        str: 转换后的中文大写
    """
    if num == 0:
        return ""
    
    result = []
    num_str = str(num)
    num_len = len(num_str)
    
    # 补齐4位
    num_str = num_str.zfill(4)
    
    # 处理每一位
    last_is_zero = True  # 上一位是否为零
    for i, digit in enumerate(num_str):
        digit_int = int(digit)
        
        # 当前数字是0的情况
        if digit_int == 0:
            if not last_is_zero and i < len(num_str) - 1 and any(int(d) > 0 for d in num_str[i+1:]):
                result.append(CHINESE_DIGITS[0])
            last_is_zero = True
            continue
            
        # 当前数字非0
        if digit_int > 0:
            result.append(CHINESE_DIGITS[digit_int])
            result.append(UNITS[4 - i - 1])
            last_is_zero = False
    
    return "".join(result)

def convert_integer(num: int) -> str:
    """
    转换整数部分
    
    Args:
        num: 待转换的整数
    
    Returns:
        str: 转换后的中文大写
    """
    if num == 0:
        return CHINESE_DIGITS[0]
    
    result = []
    num_str = str(num)
    num_len = len(num_str)
    
    # 按4位分组处理
    groups = []
    while num > 0:
        groups.append(num % 10000)
        num //= 10000
    
    # 处理每个分组
    for i, group in enumerate(groups):
        if group == 0:
            # 处理全零的组
            if i < len(groups) - 1 and groups[i+1] > 0:
                result.insert(0, CHINESE_DIGITS[0])
            continue
        
        # 转换当前组
        group_chinese = _convert_4digits(group)
        if group_chinese:
            result.insert(0, group_chinese + LARGE_UNITS[i])
    
    return "".join(result)

def convert_decimal(jiao: int, fen: int) -> str:
    """
    转换小数部分
    
    Args:
        jiao: 角的数值
        fen: 分的数值
    
    Returns:
        str: 转换后的中文大写
    """
    if jiao == 0 and fen == 0:
        return "整"
    
    result = []
    
    if jiao > 0:
        result.extend([CHINESE_DIGITS[jiao], "角"])
    elif fen > 0:
        result.append(CHINESE_DIGITS[0])
    
    if fen > 0:
        result.extend([CHINESE_DIGITS[fen], "分"])
    
    return "".join(result)

def convert(number: str) -> str:
    """
    将数字转换为中文大写金额
    
    Args:
        number: 待转换的数字字符串
    
    Returns:
        str: 转换后的中文大写金额
    """
    # 分离整数和小数部分
    integer_part, decimal_part = split_number(number)
    
    # 转换整数部分
    integer_chinese = convert_integer(integer_part)
    
    # 转换小数部分
    jiao = decimal_part // 10
    fen = decimal_part % 10
    decimal_chinese = convert_decimal(jiao, fen)
    
    # 组合结果
    result = integer_chinese + "元"
    if decimal_chinese != "整":
        result += decimal_chinese
    else:
        result += "整"
    
    return result 
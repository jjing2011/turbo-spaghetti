"""
解析模块的测试用例
"""
import pytest
from src.parser import split_number, normalize_number
from src.validation import (
    InvalidFormatError,
    OverflowError,
    NegativeNumberError
)

def test_split_number_basic():
    """测试基本的数值分割功能"""
    assert split_number("123.45") == (123, 45)
    assert split_number("1.23") == (1, 23)
    assert split_number("100") == (100, 0)
    assert split_number("0.01") == (0, 1)

def test_split_number_auto_padding():
    """测试小数位自动补零"""
    assert split_number("123.4") == (123, 40)
    assert split_number("1.5") == (1, 50)

def test_split_number_large_values():
    """测试大数值处理"""
    assert split_number("999999999999.99") == (999999999999, 99)
    assert split_number("100000000000.00") == (100000000000, 0)

def test_split_number_validation():
    """测试输入验证"""
    with pytest.raises(InvalidFormatError):
        split_number("123.456")  # 超过两位小数
    
    with pytest.raises(NegativeNumberError):
        split_number("-123.45")  # 负数
    
    with pytest.raises(OverflowError):
        split_number("1000000000000.00")  # 超出范围

def test_normalize_number():
    """测试数字规范化"""
    assert normalize_number("012.300") == "12.3"
    assert normalize_number("00123") == "123"
    assert normalize_number("1.23000") == "1.23"
    assert normalize_number("0.50") == "0.5"
    assert normalize_number("100.00") == "100"

def test_normalize_number_validation():
    """测试规范化输入验证"""
    with pytest.raises(InvalidFormatError):
        normalize_number("1,234.56")  # 包含逗号
    
    with pytest.raises(InvalidFormatError):
        normalize_number("abc")  # 非数字

def test_normalize_number_edge_cases():
    """测试规范化边界情况"""
    assert normalize_number("0.00") == "0"
    assert normalize_number("000.000") == "0"
    assert normalize_number("0.01") == "0.01" 
"""
解析模块的测试用例
"""
import pytest
from src.parser import split_number
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

def test_split_number_auto_truncate():
    """测试小数位自动截断"""
    assert split_number("123.456") == (123, 45)
    assert split_number("1.999") == (1, 99)
    assert split_number("0.999") == (0, 99)

def test_split_number_clean_zeros():
    """测试前导零和尾随零的清理"""
    assert split_number("00123.450") == (123, 45)
    assert split_number("000.100") == (0, 10)
    assert split_number("012.340") == (12, 34)

def test_split_number_validation():
    """测试输入验证"""
    with pytest.raises(NegativeNumberError):
        split_number("-123.45")  # 负数
    
    with pytest.raises(OverflowError):
        split_number("1000000000000.00")  # 超出范围
    
    with pytest.raises(InvalidFormatError):
        split_number("abc")  # 非数字

def test_split_number_edge_cases():
    """测试边界情况"""
    assert split_number("0.00") == (0, 0)
    assert split_number("999999999999.99") == (999999999999, 99)
    assert split_number("999999999999.999") == (999999999999, 99)  # 自动截断 
"""
转换器模块的测试用例
"""
import pytest
from src.converter import (
    convert,
    convert_integer,
    convert_decimal,
    _convert_4digits
)

def test_convert_4digits():
    """测试4位数转换"""
    assert _convert_4digits(1234) == "壹仟贰佰叁拾肆"
    assert _convert_4digits(1001) == "壹仟零壹"
    assert _convert_4digits(1100) == "壹仟壹佰"
    assert _convert_4digits(1010) == "壹仟零壹拾"
    assert _convert_4digits(10) == "壹拾"
    assert _convert_4digits(0) == ""

def test_convert_integer():
    """测试整数转换"""
    test_cases = [
        (0, "零"),
        (1, "壹"),
        (10, "壹拾"),
        (100, "壹佰"),
        (1000, "壹仟"),
        (10000, "壹万"),
        (100000000, "壹亿"),
        (10005, "壹万零伍"),
        (100050, "壹拾万零伍拾"),
        (100000001, "壹亿零壹"),
        (999999999999, "玖仟玖佰玖拾玖亿玖仟玖佰玖拾玖万玖仟玖佰玖拾玖")
    ]
    
    for num, expected in test_cases:
        assert convert_integer(num) == expected

def test_convert_decimal():
    """测试小数部分转换"""
    test_cases = [
        ((0, 0), "整"),
        ((5, 0), "伍角"),
        ((0, 5), "零伍分"),
        ((5, 5), "伍角伍分"),
        ((1, 0), "壹角"),
        ((0, 1), "零壹分")
    ]
    
    for (jiao, fen), expected in test_cases:
        assert convert_decimal(jiao, fen) == expected

def test_convert_full():
    """测试完整金额转换"""
    test_cases = [
        ("0", "零元整"),
        ("0.01", "零元零壹分"),
        ("0.10", "零元壹角"),
        ("0.50", "零元伍角"),
        ("1.23", "壹元贰角叁分"),
        ("100.05", "壹佰元零伍分"),
        ("1001.00", "壹仟零壹元整"),
        ("10001.10", "壹万零壹元壹角"),
        ("100000000.00", "壹亿元整"),
        ("999999999999.99", "玖仟玖佰玖拾玖亿玖仟玖佰玖拾玖万玖仟玖佰玖拾玖元玖角玖分")
    ]
    
    for number, expected in test_cases:
        assert convert(number) == expected

def test_convert_edge_cases():
    """测试边界情况"""
    test_cases = [
        ("00100.00", "壹佰元整"),
        ("000.50", "零元伍角"),
        ("0123.45", "壹佰贰拾叁元肆角伍分"),
        ("100.00", "壹佰元整"),
        ("100.", "壹佰元整")
    ]
    
    for number, expected in test_cases:
        assert convert(number) == expected 
"""
验证模块的测试用例
"""
import pytest
from src.validation import (
    validate,
    InvalidFormatError,
    OverflowError,
    NegativeNumberError
)

def test_valid_input():
    """测试有效输入"""
    assert validate("123.45") == True
    assert validate("0.01") == True
    assert validate("999999999999.99") == True
    assert validate(123.45) == True
    assert validate(123) == True

def test_negative_numbers():
    """测试负数处理"""
    with pytest.raises(NegativeNumberError) as exc:
        validate("-5")
    assert exc.value.code == "NEGATIVE_NUMBER"
    
    with pytest.raises(NegativeNumberError) as exc:
        validate("-123.45")
    assert exc.value.code == "NEGATIVE_NUMBER"

def test_invalid_format():
    """测试无效格式"""
    invalid_inputs = [
        "1a3",      # 包含字母
        "1,234",    # 包含逗号
        "1.234",    # 超过两位小数
        "abc",      # 纯字母
        "12。34",   # 中文句号
    ]
    
    for invalid_input in invalid_inputs:
        with pytest.raises(InvalidFormatError) as exc:
            validate(invalid_input)
        assert exc.value.code == "INVALID_FORMAT"

def test_overflow():
    """测试数值溢出"""
    with pytest.raises(OverflowError) as exc:
        validate("1000000000000.00")
    assert exc.value.code == "NUMBER_TOO_LARGE"
    
    with pytest.raises(OverflowError) as exc:
        validate("999999999999.999")
    assert exc.value.code == "NUMBER_TOO_LARGE" 
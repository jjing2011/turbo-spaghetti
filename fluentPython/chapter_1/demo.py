"""
人民币大写转换器演示脚本
"""
from src.optimized_converter import convert_optimized
from src.validation import InvalidFormatError

def demo():
    test_cases = [
        # 基本测试
        "0",           # 零元整
        "1.23",       # 普通小数
        "100.05",     # 带零的小数
        "1001.00",    # 整数元
        
        # 特殊数字处理
        "10001.10",   # 万位数
        "100000.00",  # 十万
        "1000000.00", # 百万
        "10000000.00", # 千万
        "100000000.00", # 亿
        
        # 零的特殊处理
        "10.01",      # 角位为零
        "10.10",      # 分位为零
        "100.00",     # 整数
        "10050",      # 中间有零
        "10000.56",   # 万后有零
        
        # 边界测试
        "999999999999.99",  # 最大值
        "0.01",            # 最小值（一分钱）
        "0.10",            # 一角
        "1234567.89",      # 复杂数字
        
        # 边界值测试（新增）
        "999999999999.999",   # 边界值（应截断为999999999999.99）
        "999999999999.9999",  # 边界值（应截断为999999999999.99）
        "999999999999.99999", # 边界值（应截断为999999999999.99）
    ]
    
    print("人民币大写转换器完整测试\n" + "="*30)
    
    for number in test_cases:
        try:
            result = convert_optimized(number)
            print(f"\n输入: {number}")
            print(f"输出: {result}")
        except InvalidFormatError as e:
            print(f"\n错误: {str(e)}")
            
    # 错误测试
    error_cases = [
        "-1.23",        # 负数
        "abc",          # 非法字符
        "1,234.56",     # 带逗号
        "1000000000000.00",  # 超出范围
        "1000000000000.999", # 超出范围（截断后仍超出）
    ]
    
    print("\n错误处理测试\n" + "="*30)
    for number in error_cases:
        try:
            result = convert_optimized(number)
            print(f"\n输入: {number}")
            print(f"输出: {result}")
        except Exception as e:
            print(f"\n输入: {number}")
            print(f"错误: {str(e)}")
            
    print("\n性能测试\n" + "="*30)
    import time
    start = time.perf_counter()
    for _ in range(1000):
        convert_optimized("123456789.99")
    end = time.perf_counter()
    print(f"1000次转换耗时: {(end-start)*1000:.2f}ms")
    print(f"平均每次耗时: {(end-start)*1000/1000:.3f}ms")

if __name__ == "__main__":
    demo() 
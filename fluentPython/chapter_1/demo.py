"""
人民币大写转换器演示脚本
"""
from src.optimized_converter import convert_optimized
from src.validation import InvalidFormatError

def demo():
    test_cases = [
        "0",           # 零元整
        "1.23",       # 普通小数
        "100.05",     # 带零的小数
        "1001.00",    # 整数元
        "10001.10",   # 万位数
        "100000000.00", # 亿位数
    ]
    
    print("人民币大写转换器演示\n" + "="*20)
    
    for number in test_cases:
        try:
            result = convert_optimized(number)
            print(f"\n输入: {number}")
            print(f"输出: {result}")
        except InvalidFormatError as e:
            print(f"\n错误: {str(e)}")
            
    print("\n性能测试示例:")
    import time
    start = time.perf_counter()
    for _ in range(1000):
        convert_optimized("123456789.99")
    end = time.perf_counter()
    print(f"1000次转换耗时: {(end-start)*1000:.2f}ms")
    print(f"平均每次耗时: {(end-start)*1000/1000:.3f}ms")

if __name__ == "__main__":
    demo() 
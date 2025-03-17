"""
性能测试模块
"""
import time
import random
from decimal import Decimal
from src.converter import convert

def generate_test_data(count: int = 100000) -> list:
    """生成测试数据"""
    test_data = []
    for _ in range(count):
        # 生成整数部分（0-999999999999）
        integer = random.randint(0, 999999999999)
        # 生成小数部分（0-99）
        decimal = random.randint(0, 99)
        # 组合成字符串
        number = f"{integer}.{decimal:02d}"
        test_data.append(number)
    return test_data

def run_performance_test(count: int = 100000) -> tuple:
    """
    运行性能测试
    
    Returns:
        tuple: (总时间, 平均时间, 最大时间, 最小时间)
    """
    # 生成测试数据
    test_data = generate_test_data(count)
    
    # 执行转换并记录时间
    times = []
    for number in test_data:
        start = time.perf_counter()
        convert(number)
        end = time.perf_counter()
        times.append(end - start)
    
    # 计算统计数据
    total_time = sum(times)
    avg_time = total_time / len(times)
    max_time = max(times)
    min_time = min(times)
    
    return total_time, avg_time, max_time, min_time

def main():
    """主函数"""
    # 运行性能测试
    count = 100000
    print(f"开始性能测试，样本数量：{count}")
    
    total_time, avg_time, max_time, min_time = run_performance_test(count)
    
    # 输出结果
    print("\n性能测试结果：")
    print(f"总时间: {total_time:.2f} 秒")
    print(f"平均时间: {avg_time*1000:.2f} 毫秒")
    print(f"最大时间: {max_time*1000:.2f} 毫秒")
    print(f"最小时间: {min_time*1000:.2f} 毫秒")
    
    # 检查性能指标
    if avg_time < 0.01:  # 10ms
        print("\n✅ 性能测试通过：平均转换时间小于10ms")
    else:
        print("\n❌ 性能测试失败：平均转换时间大于10ms")

if __name__ == "__main__":
    main() 
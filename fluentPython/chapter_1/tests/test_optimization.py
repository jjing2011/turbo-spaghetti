"""
优化效果对比测试
"""
import time
import random
from typing import List, Tuple
from src.converter import convert
from src.optimized_converter import convert_optimized

def generate_test_cases(count: int = 1000) -> List[str]:
    """生成测试数据"""
    test_cases = []
    for _ in range(count):
        integer = random.randint(0, 999999999999)
        decimal = random.randint(0, 99)
        number = f"{integer}.{decimal:02d}"
        test_cases.append(number)
    return test_cases

def benchmark_conversion(func, test_cases: List[str]) -> Tuple[float, float, float]:
    """
    对转换函数进行基准测试
    
    Returns:
        Tuple[float, float, float]: (总时间, 平均时间, 最大时间)
    """
    times = []
    for number in test_cases:
        start = time.perf_counter()
        func(number)
        end = time.perf_counter()
        times.append(end - start)
    
    total_time = sum(times)
    avg_time = total_time / len(times)
    max_time = max(times)
    
    return total_time, avg_time, max_time

def test_optimization_effect():
    """测试优化效果"""
    # 生成测试数据
    test_cases = generate_test_cases(1000)
    
    # 测试原始版本
    original_total, original_avg, original_max = benchmark_conversion(
        convert, test_cases
    )
    
    # 测试优化版本
    optimized_total, optimized_avg, optimized_max = benchmark_conversion(
        convert_optimized, test_cases
    )
    
    # 计算性能提升
    speedup = original_avg / optimized_avg
    
    # 输出结果
    print("\n性能对比结果：")
    print(f"原始版本 - 平均: {original_avg*1000:.3f}ms, 最大: {original_max*1000:.3f}ms")
    print(f"优化版本 - 平均: {optimized_avg*1000:.3f}ms, 最大: {optimized_max*1000:.3f}ms")
    print(f"性能提升: {speedup:.2f}x")
    
    # 验证优化效果
    assert optimized_avg < original_avg, "优化版本应该更快"
    assert optimized_avg < 0.01, "优化版本应该满足10ms的性能要求"

def test_optimization_correctness():
    """测试优化版本的正确性"""
    test_cases = [
        "0", "0.01", "0.10", "0.50",
        "1.23", "100.05", "1001.00",
        "10001.10", "100000000.00",
        "999999999999.99"
    ]
    
    for number in test_cases:
        original_result = convert(number)
        optimized_result = convert_optimized(number)
        assert optimized_result == original_result, \
            f"优化版本结果不一致：{number} -> {optimized_result} != {original_result}"

if __name__ == "__main__":
    test_optimization_effect()
    test_optimization_correctness() 
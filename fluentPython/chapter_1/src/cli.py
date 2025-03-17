"""
命令行接口模块
"""
import sys
from .converter import convert
from .validation import ConversionError

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python -m src.cli <数字>")
        print("示例: python -m src.cli 123.45")
        sys.exit(1)
    
    try:
        result = convert(sys.argv[1])
        print(result)
    except ConversionError as e:
        print(f"错误: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
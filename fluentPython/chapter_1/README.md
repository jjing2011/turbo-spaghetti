# 人民币数字金额转大写工具

这是一个将人民币数字金额转换为大写的Python工具。

## 功能特点

- 支持输入验证（纯数字、小数位检查等）
- 处理金额范围：0.01 到 999,999,999,999.99
- 标准的中文大写金额输出
- 完善的错误处理机制
- 支持命令行调用

## 安装

使用 Poetry 安装项目依赖：

```bash
poetry install
```

## 使用方法

### 作为Python模块使用

```python
from src.converter import convert

try:
    # 基本使用
    result = convert("123.45")
    print(result)  # 输出：壹佰贰拾叁元肆角伍分
    
    # 处理整数
    result = convert("100")
    print(result)  # 输出：壹佰元整
    
    # 处理小数
    result = convert("0.05")
    print(result)  # 输出：零元零伍分
except Exception as e:
    print(f"错误：{e}")
```

### 命令行使用

```bash
# 基本使用
python -m src.cli 123.45
# 输出：壹佰贰拾叁元肆角伍分

# 处理整数
python -m src.cli 100
# 输出：壹佰元整

# 处理小数
python -m src.cli 0.05
# 输出：零元零伍分
```

## 开发

### 运行测试

```bash
poetry run pytest
```

### 代码风格检查

```bash
poetry run flake8
```

## 项目结构

```
.
├── src/
│   ├── __init__.py
│   ├── validation.py    # 输入验证模块
│   ├── parser.py       # 数值解析模块
│   ├── converter.py    # 转换核心模块
│   └── cli.py         # 命令行接口
├── tests/
│   ├── __init__.py
│   ├── test_validation.py
│   ├── test_parser.py
│   └── test_converter.py
├── pyproject.toml      # 项目配置和依赖
└── README.md          # 项目文档
```

## 转换规则

1. 整数部分：
   - 基本单位：个、拾、佰、仟
   - 大单位：万、亿
   - 零的处理：
     - 多个连续的零合并为一个
     - 万、亿前的零省略
     - 个位是零时省略

2. 小数部分：
   - 角分位：角、分
   - 没有小数时用"整"字
   - 角为零分不为零时，加"零"字

## 错误处理

- 格式错误：非法字符、超过两位小数等
- 范围错误：超出范围（大于999,999,999,999.99）
- 负数错误：不支持负数转换

## 许可证

MIT 
# 使用Python官方镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 安装poetry
RUN pip install poetry

# 复制项目文件
COPY pyproject.toml poetry.lock* ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY README.md ./

# 配置poetry不创建虚拟环境（在容器中没有必要）
RUN poetry config virtualenvs.create false

# 安装依赖
RUN poetry install --no-dev

# 设置环境变量
ENV PYTHONPATH=/app

# 设置容器启动命令
ENTRYPOINT ["python", "-m", "src.cli"]
CMD ["123.45"] 
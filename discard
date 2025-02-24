# 使用 Python 3.7 作为基础镜像
FROM python:3.7-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt requirements.txt

# 安装依赖
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# 复制代码到容器中
COPY . .

# 设置启动命令
ENTRYPOINT ["sh", "-c", "python app.py"]

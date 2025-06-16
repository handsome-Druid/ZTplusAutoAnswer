FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt dist-upgrade -y && \
    apt install -y python3 python3-pip && \
    apt install -y python3-flask python3-flask-cors sqlite3 && \
    apt clean && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /ztplus

# 复制本地项目文件到容器内
COPY . /ztplus

# 默认命令
CMD ["python3", "question_server.py"]

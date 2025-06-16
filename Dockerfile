FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt dist-upgrade -y && \
    apt install -y python3 python3-pip && \
    apt install -y python3-flask python3-flask-cors sqlite3 && \
    apt clean && rm -rf /var/lib/apt/lists/*

# ��������Ŀ¼
WORKDIR /ztplus

# ���Ʊ�����Ŀ�ļ���������
COPY . /ztplus

# Ĭ������
CMD ["python3", "question_server.py"]

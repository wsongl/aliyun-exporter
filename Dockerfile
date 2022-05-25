FROM python:3.8
WORKDIR /opt/
ADD . /opt/
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
EXPOSE 8080
CMD python main.py

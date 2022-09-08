FROM python:3.8-buster

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./student_management_system ./

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
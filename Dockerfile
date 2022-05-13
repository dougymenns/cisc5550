# Dockerfile, Image, Container
FROM python:3.8.5
ARG api_ip
ENV TODO_API=${api_ip}
RUN pip install flask
RUN pip install requests
EXPOSE 80/tcp
COPY todolist.py . 
COPY todolist.db .
COPY users.db .
COPY templates/homepage.html templates/
COPY templates/login.html templates/
COPY templates/register.html templates/
COPY templates/login_retry.html templates/
CMD python3 todolist.py


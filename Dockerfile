FROM python:3.11

COPY . .
RUN apt update && apt install -y uwsgi
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
ENV PORT=8080
EXPOSE 8080

CMD ["./start.sh"]
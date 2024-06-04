FROM python

COPY . .
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh ./lite
ENV PORT=8080
EXPOSE 8080

CMD ["./start.sh"]
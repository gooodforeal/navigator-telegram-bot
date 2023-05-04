FROM python:3.9
COPY . .
RUN pip3 install -r requirements.txt
CMD python TRPP_project/bot.py

FROM --platform=linux/amd64 python:3.8
COPY requirements.txt /opt/sale-fish-bot/requirements.txt
WORKDIR /opt/sale-fish-bot
RUN pip install -r requirements.txt
COPY . /opt/sale-fish-bot
CMD ["python", "bot.py"]


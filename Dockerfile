FROM --platform=linux/amd64 python:3.8
COPY requirements.txt /opt/sale_fish_bot/requirements.txt
WORKDIR /opt/sale_fish_bot
RUN pip install -r requirements.txt
COPY . /opt/sale_fish_bot

CMD ["python", "bot.py"]


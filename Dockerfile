FROM --platform=linux/amd64 python:3.8
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN mkdir -p /opt/apps/sale-fish-bot
COPY requirements.txt /opt/apps/sale-fish-bot/requirements.txt
WORKDIR /opt/apps/sale-fish-bot
COPY . /opt/apps/sale-fish-bot
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]


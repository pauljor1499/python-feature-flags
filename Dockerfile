FROM python:3.10-slim

RUN mkdir /Questions-Bank-Backend
WORKDIR /Questions-Bank-Backend
RUN ls -l

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN python -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . /Questions-Bank-Backend
RUN ls -l

EXPOSE 8002

CMD ["sh", "-c", ". venv/bin/activate && python main.py"]

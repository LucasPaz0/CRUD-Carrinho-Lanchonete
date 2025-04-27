FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

CMD ["python", "crud_carrinho_lanchonete.py"]

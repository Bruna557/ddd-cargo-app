FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./cargo_shipping /code/cargo_shipping

CMD ["uvicorn", "cargo_shipping.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

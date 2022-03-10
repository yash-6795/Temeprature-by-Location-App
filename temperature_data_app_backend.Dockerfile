#
FROM python:3.9

#
WORKDIR /code

#
COPY ./API/requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./API /code

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
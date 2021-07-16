FROM python:3.8

# WORKDIR /code

COPY ./my_flask /code

RUN pip install -r /code/requirements.txt

# EXPOSE 5555

ENV MYTESTPORT 5051

CMD ["python", "/code/app.py"]
FROM python:3.11-slim


WORKDIR /src


COPY . /src
RUN pip install -r /src/req.txt


EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "src/core/log.config"]
